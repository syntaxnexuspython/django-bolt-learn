import msgspec

class UserSchema(msgspec.Struct):
    username: str
    email: str

class ProductSchema(msgspec.Struct):
    name: str
    description: str
    price: float
    user_id: int

class ProductResponseSchema(ProductSchema):
    id: int
    user: UserSchema
    

class OrderProductSchema(msgspec.Struct):
    product_id: int
    quantity: int
    user_id:int
    price: float

class OrderResponseSchema(OrderProductSchema):
    id: int
    product: ProductSchema
    user: UserSchema