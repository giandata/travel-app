# main.py

from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
import datetime

class Item(BaseModel):
    starting_country: str
    starting_city: str
    starting_date: datetime.date
    duration: int
    selected_countries: List[str]
    travel_budget: Optional[tuple] = None
    travel_type: Optional[str] = None
    setting_flex: Optional[bool] = None
    setting_night: Optional[bool] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    return item_dict