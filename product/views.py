from django.http import JsonResponse, HttpResponse

from user.decorator.permission import *
from product.models import Book


@admin_required
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        publisher_id = request.POST.get("publisher_id")
        author_id = request.POST.get("author_id")
        book = Book.objects.create(
            title=title,
            description=description,
            price=price,
            publisher_id=publisher_id,
            author_id=author_id
        )
        return JsonResponse({
            "success": True,
            "message": "Book added successfully",
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "Only POST method allowed",
        })


@login_required
def get_books(request):
    books = Book.objects.all()
    author_id = request.GET.get("author_id")
    publisher_id = request.GET.get("publisher_id")
    if author_id:
        books = books.filter(author_id=author_id)
    if publisher_id:
        books = books.filter(publisher_id=publisher_id)

    return JsonResponse({
        "success": True,
        "message": "Books retrieved successfully",
        "books": list(books.values())
    })