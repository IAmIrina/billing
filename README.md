
# Project work "Billing for Online cinema". 
Yandex Praktikum:  Graduate work, teamwork.

Billing service for "Online cinema" charges user accounts using https://stripe.com/ API, adds or removes subscriptions and notify users about changes.

Components:
- Payment API allows charging user account using Stripe API and send information about transaction to queue of Payment Manager.
- Payment Manager processes events from its queue and add or remove subscriptions and send data to Notification service to notify users about the changes.
- Scheduler checks statuses of payments and removes overdue subscriptions or prolongs them.


## Stack
- FastAPI
- Redis
- Postgres
- Alembic
- Nginx


## Dev API сервиса
API of the service http://localhost:8090/api/openapi

## Deploy

1. Create file **.env** (use example **.env.example**)
2. Run docker-compose
```commandline
docker-compose -f docker-compose.dev.yml up --build
```
