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
        stringer="Alex",
        order_date=date(2025, 6, 10),  
        racket="Wilson Pro Staff", 
        mains_tension=52, 
        mains_string="Luxilon ALU Power",
        crosses_tension=52,
        crosses_string="Luxilon ALU Power",
        replacement_grip=None,
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
        stringer="Alex",
        order_date=date(2025, 6, 18), 
        racket="Head Speed MP", 
        mains_tension=54,
        mains_string="Head Velocity",
        crosses_tension=50,
        crosses_string="Head Synthetic Gut",
        replacement_grip="Head White Tacky",
        paid=True,
        completed=False
    )

    session.add(order)
    session.commit()
    return order

# @pytest.fixture
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
    Orders.create_order(customer=order_wilson.customer, order_date=order_wilson.order_date, racket=order_wilson.racket, mains_tension=order_wilson.mains_tension, mains_string=order_wilson.mains_string, crosses_tension=order_wilson.crosses_tension, crosses_string=order_wilson.crosses_string, replacement_grip=order_wilson.replacement_grip, paid=order_wilson.paid)
    order: Orders = session.query(Orders).filter_by(customer="Alex").first()
    assert order is not None
    assert order.customer == "Alex"
    assert order.order_date == date(2025, 6, 10)
    assert order.racket == "Wilson Pro Staff"
    assert order.mains_tension == 52
    assert order.mains_string == "Luxilon ALU Power"
    assert order.crosses_tension == 52
    assert order.crosses_string == "Luxilon ALU Power"
    assert order.replacement_grip is None
    assert not order.paid

@pytest.mark.parametrize("customer, order_date, racket, mains_tension, mains_string, crosses_tension, crosses_string, replacement_grip, paid", [
    (1, date(2025,1,1), "Wilson Pro Staff", 52, "Luxilon ALU Power", 52, "Luxilon ALU Power", None, False),
    ("Alex", 202511, "Wilson Pro Staff", 52, "Luxilon ALU Power", 52, "Luxilon ALU Power", None, False),
    ("Alex", date(2025,1,1), 1, 52, "Luxilon ALU Power", 52, "Luxilon ALU Power", None, False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", "52", "Luxilon ALU Power", 52, "Luxilon ALU Power", None, False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, "Luxilon ALU Power", "52", "Luxilon ALU Power", None, False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, 1, 52, "Luxilon ALU Power", None, False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, "Luxilon ALU Power", 52, 1, None, False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, "Luxilon ALU Power", 52, "Luxilon ALU Power", 1, False),
    ("Alex", date(2025,1,1), "Wilson Pro Staff", 52, "Luxilon ALU Power", 52, "Luxilon ALU Power", None, "False")
])

def test_create_order_invalid_data(customer, order_date, racket, mains_tension, mains_string, crosses_tension, crosses_string, replacement_grip, paid):
    """Test validation errors during order creation."""
    with pytest.raises(ValueError):
        Orders.create_order(customer, order_date, racket, mains_tension, mains_string, crosses_tension, crosses_string, replacement_grip, paid)


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

def test_get_orders_by_customer(order_wilson: Orders):
    """Test target field value of a order."""
    fetched = Orders.get_orders_by_customer(order_wilson.customer)
    assert fetched[0].racket == "Wilson Pro Staff"

def test_get_orders_by_customer_not_found(app, session):
    """Test error when fetching nonexistent order by target."""
    with pytest.raises(ValueError, match="No orders found for customer 'nonexistent_customer'"):
        Orders.get_orders_by_customer("nonexistent_customer")

def test_get_orders_by_order_date(order_wilson: Orders):
    """Test order_date field of a order."""
    fetched = Orders.get_orders_by_order_date(order_wilson.order_date)
    assert fetched[0].order_date == order_wilson.order_date

def test_get_order_by_order_date_not_found(app, session):
    """Test error when fetching nonexistent order by order_value."""
    with pytest.raises(ValueError, match="No orders found with date '01/01/1111'"):
        Orders.get_orders_by_order_date(date(1111, 1, 1))

def test_get_orders_by_completed(order_wilson: Orders):
    """Test completed field of a order."""
    fetched = Orders.get_orders_by_completed(order_wilson.completed)
    assert fetched[0].completed == order_wilson.completed

# --- Get All orders ---

def test_get_all_orders(session, order_wilson: Orders, order_head: Orders):
    """Test retrieving all orders."""
    orders = Orders.get_all_orders()
    assert isinstance(orders, list)
    expected = [
        {
            "order_id": order_wilson.order_id,
            "customer": order_wilson.customer,
            "stringer": order_wilson.stringer,
            "order_date": order_wilson.order_date,
            "racket": order_wilson.racket,
            "mains_tension": order_wilson.mains_tension,
            "mains_string": order_wilson.mains_string,
            "crosses_tension": order_wilson.crosses_tension,
            "crosses_string": order_wilson.crosses_string,
            "replacement_grip": order_wilson.replacement_grip,
            "paid": order_wilson.paid,
            "completed": order_wilson.completed
        },
        {
            "order_id": order_head.order_id,
            "customer": order_head.customer,
            "stringer": order_head.stringer,
            "order_date": order_head.order_date,
            "racket": order_head.racket,
            "mains_tension": order_head.mains_tension,
            "mains_string": order_head.mains_string,
            "crosses_tension": order_head.crosses_tension,
            "crosses_string": order_head.crosses_string,
            "replacement_grip": order_head.replacement_grip,
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

def test_mark_completed(session, order_wilson: Orders):
    """Test marking an order as complete."""
    complete_order = Orders.mark_completed(order_wilson.order_id)
    assert complete_order.completed == True

def test_mark_completed_not_found(session, order_wilson: Orders):
    """Test error when completing nonexistent order by ID."""
    with pytest.raises(ValueError, match="Order with ID 999 not found"):
        Orders.mark_completed(999)

def test_mark_paid(session, order_wilson: Orders):
    """Test marking an order as paid."""
    paid_order = Orders.mark_paid(order_wilson.order_id)
    assert paid_order.paid == True

def test_mark_paid_not_found(session, order_wilson: Orders):
    """Test error when completing nonexistent order by ID."""
    with pytest.raises(ValueError, match="Order with ID 999 not found"):
        Orders.mark_paid(999)

def test_assign_stringer(session, order_head: Orders):
    """Test assigning a stringer to an order."""
    order: Orders = Orders.assign_stringer(order_head.order_id, "Kempton") # MAKE FAILURE TESTS NEXT
    assert order.stringer == "Kempton"

def test_assign_stringer_not_found(session, order_head: Orders):
    """Test error when completing nonexistent order by ID."""
    with pytest.raises(ValueError, match="Order with ID 999 not found"):
        Orders.assign_stringer(999, "Kempton")

def test_assign_stringer_invalid_stringer(session, order_head: Orders):
    """Test error when completing nonexistent order by ID."""
    with pytest.raises(ValueError, match="stringer must be a non-empty string"):
        Orders.assign_stringer(order_head.order_id, 1)

# --- Delete order ---

def test_delete_order_by_id(session, order_wilson: Orders):
    """Test deleting a order by ID."""
    Orders.delete_order(order_wilson.order_id)
    assert session.get(Orders, order_wilson.order_id) is None

def test_delete_order_not_found(app, session):
    """Test deleting a non-existent order by ID."""
    with pytest.raises(ValueError, match="not found"):
        Orders.delete_order(999)

def test_delete_order_by_customer(session, order_wilson: Orders): # should these really be assert is None? i guess so... should i also make a test where they do find one?
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




