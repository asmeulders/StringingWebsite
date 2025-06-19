import logging
import json 
from sqlalchemy import Text, Integer, Float, Boolean, Date, ForeignKey

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import mapped_column
# from RacketTracker.utils.api_utils import fetch_recommendation
from typing import Optional, Union
from datetime import date


from RacketTracker.db import db, Base
from RacketTracker.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

class Orders(Base):
    """Represents an stringing order.

    This model maps to the 'orders' table and stores metadata for desired target areas.

    Used in a Flask-SQLAlchemy application for order management.
    """

    __tablename__ = "Orders"
    
    order_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id = mapped_column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    racket_id = mapped_column(Integer, ForeignKey('rackets.racket_id'), nullable=False)
    date = mapped_column(Date, nullable=False)
    mains_tension = mapped_column(Integer, nullable=False)
    crosses_tension = mapped_column(Integer, nullable=False, default=mains_tension)
    mains_string_id = mapped_column(Integer, ForeignKey('strings.string_id'))
    mains_string_id = mapped_column(Integer, ForeignKey('strings.string_id'), default=mains_string_id)
    paid = mapped_column(Boolean, default=False)
    compmleted = mapped_column(Boolean, default=False)

    def validate(self) -> None:
        """Validates the order instance before committing to the database.

        Raises:
            ValueError: If any required fields are invalid.
        """
        
        # If a field is provided, check that it's a non-empty string
        # Checks only if field is provided (because it is nullable) and if provided, must be a non-empty string
        # if self.recurring is not None and (not isinstance(self.recurring, str) or not self.recurring.strip()):
        #     raise ValueError("Recurring goal must be a non-empty string if provided.")
        
        if not self.target or not isinstance(self.target, str):
            raise ValueError("Target must be a non-empty string")
        if not self.goal_value or not isinstance(self.goal_value, int):
            raise ValueError("Goal value must be a valid integer.")
        if self.goal_progress is not None and not isinstance(self.goal_progress, (float, int)):
            raise ValueError("Goal progress must be a valid float or int.")
        if self.completed is None or not isinstance(self.completed, bool):
            raise ValueError("Completed must be either true or false.")

        #progress
        if self.goal_progress >= self.goal_value and not self.completed or self.goal_progress < self.goal_value and self.completed:
            raise ValueError("Goal completion mismatch.")
        try:
            notes = json.loads(self.progress_notes)
            if not isinstance(notes, list):
                raise ValueError("Progress notes must be a JSON-formatted list.")
        except (ValueError, TypeError):
            raise ValueError("Progress notes must be a valid JSON-formatted string representing a list.")

    @classmethod
    def create_order(cls, customer_id: int, racket_id: int, date: Date, mains_tension: int, crosses_tension: int, mains_string_id: int, crosses_string_id: int, paid: bool) -> None:
        """
        Creates a new order in the orders table using SQLAlchemy.

        Args:
            customer_id (int): Foreign key of the customer.
            racket_id (int): Foreign key of the racket provided.
            date (date): Date of the order.
            mains_tension (int): Tension of the mains.
            crosses_tension (int): Tension of the crosses.
            mains_string_id (int): Foreign key of the string used on the mains.
            crosses_string_id (int): Foreign key of the string used on the crosses.
            paid (bool): True if paid for by customer.

        Raises:
            ValueError: If any field is invalid. 
            SQLAlchemyError: For any other database-related issues.
        """
        logger.info(f"Received request to create goal.")

        try:
            order = Orders(
                customer_id=customer_id,
                racket_id=racket_id,
                date=date,
                mains_tension=mains_tension,
                crosses_tension=crosses_tension,
                mains_string_id=mains_string_id,
                crosses_string_id=crosses_string_id,
                paid=paid
            )
            order.validate()
        except ValueError as e:
            logger.warning(f"Validation failed: {e}")
            raise

        try:           
            db.session.add(order)
            db.session.commit()
            paid_message = "Paid" if paid else "Unpaid"
            logger.info(f"Order successfully placed: {mains_tension}. {paid_message}")

        except SQLAlchemyError as e:
            logger.error(f"Database error while creating goal: {e}")
            db.session.rollback()
            raise 

##############################################
# Delete Goals
##############################################

    @classmethod
    def delete_order(cls, order_id: int) -> None:
        """
        Permanently deletes an order by ID.

        Args:
            order_id (int): The ID of the order to delete.

        Raises:
            ValueError: If the order with the given ID does not exist.
            SQLAlchemyError: For any database-related issues.
        """
        logger.info(f"Received request to delete order with ID {order_id}")

        try:
            order = cls.query.get(order_id)
            if not order:
                logger.warning(f"Attempted to delete non-existent order with ID {order_id}")
                raise ValueError(f"Order with ID {order_id} not found")

            db.session.delete(order)
            db.session.commit()
            logger.info(f"Successfully deleted order with ID {order_id}")

        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting order with ID {order_id}: {e}")
            db.session.rollback()
            raise

