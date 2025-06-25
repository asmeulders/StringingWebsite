# import logging
# import json 
# from sqlalchemy import Text, Integer, Float, Boolean, Date, ForeignKey

# from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# # from sqlalchemy.orm import mapped_column
# # from RacketTracker.utils.api_utils import fetch_recommendation
# from typing import Optional, Union
# from datetime import date

# from RacketTracker.models.order_model import Orders

# from RacketTracker.db import db # , Base
# from RacketTracker.utils.logger import configure_logger


# logger = logging.getLogger(__name__)
# configure_logger(logger)

# class Rackets(db.Model):
#     """Represents a racket.

#     This model maps to the 'rackets' table and stores metadata for desired target areas.

#     Used in a Flask-SQLAlchemy application for racket management.
#     """

#     __tablename__ = "rackets"
    
#     racket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     brand = db.Column(db.Text, nullable=False)
#     model = db.Column(db.Text, nullable=False)
#     year = db.Column(db.Integer, nullable=True)
#     head_size = db.Column(db.Integer, nullable=False)
#     grip_size = db.Column(db.Float, nullable=False)
#     weight = db.Column(db.Integer, nullable=False)
#     stringing_pattern = db.Column(db.Text, nullable=False)
#     swing_weight = db.Column(db.Float, nullable=True)
#     balance = db.Column(db.Float, nullable=True)
#     stiffness = db.Column(db.Integer, nullable=True)

#     orders = db.relationship("Orders", backpopulates="racket")

#     def validate(self) -> None:
#         """Validates the racket instance before committing to the database.

#         Raises:
#             ValueError: If any required fields are invalid.
#         """
        
#         # If a field is provided, check that it's a non-empty string
#         # Checks only if field is provided (because it is nullable) and if provided, must be a non-empty string
#         # if self.recurring is not None and (not isinstance(self.recurring, str) or not self.recurring.strip()):
#         #     raise ValueError("Recurring goal must be a non-empty string if provided.")
        
#         if not self.brand or not isinstance(self.brand, str):
#             raise ValueError("brand must be a non-empty string")
#         if not self.model or not isinstance(self.model, str):
#             raise ValueError("model must be a non-empty string.")
#         if not isinstance(self.year, int) and self.year >= 1900:
#             raise ValueError("year must be a valid int.")
#         if not self.head_size or not isinstance(self.head_size, int):
#             raise ValueError("head_size must be a valid int.")
#         if not self.grip_size or not isinstance(self.grip_size, float):
#             raise ValueError("grip_size must be a valid float")
#         if not self.weight or not isinstance(self.weight, int):
#             raise ValueError("weight must be a valid integer.")
#         if not self.stringing_pattern and not isinstance(self.stringing_pattern, str):
#             raise ValueError("stringing_pattern must be a non-empty string.")
#         if not isinstance(self.swing_weight, float) and self.swing_weight >= 0:
#             raise ValueError("swing_weight must be a valid float greater than 0.")
#         if not isinstance(self.balance, float) and self.balance >= 0:
#             raise ValueError("swing_weight must be a valid float greater than 0.")
#         if not isinstance(self.stiffness, int) and self.stiffness >= 0:
#             raise ValueError("stiffness must be a valid int greater than 0.")

#     @classmethod
#     def create_racket(cls, brand: str, model: str, year: int, head_size: int, grip_size: float, weight: int, stringing_pattern: str, swing_weight: float, balance: float, stiffness: int) -> None:
#         """
#         Creates a new racket in the rackets table using SQLAlchemy.

#         Args:
#             brand (str): Brand of the racket.
#             model (str): Model of the racket.
#             year (int): Release year of the racket.
#             head_size (int): Head size of the racket.
#             grip_size (float): Grip size of the racket.
#             weight (int): Weight of the racket (grams).
#             stringing_pattern (str): Stringing pattern of the racket.
#             swing_weight (float, optional): Swing weight of the racket.
#             balance (float, optional): Balance point of the racket.
#             stiffness (int, optional): Stiffness of the racket

#         Raises:
#             ValueError: If any field is invalid. 
#             SQLAlchemyError: For any other database-related issues.
#         """
#         logger.info(f"Received request to create goal.")

#         try:
#             racket = Rackets(
#                 brand=brand,
#                 model=model,
#                 year=year,
#                 head_size=head_size,
#                 grip_size=grip_size,
#                 weight=weight,
#                 stringing_pattern=stringing_pattern,
#                 swing_weight=swing_weight,
#                 balance=balance,
#                 stiffness=stiffness
#             )
#             racket.validate()
#         except ValueError as e:
#             logger.warning(f"Validation failed: {e}")
#             raise

#         try:           
#             db.session.add(racket)
#             db.session.commit()
            
#             logger.info(f"Racket successfully created: {brand} {model} - {head_size}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while creating goal: {e}")
#             db.session.rollback()
#             raise 

# ##############################################
# # Delete Goals
# ##############################################

#     @classmethod
#     def delete_racket(cls, racket_id: int) -> None:
#         """
#         Permanently deletes an racket by ID.

#         Args:
#             racket_id (int): The ID of the racket to delete.

#         Raises:
#             ValueError: If the racket with the given ID does not exist.
#             SQLAlchemyError: For any database-related issues.
#         """
#         logger.info(f"Received request to delete racket with ID {racket_id}")

#         try:
#             racket = cls.query.get(racket_id)
#             if not racket:
#                 logger.warning(f"Attempted to delete non-existent racket with ID {racket_id}")
#                 raise ValueError(f"racket with ID {racket_id} not found")

