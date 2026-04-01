from contextlib import asynccontextmanager

from fastapi import FastAPI
from routers import sales, analytics
from services import storage
from services.storage import engine, Base
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при запуске приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закрываем соединения при завершении (опционально)
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(sales.router)
app.include_router(analytics.router)
app.include_router(storage.router)


if __name__ == '__main__':
    
    uvicorn.run("main:app", reload=True)