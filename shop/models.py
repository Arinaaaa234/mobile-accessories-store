from django.conf import settings
from django.db import models
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("створено о", auto_now_add=True)
    updated_at = models.DateTimeField("оновлено о", auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField("назва", max_length=120)
    slug = models.SlugField("посилання", unique=True)
    description = models.TextField("опис", blank=True)

    class Meta:
        verbose_name = "категорія"
        verbose_name_plural = "категорії"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        verbose_name="категорія",
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField("назва", max_length=160)
    slug = models.SlugField("посилання", unique=True)
    description = models.TextField("опис")
    price = models.DecimalField("ціна", max_digits=10, decimal_places=2)
    image = models.ImageField("зображення", upload_to="products/", blank=True)
    is_popular = models.BooleanField("популярний товар", default=False)
    is_sale = models.BooleanField("акційний товар", default=False)
    stock = models.PositiveIntegerField("кількість на складі", default=0)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товари"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    @property
    def average_rating(self):
        value = self.ratings.aggregate(models.Avg("score"))["score__avg"]
        return round(value, 1) if value else 0


class NewsletterSubscriber(TimeStampedModel):
    email = models.EmailField("email", unique=True)
    full_name = models.CharField("ім'я", max_length=120, blank=True)

    class Meta:
        verbose_name = "підписник"
        verbose_name_plural = "підписники"

    def __str__(self):
        return self.email


class Rating(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name="товар",
        related_name="ratings",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="користувач",
        related_name="ratings",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    score = models.PositiveSmallIntegerField("оцінка")
    comment = models.TextField("коментар", blank=True)

    class Meta:
        verbose_name = "оцінка"
        verbose_name_plural = "оцінки"
        unique_together = ["product", "user"]

    def __str__(self):
        return f"{self.product} - {self.score}/5"


class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ("new", "Нове"),
        ("processing", "В обробці"),
        ("done", "Виконано"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="користувач",
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer_name = models.CharField("ім'я покупця", max_length=120)
    email = models.EmailField("email")
    phone = models.CharField("телефон", max_length=30)
    address = models.CharField("адреса", max_length=255)
    status = models.CharField("статус", max_length=20, choices=STATUS_CHOICES, default="new")

    class Meta:
        verbose_name = "замовлення"
        verbose_name_plural = "замовлення"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Замовлення #{self.pk} - {self.customer_name}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="замовлення",
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Product, verbose_name="товар", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("кількість", default=1)
    price = models.DecimalField("ціна", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "товар у замовленні"
        verbose_name_plural = "товари у замовленні"

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price


class PasswordResetCode(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reset_codes", on_delete=models.CASCADE)
    code = models.CharField("тимчасовий код", max_length=8)
    is_used = models.BooleanField("використано", default=False)

    class Meta:
        verbose_name = "код відновлення пароля"
        verbose_name_plural = "коди відновлення пароля"

    def __str__(self):
        return f"Код для {self.user}"
