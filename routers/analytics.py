from datetime import datetime
import io
from typing import List, Optional

from fastapi import APIRouter, Query, File, UploadFile
import pandas as pd
from models.sale import SaleAddSchema, SaleSchema
from models.analytics import returned_metrics
from services.storage import SaleModel, SessionDep
from services.aggregation import aggregation


router = APIRouter()

@router.get('/analytics')
def Aggregated_metrics():
    pass


@router.get('/analytics/summary')
def summary_metrics(analytics: returned_metrics):
    pass


@router.get('/analytics/top-products')
def top_products_metrics(session: SessionDep,
    date_from: Optional[datetime] = Query(None, description="Начало диапазона дат"),
    date_to: Optional[datetime] = Query(None, description="Конец диапазона дат"),
    sort_by: Optional[datetime] = Query(default='revenue', description="Конец диапазона дат")
):
    pass



@router.get('/analytics/summary-usd')
def summary_usd_metrics():
    pass


@router.post('/analytics/upload-csv')
async def upload_csv_metrics(session: SessionDep, uploaded_file: UploadFile = File(...)):
    contents = await uploaded_file.read()
    df = pd.read_csv(io.BytesIO(contents))
    result = aggregation(df)
    
    new_sales = []
    for rec in result:
        if 'sold_at' in rec and rec['sold_at']:
            rec['sold_at'] = datetime.strptime(rec['sold_at'], '%Y-%m-%d').date()
        rec.pop('order_id', None)
        new_sale = SaleModel(**rec)
        new_sales.append(new_sale)

    session.add_all(new_sales)
    await session.commit()

    return {'ok': True, 'msg': f'Продажи добавлены в количестве: {len(new_sales)}'}