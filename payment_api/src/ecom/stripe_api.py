import logging
import time
from typing import List, Tuple

import stripe

from ecom.abstract import EcomClient
from schema.payment import RefundReason
from schema.product import Product

logger = logging.getLogger(__name__)

api_client = None


class StripeClient(EcomClient):
    """Implement Stripe API request and proccess the results."""

    def __init__(self, secret_key: str, method_types: List[str], session_expires_in: int) -> None:
        stripe.api_key = secret_key
        self.method_types = method_types
        self.session_expires_in = session_expires_in

    async def create_checkout_session(
        self,
        product: Product,
        success_redirect: str,
        cancel_redirect: str,
        idempotency_key: str = None,
    ) -> Tuple[str, str, str]:
        """Create checkout session.

            Args:
                product :  product details.
                success_redirect: URL after payment was successfully completed.
                cancel_redirect: URL after payment was cancelled.
                idempotency_key: Allow to escape duplications.

            Returns:
                tuple[str, str, str]: Session id, Payment intent id, Session URL.
        """
        price_data = product.dict()
        checkout_session = stripe.checkout.Session.create(
            success_url=success_redirect + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_redirect,
            payment_method_types=self.method_types,
            mode="payment",
            expires_at=int(time.time() + self.session_expires_in),
            line_items=[
                {
                    'quantity': 1,
                    'price_data': price_data,
                },
            ],
            idempotency_key=idempotency_key
        )
        logger.info(
            'Session id %s created, payment_intent %s price_data %s',
            checkout_session.id,
            checkout_session.payment_intent,
            price_data,
        )
        return checkout_session.id, checkout_session.payment_intent, checkout_session.url

    async def create_customer(self, name: str, email: str, idempotency_key: str = None) -> int:
        customer = stripe.Customer.create(name=name, email=email, idempotency_key=idempotency_key)
        logger.info('Customer %s created id ', customer.email, customer.id)
        return customer.id

    async def refund(self,
                     payment_intent: str,
                     amount: int = None,
                     reason: RefundReason = None,
                     idempotency_key: str = None
                     ) -> Tuple[str, str]:
        refund = stripe.Refund.create(
            amount=amount,
            payment_intent=payment_intent,
            reason=reason,
            idempotency_key=idempotency_key,
        )
        logger.info(
            'Refund created: payment %s, amount %s, reason %s, charge %s',
            payment_intent,
            amount,
            reason,
            refund.charge,
        )
        return refund.id, refund.charge


def get_client() -> EcomClient:
    return api_client
