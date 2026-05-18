from pydantic import BaseModel
from typing import Optional

class StockResponse(BaseModel):
    stock_code: str
    stock_name: str
    category: Optional[str] = None
    industry: Optional[str] = None
    market: Optional[str] = None
