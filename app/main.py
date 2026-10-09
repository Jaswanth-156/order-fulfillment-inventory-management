from fastapi import FastAPI

from app.routers import auth, dashboard, inventory_transfer,products,warehouses,inventory,order_assignment,orders,returns,notifications,audit_logs


app = FastAPI(
    title="Order Fulfillment and Inventory Management Platform"
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(warehouses.router)
app.include_router(inventory.router)
app.include_router(order_assignment.router)
app.include_router(orders.router)
app.include_router(returns.router)
app.include_router(notifications.router)
app.include_router(audit_logs.router)
app.include_router(inventory_transfer.router)
app.include_router(dashboard.router)