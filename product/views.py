from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from user.decorator.permission import *
from product.models import *


@csrf_exempt
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


@csrf_exempt
@admin_required
def author(request):
    try:
        name = request.POST.get("name")
        if not name or Author.objects.filter(name=name).exists():
            return JsonResponse({
                "success": False,
                "message": "Author already exists",
            })

        author = Author.objects.create(name=name)
        return JsonResponse({
            "success": True,
            "message": "Author added successfully",
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Error occurred",
        })


@csrf_exempt
@admin_required
def publisher(request):
    try:
        name = request.POST.get("name")
        if not name or Publisher.objects.filter(name=name).exists():
            return JsonResponse({
                "success": False,
                "message": "Publisher already exists",
            })

        publisher = Publisher.objects.create(name=name)
        return JsonResponse({
            "success": True,
            "message": "Publisher added successfully",
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Error occurred",
        })
