from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("order/create/", views.create_order, name="create_order"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("password-reset/", views.password_reset_request, name="password_reset"),
    path("password-reset/confirm/", views.password_reset_confirm, name="password_reset_confirm"),
]
