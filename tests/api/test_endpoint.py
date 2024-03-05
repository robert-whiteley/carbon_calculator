import pytest
from httpx import AsyncClient
import os

test_params = '../../test_images/banana.jpg'

@pytest.mark.asyncio
async def test_predict_is_up():
    from carb_calc.api.fast import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/predict", crop_image=test_params)
    assert response.status_code == 200
