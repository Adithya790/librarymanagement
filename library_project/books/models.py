from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/')
    description = models.TextField()
    stock = models.IntegerField(default=1)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Reservation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reserved {self.book.title}"



class IssuedBook(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE )

    book = models.ForeignKey(Book, on_delete=models.CASCADE )

    issue_date = models.DateField(auto_now_add=True)

    due_date = models.DateField()

    return_date = models.DateField(null=True,blank=True)

    fine = models.DecimalField(max_digits=8,decimal_places=2,default=0)

    status = models.CharField(max_length=20,default='Issued')
    def __str__(self):return f"{self.user.username} - {self.book.title}"