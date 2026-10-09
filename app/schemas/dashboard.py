from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_orders: int
    pending_orders: int
    processing_orders: int
    shipped_orders: int
    delivered_orders: int
    cancelled_orders: int
    total_products: int
    low_stock_items: int
    total_warehouses: int