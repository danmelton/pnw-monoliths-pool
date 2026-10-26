from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="app2", version="1.0.0")


class ItemIn(BaseModel):
    name: str


class Item(BaseModel):
    id: int
    name: str


items: dict[int, Item] = {}
next_id = 1


def find(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.get("/items")
def list_items() -> list[Item]:
    return list(items.values())


@app.post("/items", status_code=201)
def create_item(body: ItemIn) -> Item:
    global next_id
    item = Item(id=next_id, name=body.name)
    items[item.id] = item
    next_id += 1
    return item


@app.get("/items/{item_id}")
def read_item(item_id: int) -> Item:
    return find(item_id)


@app.put("/items/{item_id}")
def update_item(item_id: int, body: ItemIn) -> Item:
    item = find(item_id)
    item.name = body.name
    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> Item:
    return items.pop(find(item_id).id)
