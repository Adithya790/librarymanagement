from django.shortcuts import render,get_object_or_404
from .models import Book, Category
from django.db.models import Q

def home(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    total_books = Book.objects.count()
    total_members = 120
    issued_books = 45

    context = {
        'books': books,
        'categories': categories,
        'total_books': total_books,
        'total_members': total_members,
        'issued_books': issued_books,
    }

    return render(request, 'home.html', context)

def book_list(request):

    books = Book.objects.all()
    categories = Category.objects.all()

    search = request.GET.get('search')
    category = request.GET.get('category')

    # Search functionality
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    # Category filter
    if category:
        books = books.filter(category_id=category)

    context = {
        'books': books,
        'categories': categories,
    }

    return render(request, 'book_list.html', context)

def book_detail(request, id):

    book = get_object_or_404(Book, id=id)

    context = {
        'book': book
    }

    return render(request, 'book_detail.html', context)
