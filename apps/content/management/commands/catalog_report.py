from django.core.management.base import BaseCommand
from django.db.models import Count, Avg, Min, Max

from ...models import Category, Model


class Command(BaseCommand):
    help = "Prints a summary report of the catalog"

    def add_arguments(self, parser):
        parser.add_argument("--category", default=None)

    def handle(self, *args, **kwargs):
        category_name = kwargs["category"]

        categories = Category.objects.all()

        if category_name:
            categories = categories.filter(name=category_name)

        if not categories.exists():
            self.stderr.write(self.style.ERROR("No categories found."))
            return

        for category in categories:
            products = Model.objects.filter(category=category)

            stats = products.aggregate(
                count=Count("id"),
                avg_price=Avg("price"),
                min_price=Min("price"),
                max_price=Max("price"),
            )

            no_image = products.filter(image="").count()

            self.stdout.write(self.style.SUCCESS(f"\n P{category.name}"))
            self.stdout.write(f"  Products   : {stats['count']}")
            self.stdout.write(f"  Min price  : {stats['min_price'] or 0:.2f}")
            self.stdout.write(f"  Max price  : {stats['max_price'] or 0:.2f}")
            self.stdout.write(f"  Avg price  : {stats['avg_price'] or 0:.2f}")

            if no_image:
                self.stdout.write(self.style.WARNING(f"  No image   : {no_image} product(s)"))
            else:
                self.stdout.write(f"  No image   : 0")