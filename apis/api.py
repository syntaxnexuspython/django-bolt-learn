from django_bolt import BoltAPI, JSON
from .schemas import (
    ProductSchema,
    ProductResponseSchema,
    OrderProductSchema,
    OrderResponseSchema,
)
from .models import Product, Order
from asgiref.sync import sync_to_async

api = BoltAPI()

@api.get('/')
async def root():
    return JSON({"hello": "world"})


@api.post("/products", tags=["Product"])
async def create_product(product: ProductSchema) -> ProductResponseSchema:
    try:
        product = await Product.objects.acreate(
            name=product.name,
            description=product.description,
            price=product.price,
            user_id=product.user_id,
        )
        product = await Product.objects.prefetch_related("user").aget(id=product.id)
        return ProductResponseSchema(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            user_id=product.user_id,
            user={"username": product.user.username, "email": product.user.email},
        )
    except Exception as e:
        return JSON({"error": str(e)})


@api.get("/products", tags=["Product"])
async def get_products() -> list[ProductResponseSchema]:
    try:
        products = await sync_to_async(list)(
            Product.objects.select_related("user").all()
        )
        return [
            ProductResponseSchema(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                user_id=product.user_id,
                user={"username": product.user.username, "email": product.user.email},
            )
            for product in products
        ]
    except Exception as e:
        print(e)
        return []


@api.get("/products/{product_id}", tags=["Product"])
async def get_product(product_id: int) -> ProductResponseSchema:
    try:
        product = await Product.objects.prefetch_related("user").aget(id=product_id)
        return ProductResponseSchema(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            user_id=product.user_id,
            user={"username": product.user.username, "email": product.user.email},
        )
    except Exception as e:
        return JSON({"error": str(e)})


@api.post("/orders", tags=["Order"])
async def create_order(order: OrderProductSchema) -> OrderProductSchema:
    try:
        order = await Order.objects.acreate(
            product_id=order.product_id,
            quantity=order.quantity,
            user_id=order.user_id,
            price=order.price,
        )
        return OrderProductSchema(
            product_id=order.product_id,
            quantity=order.quantity,
            user_id=order.user_id,
            price=order.price,
        )
    except Exception as e:
        return JSON({"error": str(e)})


@api.get("/orders/users/{user_id}", tags=["Order"])
async def get_orders(user_id: int) -> list[OrderResponseSchema]:
    try:
        orders = await sync_to_async(list)(
            Order.objects.select_related("user", "product").filter(user_id=user_id)
        )
        return [
            OrderResponseSchema(
                id=order.id,
                product={
                    "id": order.product.id,
                    "name": order.product.name,
                    "description": order.product.description,
                    "price": order.product.price,
                    "user_id": order.product.user_id,
                },
                product_id=order.product_id,
                price=order.price,
                quantity=order.quantity,
                user_id=order.user_id,
                user={"username": order.user.username, "email": order.user.email},
            )
            for order in orders
        ]
    except Exception as e:
        print(e)
        return JSON({"error": str(e)})


@api.get("/orders/{order_id}", tags=["Order"])
async def get_order(order_id: int) -> OrderResponseSchema:
    try:
        order = await Order.objects.prefetch_related("user", "product").aget(
            id=order_id
        )
        return OrderResponseSchema(
            id=order.id,
            product={
                "id": order.product.id,
                "name": order.product.name,
                "description": order.product.description,
                "price": order.product.price,
                "user_id": order.product.user_id,
            },
            product_id=order.product_id,
            price=order.price,
            quantity=order.quantity,
            user_id=order.user_id,
            user={"username": order.user.username, "email": order.user.email},
        )
    except Exception as e:
        return JSON({"error": str(e)})
