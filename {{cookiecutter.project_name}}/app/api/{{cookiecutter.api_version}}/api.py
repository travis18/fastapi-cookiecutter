# import api in endpoints folder and include them in this file
# example as below
"""
```
from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, utils, shops, rptgen, shop_items, configs
from app.api.api_v1.endpoints.rakuten import orders

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(shops.router, prefix="/shops", tags=["shops"])
api_router.include_router(rptgen.router, prefix="/report_record", tags=["report_record"])
api_router.include_router(orders.router, prefix="/rakuten/searchOrder", tags=["rakuten/orders"])
api_router.include_router(shop_items.router, prefix="/products", tags=["shop_items", "products"])
api_router.include_router(configs.router, prefix="/configs", tags=["configs"])
```
"""