from django.urls import path
from .views import (
    home,
    book_list,
    book_detail,
    issue_book,
    reserve_book,
    reserved_books,
    remove_reservation,
    my_issued_books,
    return_book,
    due_fines
)
urlpatterns = [

    path('', home, name='home'),

    path('books/', book_list, name='book_list'),

    path('book/<int:id>/', book_detail, name='book_detail'),

    path('issue/<int:id>/', issue_book, name='issue_book'),

    path('issued-books/', my_issued_books, name='my_issued_books'),

    path('return-book/<int:id>/', return_book, name='return_book'),

    path('due-fines/', due_fines, name='due_fines'),

    path('reserve/<int:id>/', reserve_book, name='reserve_book'),

    path('reserve-books/', reserved_books, name='reserved_books'),

    path('remove-reserve/<int:id>/', remove_reservation, name='remove_reservation'),
]