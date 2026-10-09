
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_assignment import OrderAssignment
from app.models.user import User
from app.models.warehouse_user import WarehouseUser

from app.repositories import order_assignment_repository
from app.services.audit_log_service import create_audit_log
from app.services.notification_service import create_notification


def assign_order(
    db: Session,
    order_id: int,
    agent_id: int,
    assigned_by: int
):
    # Check whether the order exists.
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise ValueError("Order not found")

    # Check whether the agent exists and is active.
    agent = db.query(User).filter(
        User.id == agent_id,
        User.is_active == True
    ).first()

    if not agent:
        raise ValueError("Fulfillment agent not found or inactive")

    # Verify that the user has the Fulfillment Agent role.
    if agent.role.name != "Fulfillment Agent":
        raise ValueError("User is not a Fulfillment Agent")

    # Verify that the agent is assigned to the order's warehouse.
    warehouse_access = db.query(WarehouseUser).filter(
        WarehouseUser.user_id == agent_id,
        WarehouseUser.warehouse_id == order.warehouse_id
    ).first()

    if not warehouse_access:
        raise ValueError(
            "Fulfillment agent is not assigned to this warehouse"
        )

    # Get the previous assignment, if one exists.
    previous_assignment = (
        order_assignment_repository.get_assignment_by_order(
            db,
            order_id
        )
    )

    # Create the new assignment.
    assignment = OrderAssignment(
        order_id=order_id,
        agent_id=agent_id,
        assigned_by=assigned_by
    )

    try:
        assignment = order_assignment_repository.create_assignment(
            db,
            assignment
        )

        # Notify the agent and record the audit action.
        if previous_assignment:
            create_notification(
                db=db,
                user_id=agent_id,
                title="Order Reassigned",
                message=f"Order {order_id} has been reassigned to you.",
                notification_type="ORDER_REASSIGNED"
            )

            action = "ORDER_REASSIGNED"
            details = {
                "previous_agent_id": previous_assignment.agent_id,
                "new_agent_id": agent_id
            }

        else:
            create_notification(
                db=db,
                user_id=agent_id,
                title="Order Assigned",
                message=f"Order {order_id} has been assigned to you.",
                notification_type="ORDER_ASSIGNED"
            )

            action = "ORDER_ASSIGNED"
            details = {
                "agent_id": agent_id
            }

        create_audit_log(
            db=db,
            user_id=assigned_by,
            action=action,
            entity_type="Order",
            entity_id=order_id,
            details=details
        )

        db.commit()
        db.refresh(assignment)

        return assignment

    except Exception:
        db.rollback()
        raise
