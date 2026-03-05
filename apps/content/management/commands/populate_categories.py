import json
import os

from django.core.management.base import BaseCommand

from apps.content.models import Category
from apps.content.serializers import CategoryCreateSerializer


FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "category.jsonl")


def _parse_jsonl(path):
    result = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                result.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {e}")
    return result


class Command(BaseCommand):
    help = "Populate database with Categories from jsonl file"

    def add_arguments(self, parser):
        parser.add_argument("--seed", action="store_true", help="Seed categories")
        parser.add_argument("--delete", action="store_true", help="Delete all categories")

    def handle(self, *args, **kwargs):
        if kwargs["delete"]:
            count, _ = Category.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {count} categories"))
            return

        data = _parse_jsonl(FILE_PATH)
        serializer = CategoryCreateSerializer(data=data, many=True)

        if not serializer.is_valid():
            self.stderr.write(str(serializer.errors))
            return

        Category.objects.bulk_create([
            Category(**item) for item in serializer.validated_data
        ])
        self.stdout.write(self.style.SUCCESS(f"Created {len(serializer.validated_data)} categories"))