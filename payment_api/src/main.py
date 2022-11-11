import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import payments
from core.config import settings

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    ...


@app.on_event('shutdown')
async def shutdown():
    ...


app.include_router(payments.router, prefix='/api/v1/payment', tags=['payment'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=settings.uvicorn_reload,
        host='0.0.0.0',
        port=8080,
    )
