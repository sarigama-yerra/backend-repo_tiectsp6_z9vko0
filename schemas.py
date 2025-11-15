"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Marketing/demo examples kept for reference
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in PKR")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Al Rehman Biryani specific schemas

class DaigOrder(BaseModel):
    name: str = Field(..., description="Customer full name")
    phone: str = Field(..., min_length=7, max_length=20, description="Contact number")
    quantity: str = Field(..., description="Daig size or number of plates/servings")
    address: str = Field(..., description="Delivery address in Karachi")
    notes: Optional[str] = Field(None, description="Special instructions or occasion")
    preferred_time: Optional[str] = Field(None, description="Preferred delivery date/time")
    source: Optional[str] = Field("website", description="Lead source e.g., website/whatsapp/call")

class Inquiry(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    message: str

class Review(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    source: Optional[str] = Field(None, description="Platform e.g., Google, Foodpanda")
    photo_url: Optional[str] = None

class Branch(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    hours: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    areas: Optional[List[str]] = None
