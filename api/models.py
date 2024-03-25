from django.db import models
from user.models import Author

class  Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name ='book')
    publication_date = models.DateField()

    def __str__(self):
        return self.title