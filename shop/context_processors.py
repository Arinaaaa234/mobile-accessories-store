from .models import Category


def catalog_categories(request):
    return {"menu_categories": Category.objects.all()}


def cart_counter(request):
    cart = request.session.get("cart", {})
    return {"cart_count": sum(cart.values())}
