from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI(title="My API", version="1.0.0")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str


class StatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_products: int
    revenue: float
    metrics: dict


class UserService:
    def get_all(self) -> List[UserResponse]:
        data = [
            {"id": 1, "name": "Иван Иванов", "email": "ivan@example.com", "is_active": True},
            {"id": 2, "name": "Мария Петрова", "email": "maria@example.com", "is_active": True},
            {"id": 3, "name": "Петр Сидоров", "email": "petr@example.com", "is_active": False}
        ]
        return [UserResponse(**user) for user in data]


class ProductService:
    def get_all(self) -> List[ProductResponse]:
        data = [
            {"id": 1, "name": "Ноутбук", "price": 50000.0, "category": "Электроника"},
            {"id": 2, "name": "Смартфон", "price": 25000.0, "category": "Электроника"},
            {"id": 3, "name": "Книга", "price": 500.0, "category": "Книги"}
        ]
        return [ProductResponse(**product) for product in data]


class StatsService:
    def get_stats(self) -> StatsResponse:
        return StatsResponse(
            total_users=150,
            active_users=120,
            total_products=45,
            revenue=1500000.50,
            metrics={
                "conversion_rate": 15.5,
                "average_order_value": 2500.75,
                "monthly_growth": 12.3
            }
        )


user_service = UserService()
product_service = ProductService()
stats_service = StatsService()


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API!", "version": "1.0.0"}


@app.get("/users", response_model=List[UserResponse])
async def get_users():
    return user_service.get_all()


@app.get("/products", response_model=List[ProductResponse])
async def get_products():
    return product_service.get_all()


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    return stats_service.get_stats()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
