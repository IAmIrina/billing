from abc import ABC, abstractmethod
from typing import Tuple

from schema.payment import CancelReason, PaymentEvent, RefundReason
from schema.product import Product


class EcomClient(ABC):

    @property
    @abstractmethod
    def public_key(self):
        pass

    @abstractmethod
    async def create_customer(self, name: str, email: str, idempotency_key: str = None) -> str:
        """Create customer on ecom side.

            Args:
                name: Name of customer,
                email: Email of customer,
                idempotency_key: Allow to escape duplications.

            Returns:
                str: customer id on ecom side
        """
        pass

    @abstractmethod
    async def create_payment_intent(
        self,
        customer_id: str,
        product: Product,
        idempotency_key: str = None,
    ) -> Tuple[str, str]:
        """Create payment intent.

            Args:
                product :  product details.
                idempotency_key: Allow to escape duplications.

            Returns:
                Tuple[str, str]: Payment id, Client secret.
        """
        pass

    @abstractmethod
    async def cancel_payment_intent(
        self,
        payment_intent: str,
        reason: CancelReason = None,
        idempotency_key: str = None
    ) -> None:
        """Cancel payment intent.

            Args:
                payment_intent :  payment_intent id.
                reason: The reason of cancellation.
                idempotency_key: Allow to escape duplications.

        """
        pass

    @abstractmethod
    async def charge(self,
                     customer_id: str,
                     product: Product,
                     idempotency_key: str = None
                     ) -> str:
        """Charge client.

            Args:

                customer_id :  Customer to charge.
                product: Product data.
                idempotency_key: Allow to escape duplications.

            Returns:
                str: PaymentIntent id.
        """
        pass

    @abstractmethod
    async def refund(self,
                     payment_intent: str,
                     amount: int = None,
                     reason: RefundReason = None,
                     idempotency_key: str = None
                     ) -> str:
        """Refund payment.

            Args:

                payment_intent :  Refund payment.
                amount: Refund amount.
                reason: Refund reasin.
                idempotency_key: Allow to escape duplications.

            Returns:
                str: Cahrge id.
        """
        pass


class EcomEventParser(ABC):
    @abstractmethod
    async def parse(self, payload: bytes, headers: dict) -> PaymentEvent:
        """Parse webhook event.
            Args:
                payload: Event payload.
                headers: Event headers.

            Returns:
                PaymentEvent: Object that represent parsed webhook event.
        """
        pass
