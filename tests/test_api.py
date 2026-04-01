import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_get_sales():
    async with AsyncClient(transport=ASGITransport(app=app),
                        base_url='http://test',
    ) as ac:
        responce = await ac.get('/sales')
        assert responce.status_code == 200
        data = responce.json()
        assert len(data) > 0 
        
        
@pytest.mark.asyncio
async def test_add_sales():
    async with AsyncClient(transport=ASGITransport(app=app),
                        base_url='http://test',
    ) as ac:
        responce = await ac.post('/sales', json=
            [
            {
                "order_id": "ORD-001",
                "marketplace": "ozon",
                "product_name": "Кабель USB-C",
                "quantity": 3,
                "price": 450.00, 
                "cost_price": 120.00, 
                "status": "delivered", 
                "sold_at": "2025-03-15"
            }
        ])
        assert responce.status_code == 200
        data = responce.json()
        assert data ==  {'ok': True, 'msg': 'количество строк: 1, 1'}