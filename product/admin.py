from django.contrib import admin

from product.models import Book, Author, Publisher


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)