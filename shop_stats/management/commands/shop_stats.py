from django.core.management.base import BaseCommand
from api.models import Book
from user.models import Author
from shop_stats.models import ShopStats

class Command(BaseCommand):
    help = 'Updates the shop stats in the database'

    def handle(self, *args, **options):
        active_books_count = Book.objects.filter(is_active=True).count()
        inactive_books_count = Book.objects.filter(is_active=False).count()
        active_authors_count = Author.objects.filter(is_active=True).count()
        inactive_authors_count = Author.objects.filter(is_active=False).count()

        ShopStats.objects.create(
            active_books_count=active_books_count,
            inactive_books_count=inactive_books_count,
            active_authors_count=active_authors_count,
            inactive_authors_count=inactive_authors_count
        )

        self.stdout.write(self.style.SUCCESS('Shop stats updated successfully'))