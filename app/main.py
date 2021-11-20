from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth,category,product,depot,magasin,container,inventory,invoice,depense
from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(inventory.router)
app.include_router(category.router)
app.include_router(container.router)
app.include_router(product.router)
app.include_router(depot.router)
app.include_router(magasin.router)
app.include_router(invoice.router)
app.include_router(depense.router)
# app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
