from django.core.management.base import BaseCommand
from django.db.models import F

from ...models import Category, Model


class Command(BaseCommand):
    help = "Applies a percentage price change to all products in a given category"

    def add_arguments(self, parser):
        parser.add_argument("--category", required=True)
        parser.add_argument("--percent", type=float, required=True)

    def handle(self, *args, **kwargs):
        category_name = kwargs["category"]
        percent = kwargs["percent"]

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Category '{category_name}' not found."))
            return

        products = Model.objects.filter(category=category)

        if not products.exists():
            self.stderr.write(self.style.WARNING(f"No products found in '{category_name}'."))
            return

        multiplier = 1 + percent / 100
        products.update(price=F("price") * multiplier)

        self.stdout.write(self.style.SUCCESS(
            f"Updated {products.count()} products in '{category_name}' by {percent:+.1f}%"
        ))