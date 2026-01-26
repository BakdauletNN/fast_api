from fastapi import FastAPI, HTTPException, Query, Form
from pydantic import BaseModel
import uvicorn
from typing import Optional, List
from datetime import date


my_app = FastAPI()


@my_app.get("/hotels")
def ht(city: Optional[str], mx_p: Optional[int]):
    return {"city:":city, "price":mx_p}
