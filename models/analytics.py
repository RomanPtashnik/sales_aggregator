from pydantic import BaseModel, Field, field_validator
from datetime import date


from services.storage import SaleModel


class returned_metrics(BaseModel):
    pass
    total_revenue: float 
    total_cost: float 
    gross_profit: float 
    margin_percent: float 
    total_orders: int 
    avg_order_value: float 
    return_rate: float 