#     @classmethod
#     def delete_goal_by_target(cls, target: str) -> None:
#         """
#         Permanently deletes a goal by target.

#         Args:
#             target (str): A target muscle group the user wants to work on.

#         Raises:
#             ValueError: If the goal with the given target does not exist.
#             SQLAlchemyError: For any database-related issues.
#         """
#         logger.info(f"Received request to delete goal with ID {target}")

#         try:
#             goal = cls.query.filter_by(target=target).first() 
#             if not goal:
#                 logger.warning(f"Attempted to delete non-existent goal with target {target}")
#                 raise ValueError(f"Goal with target {target} not found")

#             db.session.delete(goal)
#             db.session.commit()
#             logger.info(f"Successfully deleted goal with target {target}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while deleting goal with target {target}: {e}")
#             db.session.rollback()
#             raise

#     @classmethod
#     def delete_goal_by_goal_value(cls, goal_value: int) -> None:
#         """
#         Permanently deletes a goal by the goal value.

#         Args:
#             goal_value (int): A value the user wants to reach for a specific goal.

#         Raises:
#             ValueError: If the goal with the given goal value does not exist.
#             SQLAlchemyError: For any database-related issues.
#         """
#         logger.info(f"Received request to delete goal with goal value {goal_value}")

#         try:
#             goal = cls.query.filter_by(goal_value=goal_value).first()
#             if not goal:
#                 logger.warning(f"Attempted to delete non-existent goal with goal value {goal_value}")
#                 raise ValueError(f"Goal with goal value {goal_value} not found")

#             db.session.delete(goal)
#             db.session.commit()
#             logger.info(f"Successfully deleted goal with goal value {goal_value}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while deleting goal with goal value {goal_value}: {e}")
#             db.session.rollback()
#             raise
    
#     @classmethod
#     def delete_goal_by_completed(cls, completed: bool) -> None:
#         """
#         Permanently deletes a goal by the completion status.

#         Args:
#             completed (bool): The completion status of that goal 

#         Raises:
#             ValueError: If the goal with the given completion status does not exist.
#             SQLAlchemyError: For any database-related issues.
#         """
#         logger.info(f"Received request to delete goal with completion status {completed}")

#         try:
#             goal = cls.query.filter_by(completed=completed).first()
#             if not goal:
#                 logger.warning(f"Attempted to delete non-existent goal with completion {completed}")
#                 raise ValueError(f"Goal with completion {completed} not found")

#             db.session.delete(goal)
#             db.session.commit()
#             logger.info(f"Successfully deleted goal with completion {completed}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while deleting goal with completion {completed}: {e}")
#             db.session.rollback()
#             raise
    
# ###############################################
# # Progress Notes 
# ###############################################
#     def log_workout_session(self, amount: Union[float, int], exercise_type: str, duration: int, intensity: str, note: str = "") -> str:
#         """
#         Logs a workout session with progress and updates status.

#         Args:
#             amount (float, int): The amount to add to goal progress.
#             exercise_type (str): The type of exercise performed (e.g., "Running").
#             duration (int): The duration of the workout in minutes.
#             intensity (str): The intensity of the workout (e.g., "Low", "Moderate", "High").
#             note (str): An optional personal note about the session.

#         Raises:
#             ValueError: If the amount is not positive.
#             SQLAlchemyError: For any database-related issues.

#         Returns:
#             str: A message indicating progress update or completion.
#         """
#         logger.info("Logging workout session...")
#         if amount <= 0:
#             raise ValueError("Progress amount must be positive.")

#         if self.goal_progress is None:
#             self.goal_progress = 0.0

#         self.goal_progress += amount

#         workout_note = f"{exercise_type} - {duration} min - {intensity}"
#         if note:
#             workout_note += f" | Note: {note}"

#         logger.info(workout_note)

#         percent = ((float)(self.goal_progress) / self.goal_value) * 100

#         if self.goal_progress >= self.goal_value:
#             self.completed = True
#             message = f"Goal completed! Total progress: {percent:.1f}%"
#         else:
#             message = f"Workout logged. Progress: {percent:.1f}% complete."

#         db.session.commit()
#         return message

