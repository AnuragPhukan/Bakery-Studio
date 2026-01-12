from fastapi import FastAPI

from ui_routes_admin import router as admin_router
from ui_routes_assets import router as assets_router
from ui_routes_chat import router as chat_router
from ui_routes_public import router as public_router


app = FastAPI(title="Bakery Quotation UI")
app.include_router(public_router)
app.include_router(admin_router)
app.include_router(assets_router)
app.include_router(chat_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
