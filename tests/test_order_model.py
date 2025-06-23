import pytest

from RacketTracker.models.order_model import Orders # , Customers, Strings, Rackets
from pytest_mock import MockerFixture
from datetime import date

# --- Fixtures ---

@pytest.fixture
def order_wilson(session): 
    order = Orders(
        order_id=1,
        customer="Alex",
        order_date=date(2025, 6, 10),  
        racket="Wilson Pro Staff", 
        mains_tension=52, 
        crosses_tension=52,
        mains_string="Luxilon ALU Power",
        crosses_string="Luxilon ALU Power",
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
        customer="Rocky", 
        order_date=date(2025, 6, 18), 
        racket="Head Speed MP", 
        mains_tension=54, 
        crosses_tension=50,
        mains_string="Head Velocity",
        crosses_string="Head Synthetic Gut",
        paid=True,
        completed=False
    )

    session.add(order)
    session.commit()
    return order

@pytest.fixture
# def customer(session):
#     customer = Customers(
#         customer_id=1,
#         name="Alex",
#         phone_number=1000000001
#     )

#     session.add(customer)
#     session.commit()
#     return customer

# @pytest.fixture
# def string(session):
#     string = Strings(
#         string_id=1,
#         brand="Luxilon", 
#         model="ALU Power", 
#         gauge=125, 
#         shape="Round", 
#         type="Polyester"
#     )

#     session.add(string)
#     session.commit()
#     return string

# @pytest.fixture
# def racket(session):
#     racket = Rackets(
#         racket_id=1,
#         brand="Wilson", 
#         model="Pro Staff", 
#         year=2021, 
#         head_size=97, 
#         grip_size=4.375,
#         weight=315,
#         stringing_pattern="16x19",
#         swing_weight=315,
#         balance=27,
#         stiffness=60
#     )

#     session.add(racket)
#     session.commit()
#     return racket

# --- Create order ---

def test_create_order(session, order_wilson: Orders):
    """Test creating a new order."""
    Orders.create_order(customer=order_wilson.customer, order_date=order_wilson.order_date, racket=order_wilson.racket, mains_tension=order_wilson.mains_tension, crosses_tension=order_wilson.crosses_tension, mains_string=order_wilson.mains_string, crosses_string=order_wilson.crosses_string, paid=order_wilson.paid)
    order: Orders = session.query(Orders).filter_by(customer_id=3).first()
    assert order is not None
    assert order.customer == "Alex"
    assert order.order_date == date(2025, 6, 10)
    assert order.racket == "Wilson Pro Staff"
    assert order.mains_tension == 52
    assert order.crosses_tension == 52
    assert order.mains_string == "Luxilon Pro Staff"
    assert order.crosses_string == "Luxilon Pro Staff"
    assert not order.paid

@pytest.mark.parametrize("customer, order_date, racket, mains_tension, crosses_tension, mains_string, crosses_string, paid", [
    (1, date(2025,1,1), "Wilson Pro Staff", 52, 52, "Luxilon ALU Power", "Luxilon ALU Power", False),
    ("Alex", 202511, "Wilson Pro Staff", 52, 52, "Luxilon ALU Power", "Luxilon ALU Power", False),
    ("Alex", date(2025,1,1), 1, 52, 52, "Luxilon ALU Power", "Luxilon ALU Power", False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", "52", 52, "Luxilon ALU Power", "Luxilon ALU Power", False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, "52", "Luxilon ALU Power", "Luxilon ALU Power", False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, 52, 1, "Luxilon ALU Power", False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, 52, "Luxilon ALU Power", 1, False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, 52, "Luxilon ALU Power", "Luxilon ALU Power", "False")
])

def test_create_order_invalid_data(customer, order_date, racket, mains_tension, crosses_tension, mains_string, crosses_string, paid):
    """Test validation errors during order creation."""
    with pytest.raises(ValueError):
        Orders.create_order(customer, order_date, racket, mains_tension, crosses_tension, mains_string, crosses_string, paid)


# --- Get order ---

def test_get_order_by_id(order_wilson: Orders):
    """Test fetching a order by ID."""
    fetched = Orders.get_order_by_id(order_wilson.order_id)
    assert fetched.customer ==  "Alex"
    assert fetched.order_date == date(2025, 6, 10)

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
# --- Get All orders ---

def test_get_all_orders(session, order_wilson: Orders, order_head: Orders):
    """Test retrieving all orders."""
    orders = Orders.get_all_orders()
    assert isinstance(orders, list)
    expected = [
        {
            "order_id": order_wilson.order_id,
            "customer": order_wilson.customer,
            "order_date": order_wilson.order_date,
            "racket": order_wilson.racket,
            "mains_tension": order_wilson.mains_tension,
            "crosses_tension": order_wilson.crosses_tension,
            "mains_string": order_wilson.mains_string,
            "crosses_string": order_wilson.crosses_string,
            "paid": order_wilson.paid,
            "completed": order_wilson.completed
        },
        {
            "order_id": order_head.order_id,
            "customer": order_head.customer,
            "order_date": order_head.order_date,
            "racket": order_head.racket,
            "mains_tension": order_head.mains_tension,
            "crosses_tension": order_head.crosses_tension,
            "mains_string": order_head.mains_string,
            "crosses_string": order_head.crosses_string,
            "paid": order_head.paid,
            "completed": order_head.completed
        }
    ]
    assert orders == expected

# --- Update ---
def test_update_order(session, order_wilson: Orders):
    """Test updating an existing order."""
    updated = Orders.update_order(order_wilson.order_id, racket="Head Speed MP", crosses_string="Wilson Sensation")
    assert updated.racket == "Head Speed MP"
    assert updated.crosses_string == "Wilson Sensation"

# --- Delete order ---

def test_delete_order_by_id(session, order_wilson: Orders):
    """Test deleting a order by ID."""
    Orders.delete_order(order_wilson.order_id)
    assert session.get(Orders, order_wilson.order_id) is None

def test_delete_order_not_found(app, session):
    """Test deleting a non-existent order by ID."""
    with pytest.raises(ValueError, match="not found"):
        Orders.delete_order(999)

def test_delete_order_by_customer(session, order_wilson: Orders): # should these really be assert is None? i guess so...
    """Test deleting a order by target."""
    Orders.delete_order_by_customer(order_wilson.customer)
    deleted = session.query(Orders).filter_by(customer=order_wilson.customer).first()
    assert deleted is None

def test_delete_order_by_order_date(session, order_wilson: Orders):
    """Test deleting a order by order_value."""
    Orders.delete_order_by_order_date(order_wilson.order_date)
    deleted = session.query(Orders).filter_by(order_date=order_wilson.order_date).first()
    assert deleted is None

def test_delete_order_by_completed(session, order_wilson: Orders):
    """Test deleting a order by completed status."""
    Orders.delete_order_by_completed(order_wilson.completed)
    deleted = session.query(Orders).filter_by(completed=order_wilson.completed).first()
    assert deleted is None

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