#     # Helper methods
#     def get_progress_notes(self) -> list[str]:
#         """Returns progress notes as a list of strings."""
#         logger.info("Getting previous progress notes...")
#         try:
#             return json.loads(self.progress_notes or "[]")
#         except (TypeError, json.JSONDecodeError):
#             return []

#     def add_progress_note(self, note: str) -> None:
#         """Appends a note to the progress_notes list."""
#         notes = self.get_progress_notes()
#         logger.info("Adding new progress notes...")
#         notes.append(note)
#         self.progress_notes = json.dumps(notes)


# ###############################################
# # Get Goals 
# ###############################################

    @classmethod
    def get_order_by_id(cls, order_id: int) -> "Orders":
        """
        Retrieves a order by its ID.

        Args:
            order_id (int): The ID of the order to retrieve.

        Returns:
            Orders: The order instance corresponding to the ID.

        Raises:
            ValueError: If no order with the given ID is found.
            SQLAlchemyError: If a database error occurs.
        """
        logger.info(f"Attempting to retrieve goal with ID {order_id}")

        try:
            order = cls.query.get(order_id)

            if not order:
                logger.info(f"Order with ID {order_id} not found")
                raise ValueError(f"Order with ID {order_id} not found")

            logger.info(f"Successfully retrieved order: ID={order.order_id}")
            return order

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving order by ID {order_id}: {e}")
            raise

#     @classmethod
#     def get_goals_by_target(cls, target: str) -> list["Goals"]:
#         """
#         Retrieves all goals matching a specific target field.

#         Args:
#             target (str): The target to search for.

#         Returns:
#             list[Goals]: A list of goal instances matching the target.

#         Raises:
#             ValueError: If no goals with the given target are found.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to retrieve all goals with target '{target}'")

#         try:
#             goals = cls.query.filter_by(target=target).all()

#             if not goals:
#                 logger.info(f"No goals found with target '{target}'")
#                 raise ValueError(f"No goals found with target '{target}'")

#             logger.info(f"Successfully retrieved {len(goals)} goal(s) with target '{target}'")
#             return goals

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving goals by target '{target}': {e}")
#             raise

#     @classmethod
#     def get_goals_by_goal_value(cls, goal_value: int) -> list["Goals"]:
#         """
#         Retrieves all goals matching a specific goal value.

#         Args:
#             goal_value (int): The goal value to search for.

#         Returns:
#             list[Goals]: A list of goal instances matching the goal value.

#         Raises:
#             ValueError: If no goals with the given goal value are found.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to retrieve all goals with goal value '{goal_value}'")

#         try:
#             goals = cls.query.filter_by(goal_value=goal_value).all()

#             if not goals:
#                 logger.info(f"No goals found with goal value '{goal_value}'")
#                 raise ValueError(f"No goals found with goal value '{goal_value}'")

#             logger.info(f"Successfully retrieved {len(goals)} goal(s) with goal value '{goal_value}'")
#             return goals

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving goals by goal value '{goal_value}': {e}")
#             raise

#     @classmethod
#     def get_goals_by_completed(cls, completed: bool) -> list["Goals"]:
#         """
#         Retrieves all goals matching completion status.

#         Args:
#             completed (bool): The completion status to search for.

#         Returns:
#             list[Goals]: A list of goal instances matching the completion status.

#         Raises:
#             ValueError: If no goals with the given completion status are found.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to retrieve all goals with completion status '{completed}'")

#         try:
#             goals = cls.query.filter_by(completed=completed).all()

#             if not goals:
#                 logger.info(f"No goals found with completion status '{completed}'")
#                 raise ValueError(f"No goals found with completion status '{completed}'")

#             logger.info(f"Successfully retrieved {len(goals)} goal(s) with completion status '{completed}'")
#             return goals

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving goals by completion status '{completed}': {e}")
#             raise

# # Recommendations
#     @classmethod
#     def get_exercise_recommendations(cls, goal_id: int) -> list[dict]:
#         """
#         Gets exercise recommendations from ExerciseDB based on a goal's target.

#         Args:
#             goal_id (int): The ID of the goal.

#         Returns:
#             list[dict]: A list of recommended exercises.

#         Raises:
#             ValueError: If the goal is not found.
#             RuntimeError: If the external API call fails.
#         """
#         logger.info(f"Fetching exercise recommendations for goal ID {goal_id}")

#         goal = cls.query.get(goal_id)
#         if not goal:
#             logger.warning(f"Goal with ID {goal_id} not found.")
#             raise ValueError(f"Goal with ID {goal_id} not found.")

