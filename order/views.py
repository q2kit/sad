from django.http import JsonResponse, HttpResponse

from order.models import Order, Item
from product.models import Book
from user.models import User

from user.decorator.permission import login_required


@login_required
def add_to_cart(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Book does not exist'
        }, status=404)

    try:
        item = Item.objects.get(book=book, user=request.user, order=None)
        item.quantity += 1
        item.save()
    except Item.DoesNotExist:
        item = Item.objects.create(book=book, user=request.user)

    return JsonResponse({
        'success': True,
        'message': 'Book added to cart successfully'
    })


@login_required
def cart(request):
    items = Item.objects.filter(user=request.user, order=None).values(
        'id', 'book_id', 'book__title', 'book__price', 'book_description', 'quantity'
    )
    total_price = sum([item['book__price'] * item['quantity'] for item in items])
    return JsonResponse({
        'success': True,
        'items': list(items),
        'total_price': total_price
    })


@login_required
def remove_from_cart(request, book_id):
    try:
        item = Item.objects.get(book_id=book_id, user=request.user, order=None)
        item.delete()
    except Item.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Item does not exist'
        }, status=404)

    return JsonResponse({
        'success': True,
        'message': 'Book removed from cart successfully'
    })


@login_required
def checkout(request):
    try:
        order = Order.objects.create(user=request.user)
        items = Item.objects.filter(user=request.user, order=None)
        for item in items:
            item.order = order
            order.total_price += item.book.price * item.quantity
        else:
            order.delete()
            return JsonResponse({
                'success': False,
                'message': 'Cart is empty'
            }, status=400)
        Item.objects.bulk_update(items, ['order'])
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).values(
        'id', 'created_at', 'status', 'total_price'
    )
    return JsonResponse({
        'success': True,
        'orders': list(orders)
    })


@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order does not exist'
        }, status=404)

    items = Item.objects.filter(order=order).values(
        'id', 'book_id', 'book__title', 'book__price', 'book_description', 'quantity'
    )
    return JsonResponse({
        'success': True,
        'order': {
            'id': order.id,
            'created_at': order.created_at,
            'status': order.status,
            'total_price': order.total_price
        },
        'items': list(items)
    })