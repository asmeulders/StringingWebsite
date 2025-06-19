import pytest

from RacketTracker.models.order_model import Orders
from pytest_mock import MockerFixture
from datetime import date

# --- Fixtures ---

@pytest.fixture
def order_wilson(session): 
    order = Orders(
        order_id=1,
        customer_id=1, 
        racket_id=1, 
        date=date(2025, 6, 10), 
        mains_tension=55, 
        crosses_tension=55,
        mains_string_id=1,
        crosses_string_id=1,
        paid=False,
        completed=False,
    )
    session.add(order)
    session.commit()
    return order

@pytest.fixture
def order_head(session):
    order = Orders(
        order_id=2,
        customer_id=2, 
        racket_id=2, 
        date=date(2025, 6, 18), 
        mains_tension=54, 
        crosses_tension=50,
        mains_string_id=2,
        crosses_string_id=3,
        paid=True,
        completed=False,
    )

    session.add(order)
    session.commit()
    return order

# --- Create order ---

def test_create_order(session):
    """Test creating a new order."""
    Orders.create_order(customer_id=1, racket_id=1, date=date(2025, 6, 10), mains_tension=55, mains_string_id=1, paid=False)
    order = session.query(Orders).filter_by(customer_id=3).first()
    assert order is not None
    assert order.customer_id == 1
    assert order.racket_id == 1
    assert order.date == date(2025, 6, 10)
    assert order.mains_tension == 55
    assert order.crosses_tension == 55
    assert order.mains_string_id == 1
    assert order.crosses_string_id == 1
    assert not order.paid

@pytest.mark.parametrize("customer_id, racket_id, date, mains_tension, crosses_tension, mains_string_id, crosses_string_id, paid", [
    ("1", 1, date(2025,1,1), 50, 50, 1, 1, False),
    (1, "1", date(2025,1,1), 50, 50, 1, 1, False),
    (1, 1, 202511, 50, 50, 1, 1, False),
    (1, 1, date(2025,1,1), "50", 50, 1, 1, False),
    (1, 1, date(2025,1,1), 50, "50", 1, 1, False),
    (1, 1, date(2025,1,1), 50, 50, "1", 1, False),
    (1, 1, date(2025,1,1), 50, 50, 1, "1", False),
    (1, 1, date(2025,1,1), 50, 50, 1, 1, "False")
])

def test_create_order_invalid_data(customer_id, racket_id, date, mains_tension, crosses_tension, mains_string_id, crosses_string_id, paid):
    """Test validation errors during order creation."""
    with pytest.raises(ValueError):
        Orders.create_order(customer_id, racket_id, date, mains_tension, crosses_tension, mains_string_id, crosses_string_id, paid)


# --- Get order ---

def test_get_order_by_id(order_wilson):
    """Test fetching a order by ID."""
    fetched = Orders.get_order_by_id(order_wilson.order_id)
    assert fetched.customer_id == 1
    assert fetched.date == date(2025, 6, 10)

def test_get_order_by_id_not_found(app, session):
    """Test error when fetching nonexistent order by ID."""
    with pytest.raises(ValueError, match="Order with ID 999 not found"):
        Orders.get_order_by_id(999)

# def test_get_order_target(order_biceps):
#     """Test target field value of a order."""
#     fetched = Orders.get_order_by_id(order_biceps.id)
#     assert fetched.target == "biceps"

# def test_get_order_by_target_not_found(app, session):
#     """Test error when fetching nonexistent order by target."""
#     with pytest.raises(ValueError, match="No orders found with target 'nonexistent_target'"):
#         orders.get_orders_by_target("nonexistent_target")

# def test_get_order_value(order_biceps):
#     """Test order_value field of a order."""
#     fetched = orders.get_order_by_id(order_biceps.id)
#     assert isinstance(fetched.order_value, int)
#     assert fetched.order_value == order_biceps.order_value

# def test_get_order_by_order_value_not_found(app, session):
#     """Test error when fetching nonexistent order by order_value."""
#     with pytest.raises(ValueError, match="No orders found with order value '9999'"):
#         orders.get_orders_by_order_value(9999)

# def test_get_order_completed(order_biceps):
#     """Test completed field of a order."""
#     fetched = orders.get_order_by_id(order_biceps.id)
#     assert isinstance(fetched.completed, bool)
#     assert fetched.completed == order_biceps.completed

