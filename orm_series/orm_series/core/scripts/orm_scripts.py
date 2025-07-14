from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from pprint import pprint


# core/scripts/init/orm_scripts.py


from core.models import Staff, Restaurant

def run():
    restaurants = list(Restaurant.objects.all())

    if len(restaurants) < 3:
        print(f"❌ Not enough restaurants! Found {len(restaurants)}, need at least 3.")
        return

    # Pick the first 3 available restaurants
    r1, r2, r3 = restaurants[:3]

    # Create staff
    s1 = Staff.objects.create(name="John Doe")
    s2 = Staff.objects.create(name="Jane Smith")
    s3 = Staff.objects.create(name="Alice Johnson")

    # Link them with restaurants
    s1.restaurant.set([r1, r2])
    s2.restaurant.set([r2, r3])
    s3.restaurant.set([r1, r3])

    print("✅ Staff members created and linked to the following restaurants:")
    print(f"  - {s1.name} ➝ {[r.name for r in s1.restaurant.all()]}")
    print(f"  - {s2.name} ➝ {[r.name for r in s2.restaurant.all()]}")
    print(f"  - {s3.name} ➝ {[r.name for r in s3.restaurant.all()]}")
