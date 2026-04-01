from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Query
from sqlalchemy import and_, select
from models.sale import SaleAddSchema
from services.storage import SessionDep, SaleModel


router = APIRouter()


@router.post('/sales')
async def add_sales(sales: List[SaleAddSchema], session: SessionDep):
    new_sales = []
    for sale in sales:
        new_sale = SaleModel( 
            marketplace = sale.marketplace,
            product_name = sale.product_name,
            quantity = sale.quantity,
            price = sale.price,
            cost_price = sale.cost_price,
            status = sale.status,
            sold_at = sale.sold_at
        )
        new_sales.append(new_sale)
        
        
    session.add_all(new_sales)
    await session.commit()
    return {'ok': True, 'msg': f'количество строк: {len(new_sales)}, {len(new_sales)}'}



@router.get('/sales')
async def get_sales(session: SessionDep,
    marketplace: Optional[str] = Query(None, description="Фильтр по маркетплейсу"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    date_from: Optional[datetime] = Query(None, description="Начало диапазона дат"),
    date_to: Optional[datetime] = Query(None, description="Конец диапазона дат"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы")
):
    query = select(SaleModel)

    conditions = []

    if marketplace:
        conditions.append(SaleModel.marketplace == marketplace)
    if status:
        conditions.append(SaleModel.status == status)
    if date_from:
        conditions.append(SaleModel.sold_at >= date_from)
    if date_to:
        conditions.append(SaleModel.sold_at <= date_to)


    if conditions:
        query = query.where(and_(*conditions))

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await session.execute(query)
    sales = result.scalars().all()

    return sales