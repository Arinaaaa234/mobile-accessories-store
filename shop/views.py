import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    NewsletterForm,
    OrderForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
    RatingForm,
    RegisterForm,
)
from .models import Category, Order, OrderItem, PasswordResetCode, Product, Rating


def home(request):
    popular_products = Product.objects.filter(is_popular=True)[:4]
    sale_products = Product.objects.filter(is_sale=True)[:4]
    newsletter_form = NewsletterForm()
    if request.method == "POST":
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "Ви підписались на розсилку.")
            return redirect("home")
    return render(
        request,
        "home.html",
        {
            "popular_products": popular_products,
            "sale_products": sale_products,
            "newsletter_form": newsletter_form,
        },
    )


def catalog(request):
    products = Product.objects.select_related("category")
    return render(request, "catalog.html", {"products": products})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, "category_detail.html", {"category": category, "products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    rating_form = RatingForm()
    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.product = product
            rating.user = request.user if request.user.is_authenticated else None
            if rating.user:
                Rating.objects.update_or_create(
                    product=product,
                    user=rating.user,
                    defaults={"score": rating.score, "comment": rating.comment},
                )
            else:
                rating.save()
            messages.success(request, "Дякуємо за оцінку товару.")
            return redirect(product.get_absolute_url())
    return render(request, "product_detail.html", {"product": product, "rating_form": rating_form})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    product_key = str(product.id)
    cart[product_key] = cart.get(product_key, 0) + 1
    request.session["cart"] = cart
    messages.success(request, f"{product.name} додано до кошика.")
    return redirect("cart_detail")


def cart_detail(request):
    items, total = get_cart_items(request)
    return render(request, "cart.html", {"items": items, "total": total, "order_form": OrderForm()})


def get_cart_items(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys())
    items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        item_total = product.price * quantity
        total += item_total
        items.append({"product": product, "quantity": quantity, "total": item_total})
    return items, total


def create_order(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.warning(request, "Кошик порожній.")
        return redirect("catalog")
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user if request.user.is_authenticated else None
        order.save()
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart[str(product.id)],
                price=product.price,
            )
        request.session["cart"] = {}
        messages.success(request, "Замовлення оформлено.")
        return redirect("profile" if request.user.is_authenticated else "home")
    items, total = get_cart_items(request)
    return render(request, "cart.html", {"items": items, "total": total, "order_form": form})


def about(request):
    return render(request, "about.html")


def contacts(request):
    return render(request, "contacts.html")


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Реєстрація успішна.")
        return redirect("profile")
    return render(request, "register.html", {"form": form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            login(request, user)
            return redirect("profile")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    orders = Order.objects.all() if request.user.is_staff else request.user.orders.all()
    return render(request, "profile.html", {"orders": orders})


def password_reset_request(request):
    form = PasswordResetRequestForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            code = str(random.randint(100000, 999999))
            PasswordResetCode.objects.create(user=user, code=code)
            send_mail(
                "Код для відновлення пароля",
                f"Ваш тимчасовий код: {code}",
                None,
                [email],
            )
        messages.info(request, "Якщо email існує, код відправлено.")
        return redirect("password_reset_confirm")
    return render(request, "password_reset.html", {"form": form})


def password_reset_confirm(request):
    form = PasswordResetConfirmForm(request.POST or None)
    if form.is_valid():
        user = User.objects.filter(email=form.cleaned_data["email"]).first()
        reset_code = None
        if user:
            reset_code = user.reset_codes.filter(code=form.cleaned_data["code"], is_used=False).last()
        if reset_code:
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            reset_code.is_used = True
            reset_code.save()
            messages.success(request, "Пароль змінено. Тепер можна увійти.")
            return redirect("login")
        messages.error(request, "Неправильний або використаний код.")
    return render(request, "password_reset_confirm.html", {"form": form})
