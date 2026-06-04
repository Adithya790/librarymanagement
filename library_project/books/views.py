from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import (
    Book,
    Category,
    Reservation,
    IssuedBook
)


# HOME PAGE
def home(request):

    books = Book.objects.all()
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'books': books,
        'categories': categories,
        'total_books': Book.objects.count(),
        'total_members': 120,
        'issued_books': IssuedBook.objects.count(),
    })


# BOOK LIST PAGE
def book_list(request):

    books = Book.objects.all()
    categories = Category.objects.all()

    search = request.GET.get('search')
    category = request.GET.get('category')

    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    if category:
        books = books.filter(
            category_id=category
        )

    return render(
        request,
        'book_list.html',
        {
            'books': books,
            'categories': categories,
        }
    )


# BOOK DETAIL PAGE
def book_detail(request, id):

    book = get_object_or_404(
        Book,
        id=id
    )

    return render(
        request,
        'book_detail.html',
        {
            'book': book
        }
    )


# ISSUE BOOK
def issue_book(request, id):

    if not request.user.is_authenticated:

        messages.error(
            request,
            "Please login first."
        )

        return redirect('login')

    book = get_object_or_404(
        Book,
        id=id
    )

    if book.stock > 0:

        due_date = (
            timezone.now().date()
            + timedelta(days=14)
        )

        IssuedBook.objects.create(
            user=request.user,
            book=book,
            due_date=due_date
        )

        book.stock -= 1

        if book.stock == 0:
            book.available = False

        book.save()

        messages.success(
            request,
            f"{book.title} issued successfully!"
        )

    else:

        messages.error(
            request,
            "Book is out of stock!"
        )

    return redirect(
        'book_detail',
        id=id
    )


# MY ISSUED BOOKS
def my_issued_books(request):

    if not request.user.is_authenticated:
        return redirect('login')

    issued_books = IssuedBook.objects.filter(
        user=request.user
    ).order_by('-issue_date')

    return render(
        request,
        'issued_books.html',
        {
            'issued_books': issued_books
        }
    )


# RETURN BOOK
def return_book(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    issue = get_object_or_404(
        IssuedBook,
        id=id,
        user=request.user
    )

    today = timezone.now().date()

    issue.return_date = today
    issue.status = "Returned"

    if today > issue.due_date:

        late_days = (
            today - issue.due_date
        ).days

        issue.fine = late_days * 10

    issue.save()

    book = issue.book

    book.stock += 1
    book.available = True
    book.save()

    messages.success(
        request,
        "Book returned successfully!"
    )

    return redirect(
        'my_issued_books'
    )


# RESERVE BOOK
def reserve_book(request, id):

    if not request.user.is_authenticated:

        messages.error(
            request,
            "You must login first."
        )

        return redirect(
            'book_detail',
            id=id
        )

    book = get_object_or_404(
        Book,
        id=id
    )

    reservation, created = Reservation.objects.get_or_create(
        user=request.user,
        book=book
    )

    if created:

        messages.success(
            request,
            f"'{book.title}' added to wishlist!"
        )

    else:

        messages.warning(
            request,
            f"'{book.title}' already in wishlist!"
        )

    return redirect(
        'reserved_books'
    )


# RESERVED BOOKS PAGE
def reserved_books(request):

    if not request.user.is_authenticated:
        return redirect('login')

    reservations = Reservation.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'reserve_books.html',
        {
            'reservations': reservations
        }
    )


# REMOVE RESERVATION
def remove_reservation(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(
        Book,
        id=id
    )

    Reservation.objects.filter(
        user=request.user,
        book=book
    ).delete()

    messages.success(
        request,
        "Removed from wishlist"
    )

    return redirect(
        'reserved_books'
    )

# DUE DATE & FINES PAGE
def due_fines(request):

    if not request.user.is_authenticated:
        return redirect('login')

    issued_books = IssuedBook.objects.filter(
        user=request.user
    )

    total_fine = issued_books.aggregate(
        total=Sum('fine')
    )['total'] or 0

    return render(
        request,
        'due_fines.html',
        {
            'issued_books': issued_books,
            'total_fine': total_fine
        }
    )