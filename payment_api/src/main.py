import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import payments, subscriptions
from core.config import settings
from ecom import stripe_api
from services.payment_manager import PaymentManager
from services.data_enricher import DataEnricher
from services.role_updater import RoleUpdater

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    stripe_api.api_client = stripe_api.StripeClient(
        secret_key=settings.stripe.secret_key.get_secret_value(),
        method_types=settings.payment.method_types,
        public_key=settings.stripe.public_key.get_secret_value(),
    )


@app.on_event('shutdown')
async def shutdown():
    ...


app.include_router(payments.router, prefix='/api/v1/payment', tags=['payment'])
app.include_router(subscriptions.router, prefix='/api/v1/subscription', tags=['subscription'])

# Инициализируем компоненты и сам объект, который будет обрабатывать оплаты
# enricher = DataEnricher(db_uri=settings.postgres.dsn)
# updater = RoleUpdater(
#     settings.auth.roles_url,
#     settings.auth.login_url,
#     settings.auth.superuser_email,
#     settings.auth.superuser_password,
# )
# manager = PaymentManager(
#     auth_updater=updater,
#     enricher=enricher,
#     model_to_process=PaymentToProcess
# )
# asyncio.run(manager.watch_payments())



if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=settings.uvicorn_reload,
        host='0.0.0.0',
        port=8080,
    )
