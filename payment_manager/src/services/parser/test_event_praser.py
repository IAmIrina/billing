import pytest

from ecom_parser import StripeEventParser
from test_data import test_intent_successfull, test_refund_successfull


@pytest.mark.asyncio
async def test_payment_successfull():
    result = await StripeEventParser().parse(event=test_intent_successfull)
    assert result.type.name == 'payment_intent_succeeded'
    assert result.data == {'payment_intent': 'pi_3M6wNMEUp1F2G8nC14lPOKbf',
                           'customer': 'cus_MqcgCDPrFBw2SV',
                           'status': 'succeeded'}


@pytest.mark.asyncio
async def test_refund_intent_successfull():
    result = await StripeEventParser().parse(event=test_refund_successfull)
    print(result.dict())
    assert result.type.name == 'charge_refunded'
    assert result.data == {
        'charge_id': 'ch_3M5WAbEUp1F2G8nC1U6euMUl',
        'payment_intent': 'pi_3M5WAbEUp1F2G8nC1jazccrX',
        'status': 'succeeded'}
