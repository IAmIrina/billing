from http import HTTPStatus

import pytest

import testdata.data
from tests.functional.settings import test_settings

pytestmark = pytest.mark.asyncio


async def test_add_subscriptions_by_admin(make_post_request):
    subscription = testdata.data.subscription
    headers = {f'Authorization': f'Bearer {testdata.data.superadmin_token}'}
    response = await make_post_request(
        endpoint=f'{test_settings.subscriptions_router_prefix}',
        body=subscription.__dict__,
        headers=headers
    )
    assert response.status == HTTPStatus.OK
    assert response.body == subscription.__dict__


async def test_add_subscriptions_by_user_forbidden(make_post_request):
    subscription = testdata.data.subscription
    headers = {f'Authorization': f'Bearer {testdata.data.user_token}'}
    response = await make_post_request(
        endpoint=f'{test_settings.subscriptions_router_prefix}',
        body=subscription.__dict__,
        headers=headers
    )
    assert response.status == HTTPStatus.FORBIDDEN


async def test_change_subscriptions_by_admin(make_patch_request):
    subscription = testdata.data.subscription
    subscription.price = 5000
    headers = {f'Authorization': f'Bearer {testdata.data.superadmin_token}'}

    response = await make_patch_request(
        endpoint=f'{test_settings.subscriptions_router_prefix}{subscription.title}',
        body=subscription.__dict__,
        headers=headers
    )
    assert response.status == HTTPStatus.OK
    assert response.body == subscription.__dict__
