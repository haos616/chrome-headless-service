import sys

from typing import List, Optional
from fastapi import FastAPI, Depends
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from containers import Container
from services.chrome_headless import ChromeHeadlessService

app = FastAPI()


class MethodResource(BaseModel):
    method: str
    params: Optional[dict]


@app.post('/')
@inject
async def index(
    method_resources: List[MethodResource],
    chrome_headless_service: ChromeHeadlessService = Depends(Provide[Container.chrome_headless_service]),
):
    return await chrome_headless_service.execute(method_resources=method_resources)

container = Container()
# container.config.http_redis_cache.from_pydantic(HttpRedisCacheSettings())
container.wire(modules=[sys.modules[__name__]])