#             db.session.delete(racket)
#             db.session.commit()
#             logger.info(f"Successfully deleted racket with ID {racket_id}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while deleting racket with ID {racket_id}: {e}")
#             db.session.rollback()
#             raise

# # ###############################################
# # # Get Goals 
# # ###############################################

#     @classmethod
#     def get_racket_by_id(cls, racket_id: int) -> "Rackets":
#         """
#         Retrieves a racket by its ID.

#         Args:
#             racket_id (int): The ID of the racket to retrieve.

#         Returns:
#             rackets: The racket instance corresponding to the ID.

#         Raises:
#             ValueError: If no racket with the given ID is found.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to retrieve goal with ID {racket_id}")

#         try:
#             racket = cls.query.get(racket_id)

#             if not racket:
#                 logger.info(f"racket with ID {racket_id} not found")
#                 raise ValueError(f"racket with ID {racket_id} not found")

#             logger.info(f"Successfully retrieved racket: ID={racket.racket_id}")
#             return racket

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving racket by ID {racket_id}: {e}")
#             raise

#     @classmethod
#     def get_all_rackets(cls) -> list[dict]:
#         """
#         Retrieves all rackets from the database as dictionaries.

#         Returns:
#             list[dict]: A list of dictionaries representing all rackets.

#         Raises:
#             SQLAlchemyError: If any database error occurs.
#         """
#         logger.info("Attempting to retrieve all rackets from the database")

#         try:
#             rackets = cls.query.all()

#             if not rackets:
#                 logger.warning("The rackets table is empty.")
#                 return []

#             results = [
#                 {
#                     "racket_id": racket.racket_id,
#                     "brand": racket.brand,
#                     "model": racket.model,
#                     "year": racket.year,
#                     "head_size": racket.head_size,
#                     "grip_size": racket.grip_size,
#                     "weight": racket.weight,
#                     "stringing_pattern": racket.stringing_pattern,
#                     "swing_weight": racket.swing_weight,
#                     "balance": racket.balance,
#                     "stiffness": racket.stiffness
#                 }
#                 for racket in rackets
#             ]

#             logger.info(f"Retrieved {len(results)} rackets from the database")
#             return results

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving all rackets: {e}")
#             raise

# ##########################################
# # Update Goals
# ##########################################
#     @classmethod
#     def update_racket(
#         cls,
#         racket_id: int,
#         brand: str,
#         model: str,
#         year: int,
#         head_size: int,
#         grip_size: float,
#         weight: int,
#         stringing_pattern: str,
#         swing_weight: float,
#         balance: float,
#         stiffness: int
#     ) -> "Rackets":
#         """
#         Updates a racket in the database by its ID.

#         Args:
#             racket_id (int): The ID of the racket to update.
#             brand (str, optional): The new brand value.
#             model (str, optional): The new model value.
#             year (int, optional): The new year value.
#             head_size (int, optional): The new head_size value.
#             grip_size (float, optional): The new grip_size value.
#             weight (int, optional): The new weight value.
#             stringing_pattern (str, optional): The new stringing_pattern value.
#             swing_weight (float, optional): The new swing_weight value.
#             balance (float, optional): The new balance value.
#             stiffness (int, optional): The new stiffness value.

#         Returns:
#             Rackets: The updated racket instance.

#         Raises:
#             ValueError: If the racket with the given ID does not exist or inputs are invalid.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to update racket with ID {racket_id}")

#         try:
#             racket = cls.query.get(racket_id)

#             if not racket:
#                 logger.warning(f"Racket with ID {racket_id} not found.")
#                 raise ValueError(f"Racket with ID {racket_id} not found.")

#             # Update only provided fields
#             if brand is not None:
#                 if not isinstance(brand, str):
#                     raise ValueError("brand must be a string.")
#                 racket.brand = brand

#             if model is not None:
#                 if not isinstance(model, str):
#                     raise ValueError("model must be a string.")
#                 racket.model = model

#             if year is not None:
#                 if not isinstance(year, int):
#                     raise ValueError("year must be an integer.")
#                 racket.year = year

#             if head_size is not None:
#                 if not isinstance(head_size, int):
#                     raise ValueError("head_size must be an integer.")
#                 racket.head_size = head_size
            
#             if grip_size is not None:
#                 if not isinstance(grip_size, float):
#                     raise ValueError("grip_size must be a float")
#                 racket.grip_size = grip_size

#             if weight is not None:
#                 if not isinstance(weight, int):
#                     raise ValueError("weight must be an integer.")
#                 racket.weight = weight
            
#             if stringing_pattern is not None:
#                 if not isinstance(stringing_pattern, str):
#                     raise ValueError("stringing_pattern must be a string.")
#                 racket.stringing_pattern = stringing_pattern

#             if swing_weight is not None:
#                 if not isinstance(swing_weight, float):
#                     raise ValueError("swing_weight must be a float.")
#                 racket.swing_weight = swing_weight

#             if balance is not None:
#                 if not isinstance(balance, float):
#                     raise ValueError("balance must be a float.")
#                 racket.balance = balance

#             if stiffness is not None:
#                 if not isinstance(stiffness, int):
#                     raise ValueError("stiffness must be an integer.")
#                 racket.stiffness = stiffness

#             db.session.commit()
#             logger.info(f"Successfully updated racket with ID {racket_id}")
#             return racket

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while updating racket with ID {racket_id}: {e}")
#             db.session.rollback()
#             raise