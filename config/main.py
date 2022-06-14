from fastapi import FastAPI, Depends, Body, UploadFile, File
from typing import Dict, Optional, List
from .settings import database, SECRET_KEY
from accounts import router as accountsRouter
from products import router as productsRouter
from carts import router as cartsRouter
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(accountsRouter.router)
app.include_router(productsRouter.router)
app.include_router(cartsRouter.router)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/image", StaticFiles(directory="media"), name="image")

app.state.database = database

@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
