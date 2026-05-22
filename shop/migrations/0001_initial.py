from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="створено о")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="оновлено о")),
                ("name", models.CharField(max_length=120, verbose_name="назва")),
                ("slug", models.SlugField(unique=True, verbose_name="посилання")),
                ("description", models.TextField(blank=True, verbose_name="опис")),
            ],
            options={
                "verbose_name": "категорія",
                "verbose_name_plural": "категорії",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="NewsletterSubscriber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="створено о")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="оновлено о")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="email")),
                ("full_name", models.CharField(blank=True, max_length=120, verbose_name="ім'я")),
            ],
            options={
                "verbose_name": "підписник",
                "verbose_name_plural": "підписники",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="створено о")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="оновлено о")),
                ("name", models.CharField(max_length=160, verbose_name="назва")),
                ("slug", models.SlugField(unique=True, verbose_name="посилання")),
                ("description", models.TextField(verbose_name="опис")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="ціна")),
                ("image", models.ImageField(blank=True, upload_to="products/", verbose_name="зображення")),
                ("is_popular", models.BooleanField(default=False, verbose_name="популярний товар")),
                ("is_sale", models.BooleanField(default=False, verbose_name="акційний товар")),
                ("stock", models.PositiveIntegerField(default=0, verbose_name="кількість на складі")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to="shop.category", verbose_name="категорія")),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товари",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="створено о")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="оновлено о")),
                ("customer_name", models.CharField(max_length=120, verbose_name="ім'я покупця")),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                ("phone", models.CharField(max_length=30, verbose_name="телефон")),
                ("address", models.CharField(max_length=255, verbose_name="адреса")),
                ("status", models.CharField(choices=[("new", "Нове"), ("processing", "В обробці"), ("done", "Виконано")], default="new", max_length=20, verbose_name="статус")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to=settings.AUTH_USER_MODEL, verbose_name="користувач")),
            ],
            options={
                "verbose_name": "замовлення",
                "verbose_name_plural": "замовлення",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PasswordResetCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="створено о")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="оновлено о")),
                ("code", models.CharField(max_length=8, verbose_name="тимчасовий код")),
                ("is_used", models.BooleanField(default=False, verbose_name="використано")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reset_codes", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "код відновлення пароля",
                "verbose_name_plural": "коди відновлення пароля",
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1, verbose_name="кількість")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="ціна")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="shop.order", verbose_name="замовлення")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="shop.product", verbose_name="товар")),
            ],
            options={
                "verbose_name": "товар у замовленні",
                "verbose_name_plural": "товари у замовленні",
            },
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="створено о")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="оновлено о")),
                ("score", models.PositiveSmallIntegerField(verbose_name="оцінка")),
                ("comment", models.TextField(blank=True, verbose_name="коментар")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ratings", to="shop.product", verbose_name="товар")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="ratings", to=settings.AUTH_USER_MODEL, verbose_name="користувач")),
            ],
            options={
                "verbose_name": "оцінка",
                "verbose_name_plural": "оцінки",
                "unique_together": {("product", "user")},
            },
        ),
    ]
