from datetime import datetime

from lesson_2 import ProductEntity, get_all, add, ProductCreateReq, ProductUpdateReq, upd, pop

from fastapi import FastAPI

app = FastAPI()


@app.get("/get_all")
async def api_get_all(limit: int, offset: int, order_by: str):
    return get_all(limit=limit, offset=offset, order_by=order_by)


@app.post("/add")
async def api_add(product: ProductCreateReq):
    add(name=product.name, price=product.price, tag=product.tag, create_at=datetime.now())
    return product


@app.put("/update")
async def api_upd(index: int, product: ProductUpdateReq):
    upd(index=index, schema={
        "name": product.name,
        "price": product.price,
        "tag": product.tag,
        "create_at": datetime.now()
    })
    return None


@app.delete("/delete")
async def api_del(index: int):
    pop(index)
    return None
