import os
from fastapi import FastAPI, Query
from pydantic import BaseModel

from server import make_greeting


class HelloRequest(BaseModel):
    name: str


app = FastAPI(title="Greeter HTTP Bridge", version="1.0.0")


@app.get("/")
def root():
    return {
        "service": "greeter",
        "endpoints": [
            {"GET": "/hello?name=TuNombre"},
            {"POST": "/hello"},
        ],
    }


@app.get("/hello")
def hello_get(name: str = Query(..., description="Nombre a saludar")):
    return {"message": make_greeting(name)}


@app.post("/hello")
def hello_post(payload: HelloRequest):
    return {"message": make_greeting(payload.name)}


if __name__ == "__main__":
    # Local run helper: uvicorn app:app --reload
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)

