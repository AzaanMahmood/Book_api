from django.db import models
from user.models import Author


class CustomQueryset(models.QuerySet):
    def fil(self):
        return self.filter(is_active=True)
    
class ActiveBookManager(models.Manager):
    
    def fil(self):
        return self.get_queryset().fil()
    def get_queryset(self):
        return CustomQueryset(model=self.model, using=self._db, hints=self._hints)
    

class  Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name ='book')
    publication_date = models.DateField()
    is_active = models.BooleanField(default=True)

    objects = ActiveBookManager()  # The default manager
    active_objects = ActiveBookManager()

    def __str__(self):
        return self.title
    