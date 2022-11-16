"""Stripe webhook event parser."""
import logging
from typing import Tuple

import orjson
import stripe

from ecom.abstract import EcomEventParser
from schema.payment import (CompletedSession, Event, ExpiredSession,
                            PaymentEvent, RefundedCharge)

logger = logging.getLogger(__name__)

event_parser = None


class StripeEventParser(EcomEventParser):
    """Handle Strike Webhook requests."""

    def __init__(self, endpoint_secret: str) -> None:
        self.endpoint_secret = endpoint_secret

    async def _checkout_session_completed(self, event: dict) -> CompletedSession:
        completed_session_data = CompletedSession(
            session_id=event.data.object.id,
            payment_intent=event.data.object.payment_intent
        )
        return completed_session_data

    async def _charge_refunded(self, event: dict) -> RefundedCharge:
        charge = event.data.object
        refunded_charge = RefundedCharge(
            charge_id=charge.id,
            payment_intent=charge.payment_intent,
        )
        return refunded_charge

    async def _checkout_session_expired(self, event: dict) -> ExpiredSession:
        return ExpiredSession(session_id=event.data.object.id)

    async def _get_event(self, payload: bytes, headers: dict) -> Tuple[str, dict]:
        try:
            stripe_signature = headers['stripe-signature']
        except KeyError as e:
            logger.warning("Header stripe_signature doesn't exist %s", headers)
            raise e
        try:
            event = stripe.Webhook.construct_event(
                payload, stripe_signature, self.endpoint_secret
            )
        except ValueError as e:
            logger.warning('Invalid payload %s', payload)
            raise e
        except stripe.error.SignatureVerificationError as e:
            logger.warning('Invalid signature %s', payload)
            raise e
        return event['type'], event

    async def parse(self, payload: bytes, headers: dict) -> PaymentEvent:
        event_type, event = await self._get_event(payload=payload, headers=headers)
        logger.info('Handled event type %s', event_type)
        try:
            event_handler = getattr(self, f"_{Event(event_type).name}")
        except (ValueError, AttributeError):
            logger.warning('Unhandled event type %s', event_type)
            return None
        event_data = await event_handler(event)
        return PaymentEvent(type=event_type, data=event_data, row_data=orjson.loads(payload))


def get_event_parser() -> EcomEventParser:
    return event_parser
