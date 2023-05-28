from fastapi import FastAPI, Request
import uvicorn
import argparse
from model import predict
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    sku: str
    count: int
    size1: str
    size2: str
    size3: str
    weight: str
    type: List[str]

class Order(BaseModel):
    orderId: str
    items: List[Item]

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/pack")
def get_prediction(request: Order):
    items = []
    for el in request.items:
        items.append(el.dict())

    y = predict(items)
    return {"orderId": request.orderId,
            "package": y,
            "status": "ok"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    parser.add_argument("--debug", action="store_true", dest="debug")
    args = vars(parser.parse_args())

    uvicorn.run(app, **args)
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)