from fastapi import FastAPI

from app.routes import product, cart, order, user

app = FastAPI()

app.include_router(product.router)
app.include_router(cart.router)
app.include_router(user.router)
app.include_router(order.router)
