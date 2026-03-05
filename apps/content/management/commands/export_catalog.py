import csv
import json
import os

from django.core.management.base import BaseCommand

from ...models import Model

class Command(BaseCommand):
    help = "Exports all products to CSV or JSON file, grouped by category"

    def add_arguments(self, parser):
        parser.add_argument("--format", choices=["csv", "json"], default="json")
        parser.add_argument("--output", default="catalog")
        parser.add_argument("--category", default=None)

    def handle(self, *args, **kwargs):
        fmt = kwargs["format"]
        output = kwargs["output"]
        category = kwargs["category"]

        products = Model.objects.select_related("category").all()

        if category:
            products = products.filter(category__name=category)

        if not products.exists():
            self.stderr.write("No products found.")
            return

        if not output.endswith(f".{fmt}"):
            output = f"{output}.{fmt}"

        if fmt == "csv":
            self._export_csv(products, output)
        else:
            self._export_json(products, output)

        self.stdout.write(self.style.SUCCESS(f"Exported {products.count()} products to {output}"))

    def _export_csv(self, products, output):
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "description", "price", "category"])
            for p in products.order_by("category__name"):
                writer.writerow([p.id, p.name, p.description, p.price, p.category.name])

    def _export_json(self, products, output):
        grouped = {}
        for p in products.order_by("category__name"):
            cat = p.category.name
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": float(p.price),
            })
        with open(output, "w", encoding="utf-8") as f:
            json.dump(grouped, f, indent=2, ensure_ascii=False)