from django.db import models

from django.db import models

class ShopStats(models.Model):
    active_books_count = models.IntegerField(default=0)
    inactive_books_count = models.IntegerField(default=0)
    active_authors_count = models.IntegerField(default=0)
    inactive_authors_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats updated at {self.updated_at}"
