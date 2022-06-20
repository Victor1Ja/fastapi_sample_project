from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:300'],
    allow_methods=['*'],
    allow_headers=['*'],


)

redis = get_redis_connection(
    host="redis-15259.c85.us-east-1-2.ec2.cloud.redislabs.com",
    port=15259,
    password="GUy8YnRpBgy3xtMqhtBPQrpN3b2MRaq9",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity_available: int

    class Meta:
        database = redis


@app.get("/products")
def get_products():
    return [Product.get(pk) for pk in Product.all_pks()]


def format(pk: str):
    # product = Product.get(pk)
    # return {
    #     'id':product.pk,
    #     'name':product.name,
    #     'price':product.price,
    #     'quantity':product.quantity_available
    # }
    return Product.get(pk)

@app.post("/products")
def create_product(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get_product(pk:str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete_product(pk:str):
    return Product.delete(pk)
     


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
