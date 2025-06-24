from uuid import uuid4
from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()

@app.get('/')
async def root():
    return {
        'message': 'Hello World'
    }
    
@app.get('/{name}')
async def root_hello(name:str) -> dict:
    return {
        'message': f"Hello {name}"
    }

@app.get('/name')
async def root_hello_name(name:str, age:Optional[int] = 5) -> dict:
    return {
        'message': f"Hello {name}, You age is {age}"
    }
    
class Testpayload(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str = Field(...,min_length=5, max_length=50)
    age: Optional[int] = 5
    
@app.post('/name')
async def root_hello_name(payload: Testpayload, 
                            custom: Optional[str] = Header(None, alias="Hello-Header")  # Read custom header here
                          ) -> dict:
    return {
        'message': f"Hello {payload.name}, You age is {payload.age}, and id {payload.id}",
        'custom_header': custom
    }


def main():
    print("Hello from bookapp-fastapi!")
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
