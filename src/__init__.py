import uvicorn
from books.routes import book_router
from fastapi import FastAPI

app = FastAPI(title="Book App API",
             description="A simple API for managing books",
             version="1.0.0")

app.include_router(book_router, prefix="/api/v1", tags=["books"])

def main():
    print("Hello from bookapp-fastapi!")
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")


if __name__ == "__main__":
    main()
