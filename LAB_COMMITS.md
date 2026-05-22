# Структура комітів для лабораторних

Через поточний збій запуску локальної оболонки коміти не були створені автоматично. Щоб структура відповідала вимогам, зробіть коміти в такому порядку:

```bash
git init
git add manage.py phone_store requirements.txt .gitignore README.md shop/oop_demo.py
git commit -m "Lab 2: create Django project and OOP task"

git add shop templates
git commit -m "Lab 3: add shop app templates and navigation"

git add shop/models.py shop/admin.py shop/migrations
git commit -m "Lab 4: add shop models and admin"

git add templates/home.html templates/base.html static
git commit -m "Lab 5: build homepage layout with database products"

git add templates/category_detail.html templates/product_detail.html shop/views.py shop/urls.py
git commit -m "Lab 6: add product and category pages"

git add templates/cart.html shop/forms.py
git commit -m "Lab 7: add cart newsletter and product ratings"

git add templates/login.html templates/register.html templates/profile.html templates/password_reset.html templates/password_reset_confirm.html
git commit -m "Lab 8: add authentication profile password reset and DRY templates"
```

Після цього створіть новий GitHub-репозиторій і підключіть його:

```bash
git remote add origin YOUR_REPOSITORY_URL
git branch -M main
git push -u origin main
```