#         try:
#             exercises = fetch_recommendation(goal.target)
#             logger.info(f"Successfully found {len(exercises)} exercise(s) for goal with ID {goal_id}")
#             return exercises
#         except RuntimeError as e:
#             logger.error(f"Failed to fetch exercise recommendations: {e}")
#             raise

    @classmethod
    def get_all_orders(cls) -> list[dict]:
        """
        Retrieves all orders from the database as dictionaries.

        Returns:
            list[dict]: A list of dictionaries representing all orders.

        Raises:
            SQLAlchemyError: If any database error occurs.
        """
        logger.info("Attempting to retrieve all orders from the database")

        try:
            orders = cls.query.all()

            if not orders:
                logger.warning("The orders table is empty.")
                return []

            results = [
                {
                    "order_id": order.order_id,
                    "customer_id": order.customer_id,
                    "racket__id": order.racket_id,
                    "date": order.date,
                    "mains_tension": order.mains_tension,
                    "crosses_tension": order.crosses_tension,
                    "mains_string_id": order.mains_string_id,
                    "crosses_string_id": order.mains_string_id,
                    "paid": order.paid,
                    "completed": order.completed
                }
                for order in orders
            ]

            logger.info(f"Retrieved {len(results)} order from the database")
            return results

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving all orders: {e}")
            raise

##########################################
# Update Goals
##########################################
    @classmethod
    def update_order(
        cls,
        order_id: int,
        racket_id: int,
        mains_tension: int,
        crosses_tension: int,
        mains_string_id: int,
        crosses_string_id: int,
        paid: bool,
        completed: bool
    ) -> "Orders":
        """
        Updates a order in the database by its ID.

        Args:
            goal_id (int): The ID of the goal to update.
            target (str, optional): The new target value.
            goal_value (int, optional): The new goal value.
            goal_progress ((float, int), optional): The new goal progress value.
            completed (bool, optional): The new completion status.

        Returns:
            Goals: The updated goal instance.

        Raises:
            ValueError: If the goal with the given ID does not exist or inputs are invalid.
            SQLAlchemyError: If a database error occurs.
        """
        logger.info(f"Attempting to update order with ID {order_id}")

        try:
            order = cls.query.get(order_id)

            if not order:
                logger.warning(f"Order with ID {order_id} not found.")
                raise ValueError(f"Order with ID {order_id} not found.")

            # Update only provided fields
            if racket_id is not None:
                order.racket_id = racket_id

            if mains_tension is not None:
                if not isinstance(mains_tension, int):
                    raise ValueError("mains_tension must be an integer.")
                order.mains_tension = mains_tension

            if crosses_tension is not None:
                if not isinstance(crosses_tension, int):
                    raise ValueError("crosses_tensino must be an int.")
                order.crosses_tension = crosses_tension

            if mains_string_id is not None:
                if not isinstance(mains_string_id, int):
                    raise ValueError("mains_string_id must be an integer.")
                order.mains_string_id = mains_string_id

            if crosses_string_id is not None:
                if not isinstance(crosses_string_id, int):
                    raise ValueError("crosses_string_id must be an int.")
                order.crosses_string_id = crosses_string_id
            
            if paid is not None:
                if not isinstance(paid, bool):
                    raise ValueError("paid must be a boolean")
                order.paid = paid

            if completed is not None:
                if not isinstance(completed, bool):
                    raise ValueError("completed must be a boolean.")
                order.completed = completed

            db.session.commit()
            logger.info(f"Successfully updated order with ID {order_id}")
            return order

        except SQLAlchemyError as e:
            logger.error(f"Database error while updating order with ID {order_id}: {e}")
            db.session.rollback()
            raise

    # def log_progress(self, amount: Union[float, int]) -> str:
    #     """
    #     Logs workout progress toward a goal, updates completion status, and calculates percentage progress.

    #     Args:
    #         amount (float): The amount of progress to add.

    #     Returns:
    #         str: A message indicating the current progress percentage or goal completion.

    #     Raises:
    #         ValueError: If the amount is invalid or negative.
    #     """
    #     if amount <= 0:
    #         raise ValueError("Progress amount must be positive.")

    #     if self.goal_progress is None:
    #         self.goal_progress = 0.0

    #     self.goal_progress += amount

    #     progress_percent = ((float)(self.goal_progress) / self.goal_value) * 100

    #     if self.goal_progress >= self.goal_value:
    #         self.completed = True
    #         message = f"Goal completed! Progress: {progress_percent:.1f}%"
    #     else:
    #         #self.completed = False
    #         message = f"Progress updated: {progress_percent:.1f}% complete."

    #     db.session.commit() 
    #     return message