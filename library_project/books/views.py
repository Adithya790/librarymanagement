from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages

from .models import Book, Category, Reservation


def home(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    return render(request, 'home.html', {
        'books': books,
        'categories': categories,
        'total_books': Book.objects.count(),
        'total_members': 120,
        'issued_books': 45,
    })



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
        books = books.filter(category_id=category)

    return render(request, 'book_list.html', {
        'books': books,
        'categories': categories,
    })



def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    return render(request, 'book_detail.html', {
        'book': book
    })



def issue_book(request, id):

    book = get_object_or_404(Book, id=id)

    if book.stock > 0:
        book.stock -= 1
        book.save()
        messages.success(request, "Book issued successfully!")
    else:
        messages.error(request, "Book is out of stock!")

    return redirect('book_detail', id=id)



def reserve_book(request, id):

    if not request.user.is_authenticated:
        messages.error(request, "You must login first to reserve a book.")
        return redirect('book_detail', id=id)

    book = get_object_or_404(Book, id=id)

    reservation, created = Reservation.objects.get_or_create(
        user=request.user,
        book=book
    )

    if created:
        messages.success(request, f"'{book.title}' added to wishlist!")
    else:
        messages.warning(request, f"'{book.title}' already in wishlist!")

    return redirect('reserved_books')



def reserved_books(request):

    if not request.user.is_authenticated:
        return redirect('login')

    reservations = Reservation.objects.filter(
        user=request.user
    ).order_by('-created_at')  

    return render(request, 'reserve_books.html', {
        'reservations': reservations
    })


def remove_reservation(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, id=id)

    Reservation.objects.filter(user=request.user, book=book).delete()

    messages.success(request, "Removed from wishlist")

    return redirect('reserved_books')