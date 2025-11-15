import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import db, create_document, get_documents
from schemas import DaigOrder, Inquiry, Review, Branch

app = FastAPI(
    title="Al Rehman Biryani API",
    description="API for menu, orders, reviews, branches, and inquiries",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Al Rehman Biryani API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "Unknown"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"

    return response

# ----- Menu Endpoints -----
class MenuItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    photo_url: Optional[str] = None
    category: str

@app.get("/api/menu", response_model=List[MenuItem])
def get_menu():
    # Static seed menu; in a real app, this could come from DB
    menu: List[MenuItem] = [
        MenuItem(name="Chicken Biryani (Plate)", description="Aromatic basmati rice, tender chicken, signature masala.", price=420, category="Chicken Biryani", photo_url="https://images.unsplash.com/photo-1606491956689-2ea866880c84?q=80&w=1200&auto=format&fit=crop"),
        MenuItem(name="Beef Biryani (Plate)", description="Slow-cooked beef with robust spices.", price=520, category="Beef Biryani", photo_url="https://images.unsplash.com/photo-1625944520878-2986441aa5fb?q=80&w=1200&auto=format&fit=crop"),
        MenuItem(name="Chicken Daig (20 ppl)", description="Perfect for small gatherings.", price=8500, category="Daigs", photo_url="https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1200&auto=format&fit=crop"),
        MenuItem(name="Chicken Daig (50 ppl)", description="Family events & mehndi.", price=18500, category="Daigs", photo_url="https://images.unsplash.com/photo-1544025162-36f6ad47d34f?q=80&w=1200&auto=format&fit=crop"),
        MenuItem(name="Raita (500ml)", description="Cooling mint raita.", price=250, category="Sides", photo_url="https://images.unsplash.com/photo-1606755456203-231e3d8ff4b8?q=80&w=1200&auto=format&fit=crop"),
        MenuItem(name="Kachumber Salad", description="Fresh onions, cucumbers, tomatoes.", price=250, category="Sides", photo_url="https://images.unsplash.com/photo-1526318472351-c75fcf070305?q=80&w=1200&auto=format&fit=crop"),
        MenuItem(name="Cold Drink 1.5L", description="Chilled soft drink bottle.", price=320, category="Drinks", photo_url="https://images.unsplash.com/photo-1554866585-cd94860890b7?q=80&w=1200&auto=format&fit=crop"),
    ]
    return menu

# ----- Daig Orders -----
@app.post("/api/orders/daig")
def create_daig_order(order: DaigOrder):
    try:
        order_id = create_document("daigorder", order)
        return {"status": "ok", "id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Reviews -----
@app.get("/api/reviews")
def list_reviews(limit: int = 20):
    try:
        reviews = get_documents("review", {}, limit)
        # Provide some seed reviews if DB empty
        if not reviews:
            reviews = [
                {"name": "Maham A.", "rating": 5, "comment": "Hands down the best Karachi biryani! Perfect spice.", "source": "Google"},
                {"name": "Ali R.", "rating": 5, "comment": "Ordered daig for mehndi. Fresh, hot, on time.", "source": "Foodpanda"},
                {"name": "Sana K.", "rating": 4, "comment": "Aroma is unreal. Beef is super tender.", "source": "Google"},
            ]
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Branches -----
@app.get("/api/branches")
def list_branches():
    try:
        branches = get_documents("branch", {})
        if not branches:
            branches = [
                {"name": "Saddar", "address": "Saddar, Karachi", "phone": "+92 300 1234567", "hours": "11am - 11pm", "lat": 24.853, "lng": 67.018, "areas": ["Saddar", "PECHS", "Garden"]},
                {"name": "Gulshan-e-Iqbal", "address": "Block 10, Gulshan-e-Iqbal", "phone": "+92 333 7654321", "hours": "11am - 11pm", "lat": 24.923, "lng": 67.089, "areas": ["Gulshan", "Gulistan-e-Johar", "Bahadurabad"]},
            ]
        return branches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Inquiries / Contact -----
@app.post("/api/inquiry")
def submit_inquiry(inquiry: Inquiry):
    try:
        inquiry_id = create_document("inquiry", inquiry)
        return {"status": "ok", "id": inquiry_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
