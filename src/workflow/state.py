from typing import TypedDict,Literal
from pydantic import BaseModel, Field

class llmState(TypedDict):
    question :str
    answer:str
    product :str

class product_structural(BaseModel):
    product:str = Field(..., description="product to search for make is singular exampled 'pant' not 'pants' ")

class question_conditional(BaseModel):
    result: Literal["product", "company"]