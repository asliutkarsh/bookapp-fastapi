from src.books.routes import book_router
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.auth.routes import auth_router
from src.error import register_all_errors

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    from src.db.main import init_db
    print("Initializing the database...")
    await init_db()
    print("Database initialized.")
    yield
    print("Shutting down the application...")


app = FastAPI(title="Book App API",
             description="A simple API for managing books",
             version="1.0.0",
             lifespan=lifespan
             )

register_all_errors(app)

app.include_router(book_router, prefix="/api/v1", tags=["Books"])
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