# --- Update ---
def test_update_order(session, order_wilson):
    """Test updating an existing order."""
    updated = Orders.update_order(order_wilson.id, racket_id=5, crosses_string_id=7)
    assert updated.racket_id == 5
    assert updated.crosses_string_id == 7

# --- Delete order ---

def test_delete_order_by_id(session, order_wilson):
    """Test deleting a order by ID."""
    Orders.delete_order(order_wilson.id)
    assert session.query(Orders).get(order_wilson.id) is None

def test_delete_order_not_found(app, session):
    """Test deleting a non-existent order by ID."""
    with pytest.raises(ValueError, match="not found"):
        Orders.delete_order(999)

# def test_delete_order_by_target(session, order_biceps):
#     """Test deleting a order by target."""
#     orders.delete_order_by_target(order_biceps.target)
#     deleted = session.query(orders).filter_by(target=order_biceps.target).first()
#     assert deleted is None

# def test_delete_order_by_order_value(session, order_biceps):
#     """Test deleting a order by order_value."""
#     orders.delete_order_by_order_value(order_biceps.order_value)
#     deleted = session.query(orders).filter_by(order_value=order_biceps.order_value).first()
#     assert deleted is None

# def test_delete_order_by_completed(session, order_biceps):
#     """Test deleting a order by completed status."""
#     orders.delete_order_by_completed(order_biceps.completed)
#     deleted = session.query(orders).filter_by(completed=order_biceps.completed).first()
#     assert deleted is None

# --- Log Progress ---
# def test_log_progress_updated(session, order_biceps):
#     """Test logging progress toward a order."""
#     result = order_biceps.log_progress(5.0)
#     assert "Progress updated" in result
#     session.refresh(order_biceps)
#     assert order_biceps.order_progress == 7.0


# def test_log_progress_completed(session, order_biceps):
#     """Test logging progress toward a order."""
#     result = order_biceps.log_progress(8.0)
#     assert "order completed" in result
#     session.refresh(order_biceps)
#     assert order_biceps.order_progress == 10.0

# --- Progress Notes ---

# def test_add_progress_note(session, order_biceps):
#     """Test adding a progress note."""
#     note = "Curls with dumbbells"
#     order_biceps.add_progress_note(note)
#     session.commit()
#     notes = order_biceps.get_progress_notes()
#     assert note in notes


# --- Recommendations ---

# def test_get_exercise_recommendations(session, order_biceps, mocker):
#     """Test getting exercise recommendations for a order."""
#     mock_response = [
#         {"name": "bicep curl", "equipment": "dumbbell"},
#         {"name": "hammer curl", "equipment": "dumbbell"}
#     ]

#     mock_fetch = mocker.patch("coach_peter.models.order_model.fetch_recommendation", return_value=mock_response)

#     result = orders.get_exercise_recommendations(order_biceps.id)

#     mock_fetch.assert_called_once_with("biceps")
#     assert isinstance(result, list)
#     assert result[0]["name"] == "bicep curl"


# --- Get All orders ---

def test_get_all_orders(session, order_wilson, order_head):
    """Test retrieving all orders."""
    orders = Orders.get_all_orders()
    assert isinstance(orders, list)
    expected = [
        {
            "order_id": order_wilson.id,
            "customer_id": order_wilson.target,
            "racket_id": order_wilson.order_value,
            "date": order_wilson.order_progress,
            "mains_tension": order_wilson.completed,
            "crosses_tension": order_wilson.progress_notes,
            "mains_string_id": order_wilson.mains_string_id,
            "crosses_string_id": order_wilson.crosses_string_id,
            "paid": order_wilson.paid,
            "completed": order_wilson.completed
        },
        {
            "order_id": order_head.id,
            "customer_id": order_head.target,
            "racket_id": order_head.order_value,
            "date": order_head.order_progress,
            "mains_tension": order_head.completed,
            "crosses_tension": order_head.progress_notes,
            "mains_string_id": order_head.mains_string_id,
            "crosses_string_id": order_head.crosses_string_id,
            "paid": order_head.paid,
            "completed": order_head.completed
        }
    ]
    assert orders == expected