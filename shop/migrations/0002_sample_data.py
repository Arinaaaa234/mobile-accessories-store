from decimal import Decimal

from django.db import migrations


def add_sample_data(apps, schema_editor):
    Category = apps.get_model("shop", "Category")
    Product = apps.get_model("shop", "Product")

    cases, _ = Category.objects.get_or_create(
        slug="cases",
        defaults={"name": "Чохли", "description": "Захисні та стильні чохли для смартфонів."},
    )
    headphones, _ = Category.objects.get_or_create(
        slug="headphones",
        defaults={"name": "Навушники", "description": "Дротові та бездротові навушники."},
    )
    chargers, _ = Category.objects.get_or_create(
        slug="chargers",
        defaults={"name": "Зарядні пристрої", "description": "Блоки живлення, кабелі та швидкі зарядки."},
    )
    powerbanks, _ = Category.objects.get_or_create(
        slug="powerbanks",
        defaults={"name": "Павербанки", "description": "Зовнішні акумулятори для подорожей і роботи."},
    )
    glass, _ = Category.objects.get_or_create(
        slug="screen-protectors",
        defaults={"name": "Захисне скло", "description": "Скло та плівки для захисту екрана."},
    )

    products = [
        (cases, "Силіконовий чохол iPhone 15", "silicone-case-iphone-15", "М'який чохол з приємним покриттям.", Decimal("399.00"), True, True),
        (headphones, "Бездротові навушники AirSound", "airsound-wireless", "Компактні навушники з кейсом для заряджання.", Decimal("1299.00"), True, False),
        (chargers, "Швидка зарядка USB-C 30W", "usb-c-charger-30w", "Зарядний пристрій для смартфонів з підтримкою fast charge.", Decimal("649.00"), True, True),
        (powerbanks, "Павербанк 20000 mAh", "powerbank-20000", "Ємний павербанк з двома USB-портами.", Decimal("1599.00"), False, True),
        (glass, "Захисне скло Samsung Galaxy", "samsung-galaxy-glass", "Міцне прозоре скло з олеофобним покриттям.", Decimal("249.00"), False, False),
    ]
    for category, name, slug, description, price, popular, sale in products:
        Product.objects.get_or_create(
            slug=slug,
            defaults={
                "category": category,
                "name": name,
                "description": description,
                "price": price,
                "is_popular": popular,
                "is_sale": sale,
                "stock": 15,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_sample_data, migrations.RunPython.noop),
    ]
