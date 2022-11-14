from abc import ABC, abstractmethod
from typing import Tuple

from schema.product import Product


class EcomClient(ABC):

    @abstractmethod
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
        pass

    @abstractmethod
    async def refund(
            self,
            payment_intent: str,
            amount: int = None,
            reason: str = None,
            idempotency_key: str = None) -> Tuple[str, str]:
        """Refund payment.

            Args:
                payment_intent :  Payment to refund.
                amount: Amount of money to refund in cents.
                reason: Reason of refund.
                idempotency_key: Unique transiction id.

            Returns:
                tuple[str, str]:Refund id, Charge id.
        """
        pass

    @abstractmethod
    async def create_customer(self, name: str, email: str, idempotency_key: str = None) -> str:
        """Create customer.

            Args:
                name :  Customer name.
                email: Customer email.
                idempotency_key: Unique transiction id.

            Returns:
                str: Customer id in merchant.
        """
        pass
