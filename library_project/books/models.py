from django.db import models

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