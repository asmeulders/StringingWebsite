from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS

from config import ProductionConfig

from RacketTracker.db import db
from RacketTracker.models.order_model import Orders
from RacketTracker.models.user_model import Users
from RacketTracker.utils.logger import configure_logger
from datetime import date
import datetime, time
from werkzeug.routing import BaseConverter
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)
configure_logger(logger)

load_dotenv()

# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code"""

#     if isinstance(obj, date):
#         return obj.strftime('%Y%m%d')
#     raise TypeError ("Type %s not serializable" % type(obj))

# class DateConverter(BaseConverter):
#     """Extracts a ISO8601 date from the path and validates it."""
#     def to_python(self, value):
#         try:
#             return datetime.datetime.strptime(value, '%Y%m%d').date()
#         except ValueError as e:
#             raise e

#     def to_url(self, value):
#         return value.strftime('%Y%m%d')
    
def create_app(config_class=ProductionConfig) -> Flask:
    """Create a Flask application with the specified configuration.

    Args:
        config_class (Config): The configuration class to use.

    Returns:
        Flask app: The configured Flask application.

    """
    app = Flask(__name__)
    

    configure_logger(app.logger)

    app.config.from_object(config_class)
    # app.url_map.converters['date'] = DateConverter

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Front end test
    @app.route('/api/time')
    def get_current_time():
        return {'time': time.time()}
    
    @app.route('/api/tutorial-users', methods=['GET'])
    def tutorial_users():
        return jsonify(
            {
                'users': [
                    'alex',
                    'daniel',
                    'kempton'
                ]
            }
        )
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(username=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return make_response(jsonify({
            "status": "error",
            "message": "Authentication required"
        }), 401)

    # plan_model = PlanModel()

    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.

        """
        app.logger.info("Health check endpoint hit")
        return make_response(jsonify({
            'status': 'success',
            'message': 'Service is running'
        }), 200)

    ##########################################################
    #
    # User Management
    #
    #########################################################

    @app.route('/api/create-user', methods=['PUT'])
    def create_user() -> Response:
        """Register a new user account.

        Expected JSON Input:
            - username (str): The desired username.
            - password (str): The desired password.

        Returns:
            JSON response indicating the success of the user creation.

        Raises:
            400 error if the username or password is missing.
            500 error if there is an issue creating the user in the database.
        """
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            Users.create_user(username, password)
            return make_response(jsonify({
                "status": "success",
                "message": f"User '{username}' created successfully"
            }), 201)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"User creation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while creating user",
                "details": str(e)
            }), 500)

    @app.route('/api/login', methods=['POST'])
    def login() -> Response:
        """Authenticate a user and log them in.

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The password of the user.

        Returns:
            JSON response indicating the success of the login attempt.

        Raises:
            401 error if the username or password is incorrect.
        """
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            if Users.check_password(username, password):
                user = Users.query.filter_by(username=username).first()
                login_user(user)
                return make_response(jsonify({
                    "status": "success",
                    "message": f"User '{username}' logged in successfully"
                }), 200)
            else:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid username or password"
                }), 401)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 401)
        except Exception as e:
            app.logger.error(f"Login failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred during login",
                "details": str(e)
            }), 500)

    @app.route('/api/logout', methods=['POST'])
    @login_required
    def logout() -> Response:
        """Log out the current user.

        Returns:
            JSON response indicating the success of the logout operation.

        """
        logout_user()
        return make_response(jsonify({
            "status": "success",
            "message": "User logged out successfully"
        }), 200)

    @app.route('/api/change-password', methods=['POST'])
    @login_required
    def change_password() -> Response:
        """Change the password for the current user.

        Expected JSON Input:
            - new_password (str): The new password to set.

        Returns:
            JSON response indicating the success of the password change.

        Raises:
            400 error if the new password is not provided.
            500 error if there is an issue updating the password in the database.
        """
        try:
            data = request.get_json()
            new_password = data.get("new_password")

            if not new_password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "New password is required"
                }), 400)

            username = current_user.username
            Users.update_password(username, new_password)
            return make_response(jsonify({
                "status": "success",
                "message": "Password changed successfully"
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Password change failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while changing password",
                "details": str(e)
            }), 500)

    @app.route('/api/reset-users', methods=['DELETE'])
    def reset_users() -> Response:
        """Recreate the users table to delete all users.

        Returns:
            JSON response indicating the success of recreating the Users table.

        Raises:
            500 error if there is an issue recreating the Users table.
        """
        try:
            app.logger.info("Received request to recreate Users table")
            with app.app_context():
                Users.__table__.drop(db.engine)
                Users.__table__.create(db.engine)
            app.logger.info("Users table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": f"Users table recreated successfully"
            }), 200)

        except Exception as e:
            app.logger.error(f"Users table recreation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while deleting users",
                "details": str(e)
            }), 500)

    # ##########################################################
    # #
    # # orders
    # #
    # ##########################################################

    @app.route('/api/reset-orders', methods=['DELETE'])
    def reset_orders() -> Response:
        """Recreate the orders table to delete orders.

        Returns:
            JSON response indicating the success of recreating the orders table.

        Raises:
            500 error if there is an issue recreating the orders table.
        """
        try:
            app.logger.info("Received request to recreate orders table")
            with app.app_context():
                Orders.__table__.drop(db.engine)
                Orders.__table__.create(db.engine)
            app.logger.info("Orders table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": f"Orders table recreated successfully"
            }), 200)

        except Exception as e:
            app.logger.error(f"Orders table recreation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while deleting orders",
                "details": str(e)
            }), 500)


    @app.route('/api/create-order', methods=['POST'])
    @login_required
    def add_order() -> Response:
        """Route to create a new order.

        Expected JSON Input:
            - customer (str): The customer who made the order.
            - order_date (date): The date of the order.
            - racket (str): The name of the racket.
            - mains_tension (int): Value of the mains tension.
            - crosses_tension (int): Value of the crosses tension.
            - mains_string (str): Name of the string used on the mains.
            - crosses_string (str): Name of the string used on the crosses.
            - replacement_grip (str): Name of the replacement grip desired.
            - paid (bool): Boolean for paid status of order.

        Returns:
            JSON response indicating the success of the order addition.

        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the order to the plan.

        """
        app.logger.info("Received request to add a new order")

        try:
            data = request.get_json()

            required_fields = ["customer", "order_date", "racket", "mains_tension", "crosses_tension", "mains_string", "crosses_string", "replacement_grip", "paid"]
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                app.logger.warning(f"Missing required fields: {missing_fields}")
                return make_response(jsonify({
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400)

            customer = data["customer"]
            order_date = datetime.datetime.strptime(data["order_date"], "%Y%m%d").date()
            racket = data["racket"]
            mains_tension = data["mains_tension"]
            mains_string = data["mains_string"]
            crosses_tension = data["crosses_tension"]
            crosses_string = data["crosses_string"]
            replacement_grip = data["replacement_grip"]
            paid = data["paid"]

            if (
                not isinstance(customer, str)
            ):
                app.logger.warning("Invalid input data types - customer")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: customer should be a string"
                }), 400)
            
            if (
                not isinstance(order_date, date)
            ):
                app.logger.warning("Invalid input data types - order_date")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: order_date should be a date object"
                }), 400)
            
            if (
                not isinstance(racket, str)
            ):
                app.logger.warning("Invalid input data types - racket")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: racket should be a string"
                }), 400)
            
            if (
                not isinstance(mains_tension, int)
            ):
                app.logger.warning("Invalid input data types - mains_tension")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: mains_tension should be an int"
                }), 400)
            
            if (
                not isinstance(mains_string, str)
            ):
                app.logger.warning("Invalid input data types - mains_string")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: mains_string should be a string"
                }), 400)
            
            if (
                crosses_tension and not isinstance(crosses_tension, int)
            ):
                app.logger.warning("Invalid input data types - crosses_tension")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: crosses_tension should be an int"
                }), 400)
            
            if (
                crosses_string and not isinstance(crosses_string, str)
            ):
                app.logger.warning("Invalid input data types - crosses_string")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: crosses_string should be a string"
                }), 400)
            
            if (
                replacement_grip and not isinstance(replacement_grip, str)
            ):
                app.logger.warning("Invalid input data types - replacement_grip")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: replacement_grip should be a string"
                }), 400)
            
            if (
                not isinstance(paid, bool)
            ):
                app.logger.warning("Invalid input data types - paid")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid input types: paid should be a bool"
                }), 400)
            
            paid_status = "paid" if paid else "unpaid"

            app.logger.info(f"Adding order: {customer} - {racket}: {order_date} - {paid_status}")
            Orders.create_order(customer=customer, order_date=order_date, racket=racket, mains_tension=mains_tension, mains_string=mains_string, crosses_tension=crosses_tension, crosses_string=crosses_string, replacement_grip=replacement_grip, paid=paid)

            app.logger.info(f"Order added successfully: {customer} - {racket}: {order_date} - {paid_status}")
            return make_response(jsonify({
                "status": "success",
                "message": f"Order: '{customer} - {racket}: {order_date} - {paid_status}' added successfully"
            }), 201)

        except Exception as e:
            app.logger.error(f"Failed to add order: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while adding the order",
                "details": str(e)
            }), 500)


    @app.route('/api/delete-order/<int:order_id>', methods=['DELETE'])
    @login_required
    def delete_order(order_id: int) -> Response:
        """Route to delete a order by ID.

        Path Parameter:
            - order_id (int): The ID of the order to delete.

        Returns:
            JSON response indicating success of the operation.

        Raises:
            400 error if the order does not exist.
            500 error if there is an issue removing the order from the database.

        """
        try:
            app.logger.info(f"Received request to delete order with ID {order_id}")

            # Check if the order exists before attempting to delete
            order = Orders.get_order_by_id(order_id)
            if not order:
                app.logger.warning(f"Order with ID {order_id} not found.")
                return make_response(jsonify({
                    "status": "error",
                    "message": f"Order with ID {order_id} not found"
                }), 400)

            Orders.delete_order(order_id)
            app.logger.info(f"Successfully deleted order with ID {order_id}")

            return make_response(jsonify({
                "status": "success",
                "message": f"Order with ID {order_id} deleted successfully"
            }), 200)

        except Exception as e:
            app.logger.error(f"Failed to delete order: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while deleting the order",
                "details": str(e)
            }), 500)


    @app.route('/api/get-all-orders-from-history', methods=['GET'])
    @login_required
    def get_all_orders() -> Response:
        """Route to retrieve all orders from the history (non-deleted).

        Returns:
            JSON response containing the list of orders.

        Raises:
            500 error if there is an issue retrieving orders from the history.

        """
        try:
            # Extract query parameter for sorting by play count
            app.logger.info(f"Received request to retrieve all orders from history")

            orders = Orders.get_all_orders()

            app.logger.info(f"Successfully retrieved {len(orders)} orders from the catalog")

            return make_response(jsonify({
                "status": "success",
                "message": "Orders retrieved successfully",
                "orders": orders
            }), 200)

        except Exception as e:
            app.logger.error(f"Failed to retrieve orders: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving orders",
                "details": str(e)
            }), 500)


    @app.route('/api/get-order-from-history-by-id/<int:order_id>', methods=['GET'])
    @login_required
    def get_order_by_id(order_id: int) -> Response:
        """Route to retrieve a order by its ID.

        Path Parameter:
            - order_id (int): The ID of the order.

        Returns:
            JSON response containing the order details.

        Raises:
            400 error if the order does not exist.
            500 error if there is an issue retrieving the order.

        """
        try:
            app.logger.info(f"Received request to retrieve order with ID {order_id}")

            order = Orders.get_order_by_id(order_id)
            if not order:
                app.logger.warning(f"Order with ID {order_id} not found.")
                return make_response(jsonify({
                    "status": "error",
                    "message": f"Order with ID {order_id} not found"
                }), 400)

            app.logger.info(f"Successfully retrieved order {order.order_id} for {order.customer}")

            return make_response(jsonify({
                "status": "success",
                "message": "Order retrieved successfully",
                "customer": order.customer
            }), 200)

        except Exception as e:
            app.logger.error(f"Failed to retrieve order by ID: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving the order",
                "details": str(e)
            }), 500)

    @app.route('/api/orders/by-customer/<string:customer>', methods=['GET'])
    @login_required
    def get_orders_by_customer(customer: str) -> Response:
        """Route to retrieve all orders by customer.

        Path Parameter:
            - customer (str): Name of the customer.

        Returns:
            JSON response with a list of orders for the customer.

        Raises:
            400 error if no matching orders are found.
            500 error if there is an issue retrieving the orders.
        """
        try:
            app.logger.info(f"Request to retrieve orders by customer: {customer}")
            orders = Orders.get_orders_by_customer(customer)
            return make_response(jsonify({
                "status": "success",
                "orders": [g.order_id for g in orders] 
            }), 200)
        except ValueError as e:
            app.logger.warning(f"Order retrieval failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Internal error retrieving orders by customer: {e}")
            return make_response(jsonify({
                "status": "error", 
                "message": "Internal server error"
            }), 500)

    @app.route('/api/orders/by-completed/<string:completed>', methods=['GET'])
    @login_required
    def get_orders_by_completed(completed: str) -> Response:
        """Route to retrieve all orders by completion status.

        Path Parameter:
            - completed (str): Either 'true' or 'false'.

        Returns:
            JSON response with a list of matching orders.

        Raises:
            400 error for invalid boolean input or missing data.
            500 error for unexpected database issues.
        """
        try:
            app.logger.info(f"Request to retrieve orders by completion status: {completed}")
            status = completed.lower() == 'true'
            orders = Orders.get_orders_by_completed(status)
            return make_response(jsonify({
                "status": "success",
                "orders": [g.order_id for g in orders]
            }), 200)
        except ValueError as e:
            app.logger.warning(f"Order retrieval failed: {e}")
            return make_response(jsonify({"status": "error", "message": str(e)}), 400)
        except Exception as e:
            app.logger.error(f"Internal error retrieving completed orders: {e}")
            return make_response(jsonify({"status": "error", "message": "Internal server error"}), 500)

    @app.route('/api/orders/by-date/<string:order_date_string>', methods=['GET'])
    @login_required
    def get_orders_by_order_date(order_date_string: str) -> Response: # should i make this a datetime object instead?
        """Route to retrieve all orders by order date.

        Path Parameter:
            - order_date_string (str): The string representation of the date.

        Returns:
            JSON response with matching orders.

        Raises:
            400 error if no orders are found.
            500 error if database issues occur.
        """
        try:
            app.logger.info(f"Request to retrieve orders by order date: {order_date_string}")
            order_date = datetime.datetime.strptime(order_date_string, "%Y%m%d").date()
            orders = Orders.get_orders_by_order_date(order_date)
            return make_response(jsonify({
                "status": "success",
                "orders": [g.order_id for g in orders]
            }), 200)
        except ValueError as e:
            app.logger.warning(f"Order retrieval failed: {e}")
            return make_response(jsonify({"status": "error", "message": str(e)}), 400)
        except Exception as e:
            app.logger.error(f"Error retrieving orders by order value: {e}")
            return make_response(jsonify({"status": "error", "message": "Internal server error"}), 500)

    @app.route('/api/update-order/<int:order_id>', methods=['PATCH']) 
    @login_required
    def update_order(order_id: int) -> Response:
        """Route to update a order by ID.

        Path Parameter:
            - order_id (int): The ID of the order to update.

        Expected JSON Input:
            - customer (str): The updated customer.
            - order_date (str): The updated date represented by a string.
            - racket (str): The updated name of the racket.
            - mains_tension (int): Updated value of the mains tension.
            - crosses_tension (int): Updated value of the crosses tension.
            - mains_string (str): Updated name of the string used on the mains.
            - crosses_string (str): Updated name of the string used on the crosses.
            - replacement_grip (str): Updated name of the replacement grip desired.

        Returns:
            JSON response with the updated order or error.

        Raises:
            400 error for invalid input or if order not found.
            500 error for database issues.
        """
        try:
            data = request.get_json()
            order = Orders.get_order_by_id(order_id)

            new_customer = data.get("customer")
            
            new_order_date = data.get('order_date')
            logger.info(new_order_date)
            new_racket = data.get("racket")
            new_mains_tension = data.get("mains_tension")
            new_mains_string = data.get("mains_string")
            new_crosses_tension = data.get("crosses_tension")
            new_crosses_string = data.get("crosses_string")
            new_replacement_grip = data.get("replacement_grip")


            old_fields = [order.customer, order.order_date.strftime('%Y%m%d'), order.racket, order.mains_tension, order.mains_string, order.crosses_tension, order.crosses_string, order.replacement_grip]
            logger.info(old_fields[1])
            new_fields = [new_customer, new_order_date, new_racket, new_mains_tension, new_mains_string, new_crosses_tension, new_crosses_string, new_replacement_grip]
            updated_fields = []
            fields = []

            for i in range(len(old_fields)):
                if old_fields[i] != new_fields[i]:
                    logger.info(new_fields[i])
                    updated_fields.append(new_fields[i])
                    fields.append(new_fields[i])
                else:
                    fields.append(None)

            logger.info(datetime.datetime.strptime(fields[1], '%Y%m%d').date(), type(datetime.datetime.strptime(fields[1], '%Y%m%d').date()))

            updated_order = Orders.update_order(
                order_id,
                customer=fields[0],
                order_date=datetime.datetime.strptime(fields[1], '%Y%m%d').date(),
                racket=fields[2],
                mains_tension=fields[3],
                mains_string=fields[4],
                crosses_tension=fields[5],
                crosses_string=fields[6],
                replacement_grip=fields[7],
            )
            app.logger.info(f"Updated order {order_id} successfully.")

            return make_response(jsonify({
                "status": "success", 
                "order": updated_order.order_id,
                "updated_fields": updated_fields
            }), 200)
        except ValueError as e:
            app.logger.warning(f"Update failed for order {order_id}: {e}")
            return make_response(jsonify({
                "status": "error", 
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Internal error updating order {order_id}: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "Internal server error"
            }), 500)

    @app.route('/api/delete-order-by-customer/<string:customer>', methods=['DELETE'])
    @login_required
    def delete_order_by_customer(customer: str) -> Response:
        """Route to delete a order by customer.

        Path Parameter:
            - customer (str): The customer for the order.

        Returns:
            JSON response on successful deletion.

        Raises:
            400 error if order is not found.
            500 error on DB issues.
        """
        try:
            Orders.delete_order_by_customer(customer)
            app.logger.info(f"Deleted order with customer {customer}.")
            return make_response(jsonify({"status": "success", "message": f"Order with customer '{customer}' deleted."}), 200)
        except ValueError as e:
            app.logger.warning(f"Order delete failed for customer {customer}: {e}")
            return make_response(jsonify({"status": "error", "message": str(e)}), 400)
        except Exception as e:
            app.logger.error(f"Internal error deleting order by customer {customer}: {e}")
            return make_response(jsonify({"status": "error", "message": "Internal server error"}), 500)


    @app.route('/api/delete-order-by-date/<string:order_date_string>', methods=['DELETE'])
    @login_required
    def delete_order_by_date(order_date_string: str) -> Response:
        """Route to delete a order by date.

        Path Parameter:
            - order_date_string (str): The string representing the date of the order.

        Returns:
            JSON response on successful deletion.

        Raises:
            400 error if order is not found.
            500 error on DB issues.
        """
        try:
            app.logger.info(f"Request to retrieve orders by order date: {order_date_string}")
            order_date = datetime.datetime.strptime(order_date_string, "%Y%m%d").date()
            Orders.delete_order_by_order_date(order_date)
            app.logger.info(f"Deleted order with date {order_date}.")
            return make_response(jsonify({"status": "success", "message": f"Order with date {order_date_string} deleted."}), 200)
        except ValueError as e:
            app.logger.warning(f"Order delete failed for date {order_date}: {e}")
            return make_response(jsonify({"status": "error", "message": str(e)}), 400)
        except Exception as e:
            app.logger.error(f"Internal error deleting order by date {order_date}: {e}")
            return make_response(jsonify({"status": "error", "message": "Internal server error"}), 500)


    @app.route('/api/delete-order-by-completed/<completed>', methods=['DELETE'])
    @login_required
    def delete_order_by_completed(completed: str) -> Response:
        """Route to delete a order by completed status.

        Path Parameter:
            - completed (str): 'true' or 'false'.

        Returns:
            JSON response on successful deletion.

        Raises:
            400 error if order is not found.
            500 error on DB issues.
        """
        try:
            status = completed.lower() == 'true'
            Orders.delete_order_by_completed(status)
            app.logger.info(f"Deleted order with completed status {status}.")
            return make_response(jsonify({"status": "success", "message": f"Order with completed={status} deleted."}), 200)
        except ValueError as e:
            app.logger.warning(f"Delete by completed failed: {e}")
            return make_response(jsonify({"status": "error", "message": str(e)}), 400)
        except Exception as e:
            app.logger.error(f"Error deleting order by completed: {e}")
            return make_response(jsonify({"status": "error", "message": "Internal server error"}), 500)

    
    @app.route('/api/orders/mark-completed/<int:order_id>', methods=['PATCH'])
    @login_required
    def mark_order_completed(order_id: int):
        """Route to mark an order as completed by the id.

        Path Parameter:
            - order_id (int): The ID of the order to complete.

        Returns:
            JSON response on successful completion.

        Raises:
            400 error for invalid input or if order not found.
            500 error for database issues.
        """
        try:
            completed_order = Orders.mark_completed(order_id)
            app.logger.info(f"Completed order {order_id} successfully.")

            return make_response(jsonify({
                "status": "success", 
                "order": completed_order.order_id
            }), 200)
        
        except ValueError as e:
            app.logger.warning(f"Completion failed for order {order_id}: {e}")
            return make_response(jsonify({
                "status": "error", 
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Internal error updating order {order_id}: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "Internal server error"
            }), 500)
        

    @app.route('/api/orders/mark-paid/<int:order_id>', methods=['PATCH'])
    @login_required
    def mark_order_paid(order_id: int):
        """Route to mark an order as paid by the id.

        Path Parameter:
            - order_id (int): The ID of the order to mark paid.

        Returns:
            JSON response on successful completion.

        Raises:
            400 error for invalid input or if order not found.
            500 error for database issues.
        """
        try:
            paid_order = Orders.mark_paid(order_id)
            app.logger.info(f"Paid for order {order_id} successfully.")

            return make_response(jsonify({
                "status": "success", 
                "order": paid_order.order_id
            }), 200)
        
        except ValueError as e:
            app.logger.warning(f"Payment failed for order {order_id}: {e}")
            return make_response(jsonify({
                "status": "error", 
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Internal error paying for order {order_id}: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "Internal server error"
            }), 500)
        

    @app.route('/api/orders/assign-stringer/<int:order_id>', methods=['PATCH'])
    @login_required
    def assign_stringer(order_id: int):
        """Route to assign a stringer to the order with the id given.

        Path Parameter:
            - order_id (int): The ID of the order to assign the stringer to.

        Expected JSON Input:
            - stringer (str): The assigned stringers.

        Returns:
            JSON response on successful completion.

        Raises:
            400 error for invalid input or if order not found.
            500 error for database issues.
        """
        try:
            data = request.get_json()

            stringer = data['stringer']

            assigned_order = Orders.assign_stringer(order_id, stringer)
            app.logger.info(f"Assigned {stringer} to order {order_id} successfully.")

            return make_response(jsonify({
                "status": "success", 
                "order": assigned_order.order_id
            }), 200)
        
        except ValueError as e:
            app.logger.warning(f"Assignment failed for order {order_id}: {e}")
            return make_response(jsonify({
                "status": "error", 
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Internal error assigning {stringer} to order {order_id}: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "Internal server error"
            }), 500)
        
    # @app.route('/api/orders/recommendations/<int:order_id>', methods=['GET'])
    # @login_required
    # def get_exercise_recommendations(order_id: int) -> Response:
    #     """Route to get exercise recommendations for a order.

    #     Path Parameter:
    #         - order_id (int): The ID of the order.

    #     Returns:
    #         JSON list of recommended exercises.

    #     Raises:
    #         400 if order not found.
    #         500 on external API or DB failure.
    #     """
    #     try:
    #         recommendations = orders.get_exercise_recommendations(order_id)
    #         app.logger.info(f"Retrieved exercise recommendations for order {order_id}. {recommendations}")
    #         return make_response(jsonify({
    #             "status": "success",
    #             "recommendations": recommendations
    #         }), 200)
    #     except ValueError as e:
    #         app.logger.warning(f"Recommendation fetch failed: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": str(e)
    #         }), 400)
    #     except Exception as e:
    #         app.logger.error(f"Internal error getting recommendations: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": "Internal server error"
    #         }), 500)


    # @app.route('/api/orders/log-session/<int:order_id>', methods=['POST'])
    # @login_required
    # def log_workout(order_id: int) -> Response:
    #     """Route to log a workout session for a order.

    #     Path Parameter:
    #         - order_id (int): The ID of the order.

    #     Expected JSON Input:
    #         - amount (float): Progress amount.
    #         - exercise_type (str): Exercise name.
    #         - duration (int): Time in minutes.
    #         - intensity (str): Intensity level.
    #         - note (str, optional): Personal notes.

    #     Returns:
    #         JSON message with updated progress.

    #     Raises:
    #         400 if validation fails.
    #         500 on DB error.
    #     """
    #     try:
    #         data = request.get_json()
    #         order = orders.get_order_by_id(order_id)
    #         message = order.log_workout_session(
    #             amount=data.get("amount"),
    #             exercise_type=data.get("exercise_type"),
    #             duration=data.get("duration"),
    #             intensity=data.get("intensity"),
    #             note=data.get("note", "")
    #         )
    #         app.logger.info(f"Workout logged for order {order_id}: {message}")
    #         return make_response(jsonify({
    #             "status": "success",
    #             "message": message
    #         }), 200)
    #     except ValueError as e:
    #         app.logger.warning(f"Workout log failed for order {order_id}: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": str(e)
    #         }), 400)
    #     except Exception as e:
    #         app.logger.error(f"Internal error logging workout for order {order_id}: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": "Internal server error"
    #         }), 500)


    # ############################################################
    # #
    # # Plan Add / Remove
    # #
    # ############################################################


    # @app.route('/api/add-order-to-plan/<int:order_id>', methods=['POST'])
    # @login_required
    # def add_order_to_plan(order_id: int) -> Response:
    #     """Route to add a order to the plan by order_id.

    #     Path Parameter:
    #         - order_id (int): The ID of the order.

    #     Returns:
    #         JSON response indicating success of the addition.

    #     Raises:
    #         400 error if required fields are missing or the order does not exist.
    #         500 error if there is an issue adding the order to the plan.

    #     """
    #     try:
    #         app.logger.info("Received request to add order to plan")

    #         app.logger.info(f"Looking up order with id {order_id}")
    #         order = orders.get_order_by_id(order_id=order_id)

    #         if not order:
    #             app.logger.warning(f"order not found")
    #             return make_response(jsonify({
    #                 "status": "error",
    #                 "message": f"order not found in catalog"
    #             }), 400)

    #         plan_model.add_order_to_plan(order_id)
    #         app.logger.info(f"Successfully added order to plan: {order.target} - {order.order_progress} out of {order.order_value}")

    #         return make_response(jsonify({
    #             "status": "success",
    #             "message": f"order {order.target} - {order.order_progress} out of {order.order_value} added to plan"
    #         }), 200)

    #     except Exception as e:
    #         app.logger.error(f"Failed to add order to plan: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": "An internal error occurred while adding the order to the plan",
    #             "details": str(e)
    #         }), 500)


    # @app.route('/api/remove-order-from-plan/<int:order_id>', methods=['DELETE'])
    # @login_required
    # def remove_order_by_order_id(order_id:int) -> Response:
    #     """Route to remove a order from the plan by order_id.

    #     Path Parameter:
    #         - order_id (int): The ID of the order.

    #     Returns:
    #         JSON response indicating success of the removal.

    #     Raises:
    #         400 error if required fields are missing or the order does not exist in the plan.
    #         500 error if there is an issue removing the order.

    #     """
    #     try:
    #         app.logger.info("Received request to remove order from plan")

    #         app.logger.info(f"Looking up order to remove: id - {order_id}")
    #         order = orders.get_order_by_id(order_id)

    #         if not order:
    #             app.logger.warning(f"order with id {order_id} not found in catalog")
    #             return make_response(jsonify({
    #                 "status": "error",
    #                 "message": f"order with id {order_id} not found in catalog"
    #             }), 400)

    #         plan_model.remove_order_by_order_id(order.id)
    #         app.logger.info(f"Successfully removed order with id {order_id} from plan")

    #         return make_response(jsonify({
    #             "status": "success",
    #             "message": f"order with id {order_id} removed from plan"
    #         }), 200)

    #     except Exception as e:
    #         app.logger.error(f"Failed to remove order from plan: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": "An internal error occurred while removing the order from the plan",
    #             "details": str(e)
    #         }), 500)


    # @app.route('/api/clear-plan', methods=['POST'])
    # @login_required
    # def clear_plan() -> Response:
    #     """Route to clear all orders from the plan.

    #     Returns:
    #         JSON response indicating success of the operation.

    #     Raises:
    #         500 error if there is an issue clearing the plan.

    #     """
    #     try:
    #         app.logger.info("Received request to clear the plan")

    #         plan_model.clear_plan()

    #         app.logger.info("Successfully cleared the plan")
    #         return make_response(jsonify({
    #             "status": "success",
    #             "message": "plan cleared"
    #         }), 200)

    #     except Exception as e:
    #         app.logger.error(f"Failed to clear plan: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": "An internal error occurred while clearing the plan",
    #             "details": str(e)
    #         }), 500)


    # ############################################################
    # #
    # # View plan
    # #
    # ############################################################


    # @app.route('/api/get-all-orders-from-plan', methods=['GET'])
    # @login_required
    # def get_all_orders_from_plan() -> Response:
    #     """Retrieve all orders in the plan.

    #     Returns:
    #         JSON response containing the list of orders.

    #     Raises:
    #         500 error if there is an issue retrieving the plan.

    #     """
    #     try:
    #         app.logger.info("Received request to retrieve all orders from the plan.")

    #         orders = plan_model.get_all_orders()
    #         order_ids = [order.id for order in orders]

    #         app.logger.info(f"Successfully retrieved {len(orders)} orders from the plan.")
    #         return make_response(jsonify({
    #             "status": "success",
    #             "orders": order_ids
    #         }), 200)

    #     except Exception as e:
    #         app.logger.error(f"Failed to retrieve orders from plan: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": "An internal error occurred while retrieving the plan",
    #             "details": str(e)
    #         }), 500)
        
    
    # @app.route('/api/get-plan-progress', methods=['GET'])
    # @login_required
    # def get_plan_progress() -> Response:
    #     """Retrieve progress of orders in the plan.

    #     Returns:
    #         JSON response containing the percentage of orders completed.

    #     Raises:
    #         500 error if there is an issue retrieving progress.

    #     """
    #     try:
    #         app.logger.info("Received request to get progress of the plan.")

    #         percentage = plan_model.get_plan_progress()

    #         app.logger.info(f"Successfully retrieved percentage of orders completed in the plan.")
    #         return make_response(jsonify({
    #             "status": "success",
    #             "percentage": percentage
    #         }), 200)

    #     except Exception as e:
    #         app.logger.error(f"Failed to retrieve orders from plan: {e}")
    #         return make_response(jsonify({
    #             "status": "error",
    #             "message": "An internal error occurred while retrieving the plan",
    #             "details": str(e)
    #         }), 500)

    return app

if __name__ == '__main__':
    app = create_app()
    cors = CORS(app)
    app.logger.info("Starting Flask app...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        app.logger.error(f"Flask app encountered an error: {e}")
    finally:
        app.logger.info("Flask app has stopped.")