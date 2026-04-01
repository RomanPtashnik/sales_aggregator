from pydantic import BaseModel, Field, field_validator
from datetime import date

from services.storage import SaleModel


class SaleAddSchema(BaseModel):
    order_id: str
    marketplace: str
    product_name:str
    quantity: int = Field(ge=1)
    price: float = Field(gt=0)
    cost_price: float = Field(gt=0)
    status: str
    sold_at: date
    
    model_config = {"from_attributes": True}
    
    
    @field_validator("marketplace")
    @classmethod
    def check_data(cls, v: str):
        mark = ['ozon','wildberries','yandex_market']
        if v not in  mark:
            raise ValueError("не допустимые значения")
        return v 
    
    
    @field_validator("sold_at")
    @classmethod
    def check_date(cls, v: date):
        if v > date.today():
            raise ValueError("Дата продажи не может быть в будущем")
        return v    


class SaleSchema(SaleAddSchema):
    id: int
