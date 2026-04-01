from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import APIRouter, Depends

from datetime import date


router = APIRouter()


engine = create_async_engine('sqlite+aiosqlite:///database.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with  new_session() as session:
        yield session
        

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class SaleModel(Base):
    __tablename__ = 'SaleModel'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    marketplace: Mapped[str]
    product_name: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[float]
    cost_price: Mapped[float]
    status: Mapped[str]
    sold_at: Mapped[date]
    
    @property
    def order_id(self) -> str:
        return f"ORD-{self.id:03d}"
    

@router.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
            
            

