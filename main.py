from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def root():
    return {
        'message': 'Hello World'
    }


def main():
    print("Hello from bookapp-fastapi!")
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
