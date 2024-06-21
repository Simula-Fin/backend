from fastapi import status
from httpx import AsyncClient
import pytest
from app.main import app
from app.tests.conftest import (
    default_user_email,
    default_user_id,
    default_user_monthly_income,
    default_user_name,
    default_user_telephone,
    default_user_cpf,
    default_user_birth_date_string,
    default_user_pix_key,
    default_user_is_admin,
)

@pytest.mark.asyncio
async def test_read_current_user_status_code(
    client: AsyncClient, default_user_headers: dict[str, str]
) -> None:
    response = await client.get(
        app.url_path_for("read_current_user"),
        headers=default_user_headers,
    )

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_read_current_user_response(
    client: AsyncClient, default_user_headers: dict[str, str]
) -> None:
    response = await client.get(
        app.url_path_for("read_current_user"),
        headers=default_user_headers,
    )

    assert response.json() == {
        "user_id": default_user_id,
        "email": default_user_email,
        'telephone': default_user_telephone,
        'monthly_income': default_user_monthly_income,
        'cpf': default_user_cpf,
        'birth_date': default_user_birth_date_string,
        'pix_key': default_user_pix_key,
        'name': default_user_name,
        'is_admin': default_user_is_admin,
    }

    