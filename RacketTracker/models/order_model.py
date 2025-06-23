import logging
import json 
from sqlalchemy import Text, Integer, Float, Boolean, Date, ForeignKey

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql.expression import select
# from sqlalchemy.orm import mapped_column
# from RacketTracker.utils.api_utils import fetch_recommendation
from typing import Optional, Union
from datetime import date

# from RacketTracker.models.customer_model import Customers
# from RacketTracker.models.string_model import Strings
# from RacketTracker.models.racket_model import Rackets

from RacketTracker.db import db #, Base
from RacketTracker.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)



# class Customers(db.Model):
#     """Represents a customer.

#     This model maps to the 'customers' table and stores metadata for desired target areas.

#     Used in a Flask-SQLAlchemy application for customer management.
#     """

#     __tablename__ = "customers"
    
#     customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.Text, nullable=False)
#     phone_number = db.Column(db.Integer, nullable=False)
    
#     orders = db.relationship("Orders", back_populates="customer")

#     def validate(self) -> None:
#         """Validates the customer instance before committing to the database.

#         Raises:
#             ValueError: If any required fields are invalid.
#         """
        
#         # If a field is provided, check that it's a non-empty customer
#         # Checks only if field is provided (because it is nullable) and if provided, must be a non-empty customer
#         # if self.recurring is not None and (not isinstance(self.recurring, str) or not self.recurring.strip()):
#         #     raise ValueError("Recurring order must be a non-empty customer if provided.")
        
#         if not self.name or not isinstance(self.name, str):
#             raise ValueError("name must be a non-empty string")
#         if not self.phone_number or not isinstance(self.model, int) and self.phone_number >= 1000000000:
#             raise ValueError("model must be a valid integer.")
        
#     @classmethod
#     def create_customer(cls, name: str, phone_number: int) -> None:
#         """
#         Creates a new customer in the customers table using SQLAlchemy.

#         Args:
#             name (str): Name of the customer.
#             phone_number (int): Phone number of the customer.

#         Raises:
#             ValueError: If any field is invalid. 
#             SQLAlchemyError: For any other database-related issues.
#         """
#         logger.info(f"Received request to create order.")

#         try:
#             customer = Customers(
#                 name=name,
#                 phone_number=phone_number
#             )
#             customer.validate()
#         except ValueError as e:
#             logger.warning(f"Validation failed: {e}")
#             raise

#         try:           
#             db.session.add(customer)
#             db.session.commit()
            
#             logger.info(f"Customer successfully created: {name}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while creating order: {e}")
#             db.session.rollback()
#             raise 

# ##############################################
# # Delete orders
# ##############################################

#     @classmethod
#     def delete_customer(cls, customer_id: int) -> None:
#         """
#         Permanently deletes an customer by ID.

#         Args:
#             customer_id (int): The ID of the customer to delete.

#         Raises:
#             ValueError: If the customer with the given ID does not exist.
#             SQLAlchemyError: For any database-related issues.
#         """
#         logger.info(f"Received request to delete customer with ID {customer_id}")

#         try:
#             customer = cls.query.get(customer_id)
#             if not customer:
#                 logger.warning(f"Attempted to delete non-existent customer with ID {customer_id}")
#                 raise ValueError(f"customer with ID {customer_id} not found")

#             db.session.delete(customer)
#             db.session.commit()
#             logger.info(f"Successfully deleted customer with ID {customer_id}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while deleting customer with ID {customer_id}: {e}")
#             db.session.rollback()
#             raise

# # ###############################################
# # # Get orders 
# # ###############################################

#     @classmethod
#     def get_customer_by_id(cls, customer_id: int) -> "Customers":
#         """
#         Retrieves a customer by its ID.

#         Args:
#             customer_id (int): The ID of the customer to retrieve.

#         Returns:
#             customers: The customer instance corresponding to the ID.

#         Raises:
#             ValueError: If no customer with the given ID is found.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to retrieve order with ID {customer_id}")

#         try:
#             customer = cls.query.get(customer_id)

#             if not customer:
#                 logger.info(f"customer with ID {customer_id} not found")
#                 raise ValueError(f"customer with ID {customer_id} not found")

#             logger.info(f"Successfully retrieved customer: ID={customer.customer_id}")
#             return customer

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving customer by ID {customer_id}: {e}")
#             raise

#     @classmethod
#     def get_all_customers(cls) -> list[dict]:
#         """
#         Retrieves all customers from the database as dictionaries.

#         Returns:
#             list[dict]: A list of dictionaries representing all customers.

#         Raises:
#             SQLAlchemyError: If any database error occurs.
#         """
#         logger.info("Attempting to retrieve all customers from the database")

#         try:
#             customers = cls.query.all()

#             if not customers:
#                 logger.warning("The customers table is empty.")
#                 return []

#             results = [
#                 {
#                     "customer_id": customer.customer_id,
#                     "name": customer.name,
#                     "phone_number": customer.phone_number
#                 }
#                 for customer in customers
#             ]

#             logger.info(f"Retrieved {len(results)} customers from the database")
#             return results

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving all customers: {e}")
#             raise

# ##########################################
# # Update orders
# ##########################################
#     @classmethod
#     def update_customer(
#         cls,
#         customer_id: int,
#         name: str,
#         phone_number: str
#     ) -> "Customers":
#         """
#         Updates a customer in the database by its ID.

#         Args:
#             customer_id (int): The ID of the customer to update.
#             name (str, optional): The new name value.
#             phone_number (int, optional): The new phone_number value.
        
#         Returns:
#             Customers: The updated customer instance.

#         Raises:
#             ValueError: If the customer with the given ID does not exist or inputs are invalid.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to update customer with ID {customer_id}")

#         try:
#             customer = cls.query.get(customer_id)

#             if not customer:
#                 logger.warning(f"Customer with ID {customer_id} not found.")
#                 raise ValueError(f"Customer with ID {customer_id} not found.")

#             # Update only provided fields
#             if name is not None:
#                 if not isinstance(name, str):
#                     raise ValueError("name must be a string.")
#                 customer.name = name

#             if phone_number is not None:
#                 if not isinstance(phone_number, str):
#                     raise ValueError("phone_number must be a valid integer.")
#                 customer.phone_number = phone_number

#             db.session.commit()
#             logger.info(f"Successfully updated customer with ID {customer_id}")
#             return customer

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while updating customer with ID {customer_id}: {e}")
#             db.session.rollback()
#             raise

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

#     orders = db.relationship("Orders", back_populates="racket")

#     def validate(self) -> None:
#         """Validates the racket instance before committing to the database.

#         Raises:
#             ValueError: If any required fields are invalid.
#         """
        
#         # If a field is provided, check that it's a non-empty string
#         # Checks only if field is provided (because it is nullable) and if provided, must be a non-empty string
#         # if self.recurring is not None and (not isinstance(self.recurring, str) or not self.recurring.strip()):
#         #     raise ValueError("Recurring order must be a non-empty string if provided.")
        
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
#         logger.info(f"Received request to create order.")

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
#             logger.error(f"Database error while creating order: {e}")
#             db.session.rollback()
#             raise 

# ##############################################
# # Delete orders
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
# # # Get orders 
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
#         logger.info(f"Attempting to retrieve order with ID {racket_id}")

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
# # Update orders
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

# # class Strings(db.Model):
#     """Represents a string.

#     This model maps to the 'strings' table and stores metadata for desired target areas.

#     Used in a Flask-SQLAlchemy application for string management.
#     """

#     __tablename__ = "strings"
    
#     string_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     brand = db.Column(db.Text, nullable=False)
#     model = db.Column(db.Text, nullable=False)
#     gauge = db.Column(db.Integer, nullable=True)
#     shape = db.Column(db.Text, nullable=True)
#     type = db.Column(db.Text, nullable=False)

#     def validate(self) -> None:
#         """Validates the string instance before committing to the database.

#         Raises:
#             ValueError: If any required fields are invalid.
#         """
        
#         # If a field is provided, check that it's a non-empty string
#         # Checks only if field is provided (because it is nullable) and if provided, must be a non-empty string
#         # if self.recurring is not None and (not isinstance(self.recurring, str) or not self.recurring.strip()):
#         #     raise ValueError("Recurring order must be a non-empty string if provided.")
        
#         if not self.brand or not isinstance(self.brand, str):
#             raise ValueError("brand must be a non-empty string")
#         if not self.model or not isinstance(self.model, str):
#             raise ValueError("model must be a non-empty string.")
#         if not self.gauge or not isinstance(self.gauge, int) and self.gauge >= 0:
#             raise ValueError("gauge must be a valid integer greater than 0.")
#         if not isinstance(self.shape, str):
#             raise ValueError("shape must be a string.")
#         if not self.type or not isinstance(self.type, str):
#             raise ValueError("type must be a non-empty string.")
        
#     @classmethod
#     def create_string(cls, brand: str, model: str, gauge: int, shape: str, type: str) -> None:
#         """
#         Creates a new string in the strings table using SQLAlchemy.

#         Args:
#             brand (str): Brand of the string.
#             model (str): Model of the string.
#             gauge (int): Gauge of the string.
#             shape (str, optional): Shape of the string.
#             type (str): Type size of the string.

#         Raises:
#             ValueError: If any field is invalid. 
#             SQLAlchemyError: For any other database-related issues.
#         """
#         logger.info(f"Received request to create order.")

#         try:
#             string = Strings(
#                 brand=brand,
#                 model=model,
#                 gauge=gauge,
#                 shape=shape,
#                 type=type
#             )
#             string.validate()
#         except ValueError as e:
#             logger.warning(f"Validation failed: {e}")
#             raise

#         try:           
#             db.session.add(string)
#             db.session.commit()
            
#             logger.info(f"string successfully created: {brand} {model} - {type}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while creating order: {e}")
#             db.session.rollback()
#             raise 

# ##############################################
# # Delete orders
# ##############################################

#     @classmethod
#     def delete_string(cls, string_id: int) -> None:
#         """
#         Permanently deletes an string by ID.

#         Args:
#             string_id (int): The ID of the string to delete.

#         Raises:
#             ValueError: If the string with the given ID does not exist.
#             SQLAlchemyError: For any database-related issues.
#         """
#         logger.info(f"Received request to delete string with ID {string_id}")

#         try:
#             string = cls.query.get(string_id)
#             if not string:
#                 logger.warning(f"Attempted to delete non-existent string with ID {string_id}")
#                 raise ValueError(f"string with ID {string_id} not found")

#             db.session.delete(string)
#             db.session.commit()
#             logger.info(f"Successfully deleted string with ID {string_id}")

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while deleting string with ID {string_id}: {e}")
#             db.session.rollback()
#             raise

# # ###############################################
# # # Get orders 
# # ###############################################

#     @classmethod
#     def get_string_by_id(cls, string_id: int) -> "Strings":
#         """
#         Retrieves a string by its ID.

#         Args:
#             string_id (int): The ID of the string to retrieve.

#         Returns:
#             strings: The string instance corresponding to the ID.

#         Raises:
#             ValueError: If no string with the given ID is found.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to retrieve order with ID {string_id}")

#         try:
#             string = cls.query.get(string_id)

#             if not string:
#                 logger.info(f"string with ID {string_id} not found")
#                 raise ValueError(f"string with ID {string_id} not found")

#             logger.info(f"Successfully retrieved string: ID={string.string_id}")
#             return string

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving string by ID {string_id}: {e}")
#             raise

#     @classmethod
#     def get_all_strings(cls) -> list[dict]:
#         """
#         Retrieves all strings from the database as dictionaries.

#         Returns:
#             list[dict]: A list of dictionaries representing all strings.

#         Raises:
#             SQLAlchemyError: If any database error occurs.
#         """
#         logger.info("Attempting to retrieve all strings from the database")

#         try:
#             strings = cls.query.all()

#             if not strings:
#                 logger.warning("The strings table is empty.")
#                 return []

#             results = [
#                 {
#                     "string_id": string.string_id,
#                     "brand": string.brand,
#                     "model": string.model,
#                     "gauge": string.gauge,
#                     "shape": string.shape,
#                     "type": string.type
#                 }
#                 for string in strings
#             ]

#             logger.info(f"Retrieved {len(results)} strings from the database")
#             return results

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while retrieving all strings: {e}")
#             raise

# ##########################################
# # Update orders
# ##########################################
#     @classmethod
#     def update_string(
#         cls,
#         string_id: int,
#         brand: str,
#         model: str,
#         gauge: int,
#         shape: str,
#         type: str
#     ) -> "Strings":
#         """
#         Updates a string in the database by its ID.

#         Args:
#             string_id (int): The ID of the string to update.
#             brand (str, optional): The new brand value.
#             model (str, optional): The new model value.
#             gauge (int, optional): The new gauge value.
#             shape (str, optional): The new shape value.
#             type (str, optional): The new type value.
        
#         Returns:
#             Strings: The updated string instance.

#         Raises:
#             ValueError: If the string with the given ID does not exist or inputs are invalid.
#             SQLAlchemyError: If a database error occurs.
#         """
#         logger.info(f"Attempting to update string with ID {string_id}")

#         try:
#             string = cls.query.get(string_id)

#             if not string:
#                 logger.warning(f"String with ID {string_id} not found.")
#                 raise ValueError(f"String with ID {string_id} not found.")

#             # Update only provided fields
#             if brand is not None:
#                 if not isinstance(brand, str):
#                     raise ValueError("brand must be a string.")
#                 string.brand = brand

#             if model is not None:
#                 if not isinstance(model, str):
#                     raise ValueError("model must be a string.")
#                 string.model = model

#             if gauge is not None:
#                 if not isinstance(gauge, int):
#                     raise ValueError("gauge must be an integer.")
#                 string.gauge = gauge

#             if shape is not None:
#                 if not isinstance(shape, str):
#                     raise ValueError("shape must be a string.")
#                 string.shape = shape
            
#             if type is not None:
#                 if not isinstance(type, str):
#                     raise ValueError("type must be a string")
#                 string.type = type

#             db.session.commit()
#             logger.info(f"Successfully updated string with ID {string_id}")
#             return string

#         except SQLAlchemyError as e:
#             logger.error(f"Database error while updating string with ID {string_id}: {e}")
#             db.session.rollback()
#             raise

class Orders(db.Model):
    """Represents an stringing order.

    This model maps to the 'orders' table and stores metadata for desired target areas.

    Used in a Flask-SQLAlchemy application for order management.
    """

    __tablename__ = "orders"
    
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer = db.Column(db.Text, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    racket = db.Column(db.Text, nullable=False)
    mains_tension = db.Column(db.Integer, nullable=False)
    crosses_tension = db.Column(db.Integer, nullable=True)
    mains_string = db.Column(db.Text, nullable=False)
    crosses_string = db.Column(db.Text, nullable=True)
    paid = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)

    def validate(self) -> None:
        """Validates the order instance before committing to the database.

        Raises:
            ValueError: If any required fields are invalid.
        """
        
        # If a field is provided, check that it's a non-empty string
        # Checks only if field is provided (because it is nullable) and if provided, must be a non-empty string
        # if self.recurring is not None and (not isinstance(self.recurring, str) or not self.recurring.strip()):
        #     raise ValueError("Recurring order must be a non-empty string if provided.")
        
        if not self.customer or not isinstance(self.customer, str):
            raise ValueError("customer must be a non-empty string.")
        if not self.order_date or not isinstance(self.order_date, date):
            raise ValueError("date must be a date object.")
        if not self.racket or not isinstance(self.racket, str):
            raise ValueError("racket must be a non-empty string.")
        if not self.mains_tension or not isinstance(self.mains_tension, int):
            raise ValueError("mains_tension must be a valid integer.")
        if not isinstance(self.crosses_tension, int):
            raise ValueError("crosses_tension must be a valid integer.")
        if not self.mains_string or not isinstance(self.mains_string, str):
            raise ValueError("mains_string must be a non-empty string.")
        if not isinstance(self.crosses_string, str):
            raise ValueError("crosses_string must be a non-empty string.")
        if self.paid is None or not isinstance(self.paid, bool):
            raise ValueError("paid must be either true or false.")
        if self.completed is None or not isinstance(self.completed, bool):
            raise ValueError("completed must be either true or false.")

    @classmethod
    def create_order(cls, customer: str, order_date: date, racket: str, mains_tension: int, crosses_tension: int, mains_string: str, crosses_string: str, paid: bool = False, completed: bool = False) -> None:
        """
        Creates a new order in the orders table using SQLAlchemy.

        Args:
            customer (str): Name of the customer.
            order_date (date): Date of the order.
            racket (str): Name of the racket provided.
            mains_tension (int): Tension of the mains.
            crosses_tension (int, optional): Tension of the crosses.
            mains_string (int): Name of the string used on the mains.
            crosses_string (int, optional): Name of the string used on the crosses.
            paid (bool, optional): Paid status of the order.
            completed (bool, optional): Completion status of the racket stringing.

        Raises:
            ValueError: If any field is invalid. 
            SQLAlchemyError: For any other database-related issues.
        """
        logger.info(f"Received request to create order.")

        try:
            order = Orders(
                customer=customer,
                order_date=order_date,
                racket=racket,
                mains_tension=mains_tension,
                crosses_tension=crosses_tension,
                mains_string=mains_string,
                crosses_string=crosses_string,
                paid=paid,
                completed=completed
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
            logger.error(f"Database error while creating order: {e}")
            db.session.rollback()
            raise 

##############################################
# Delete orders
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
            order = db.session.get(cls, order_id)
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

    @classmethod
    def delete_order_by_customer(cls, customer: str) -> None:
        """
        Permanently deletes an order by customer.

        Args:
            customer (str): The name of the customer.

        Raises:
            ValueError: If the order with the given customer does not exist.
            SQLAlchemyError: For any database-related issues.
        """
        logger.info(f"Received request to delete order with customer {customer}")

        try:
            order = cls.query.filter_by(customer=customer).first() 
            if not order:
                logger.warning(f"Attempted to delete non-existent order with customer {customer}")
                raise ValueError(f"Order with target {customer} not found")

            db.session.delete(order)
            db.session.commit()
            logger.info(f"Successfully deleted order with customer {customer}")

        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting order with target {customer}: {e}")
            db.session.rollback()
            raise

    @classmethod
    def delete_order_by_order_date(cls, order_date: date) -> None:
        """
        Permanently deletes an order by the order date.

        Args:
            order_date (int): The date of a given order.

        Raises:
            ValueError: If the order with the given order value does not exist.
            SQLAlchemyError: For any database-related issues.
        """
        logger.info(f"Received request to delete order with date {order_date.strftime('%m/%d/%Y')}")

        try:
            order = cls.query.filter_by(order_date=order_date).first()
            if not order:
                logger.warning(f"Attempted to delete non-existent order with date {order_date.strftime('%m/%d/%Y')}")
                raise ValueError(f"Order with order value {order_date.strftime('%m/%d/%Y')} not found")

            db.session.delete(order)
            db.session.commit()
            logger.info(f"Successfully deleted order with date {order_date.strftime('%m/%d/%Y')}")

        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting order with date {order_date.strftime('%m/%d/%Y')}: {e}")
            db.session.rollback()
            raise
    
    @classmethod
    def delete_order_by_completed(cls, completed: bool) -> None:
        """
        Permanently deletes a order by the completion status.

        Args:
            completed (bool): The completion status of that order. 

        Raises:
            ValueError: If the order with the given completion status does not exist.
            SQLAlchemyError: For any database-related issues.
        """
        logger.info(f"Received request to delete order with completion status {completed}")

        try:
            order = cls.query.filter_by(completed=completed).first()
            if not order:
                logger.warning(f"Attempted to delete non-existent order with completion {completed}")
                raise ValueError(f"Order with completion {completed} not found")

            db.session.delete(order)
            db.session.commit()
            logger.info(f"Successfully deleted order with completion {completed}")

        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting order with completion {completed}: {e}")
            db.session.rollback()
            raise
    
# ###############################################
# # Progress Notes 
# ###############################################
#     def log_workout_session(self, amount: Union[float, int], exercise_type: str, duration: int, intensity: str, note: str = "") -> str:
#         """
#         Logs a workout session with progress and updates status.

#         Args:
#             amount (float, int): The amount to add to order progress.
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

#         if self.order_progress is None:
#             self.order_progress = 0.0

#         self.order_progress += amount

#         workout_note = f"{exercise_type} - {duration} min - {intensity}"
#         if note:
#             workout_note += f" | Note: {note}"

#         logger.info(workout_note)

#         percent = ((float)(self.order_progress) / self.order_value) * 100

#         if self.order_progress >= self.order_value:
#             self.completed = True
#             message = f"order completed! Total progress: {percent:.1f}%"
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
# # Get orders 
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
        logger.info(f"Attempting to retrieve order with ID {order_id}")

        try:
            order = db.session.get(cls, order_id)

            if not order:
                logger.info(f"Order with ID {order_id} not found")
                raise ValueError(f"Order with ID {order_id} not found")

            logger.info(f"Successfully retrieved order: ID={order.order_id}")
            return order

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving order by ID {order_id}: {e}")
            raise

    @classmethod
    def get_orders_by_customer(cls, customer: str) -> list["Orders"]:
        """
        Retrieves all orders for a given customer.

        Args:
            customer (str): The customer whose orders we retrieve.

        Returns:
            list[Orders]: A list of order instances matching the target.

        Raises:
            ValueError: If no order with the given target are found.
            SQLAlchemyError: If a database error occurs.
        """
        logger.info(f"Attempting to retrieve all orders for customer '{customer}'")

        try:
            orders: list = cls.query.filter_by(customer=customer).all()

            if not orders:
                logger.info(f"No orders found for customer '{customer}'")
                raise ValueError(f"No orders found for customer '{customer}'")

            logger.info(f"Successfully retrieved {len(orders)} order(s) for customer '{customer}'")
            return orders

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving orders for customer '{customer}': {e}")
            raise

    @classmethod
    def get_orders_by_order_date(cls, order_date: date) -> list["Orders"]:
        """
        Retrieves all orders matching a specific order date.

        Args:
            order_date (date): The date to search for.

        Returns:
            list[Orders]: A list of order instances matching the date.

        Raises:
            ValueError: If no orders with the given date are found.
            SQLAlchemyError: If a database error occurs.
        """
        logger.info(f"Attempting to retrieve all orders with date '{order_date.strftime('%m/%d/%Y')}'")

        try:
            orders = cls.query.filter_by(order_date=order_date).all()

            if not orders:
                logger.info(f"No orders found with date '{order_date.strftime('%m/%d/%Y')}'")
                raise ValueError(f"No orders found with date '{order_date.strftime('%m/%d/%Y')}'")

            logger.info(f"Successfully retrieved {len(orders)} order(s) with order value '{order_date.strftime('%m/%d/%Y')}'")
            return orders

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving orders by date '{order_date.strftime('%m/%d/%Y')}': {e}")
            raise

    @classmethod
    def get_orders_by_completed(cls, completed: bool) -> list["Orders"]:
        """
        Retrieves all orders matching completion status.

        Args:
            completed (bool): The completion status to search for.

        Returns:
            list[orders]: A list of order instances matching the completion status.

        Raises:
            ValueError: If no orders with the given completion status are found.
            SQLAlchemyError: If a database error occurs.
        """
        logger.info(f"Attempting to retrieve all orders with completion status '{completed}'")

        try:
            orders = cls.query.filter_by(completed=completed).all()

            if not orders:
                logger.info(f"No orders found with completion status '{completed}'")
                raise ValueError(f"No orders found with completion status '{completed}'")

            logger.info(f"Successfully retrieved {len(orders)} order(s) with completion status '{completed}'")
            return orders

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving orders by completion status '{completed}': {e}")
            raise

# # Recommendations
#     @classmethod
#     def get_exercise_recommendations(cls, order_id: int) -> list[dict]:
#         """
#         Gets exercise recommendations from ExerciseDB based on a order's target.

#         Args:
#             order_id (int): The ID of the order.

#         Returns:
#             list[dict]: A list of recommended exercises.

#         Raises:
#             ValueError: If the order is not found.
#             RuntimeError: If the external API call fails.
#         """
#         logger.info(f"Fetching exercise recommendations for order ID {order_id}")

#         order = cls.query.get(order_id)
#         if not order:
#             logger.warning(f"order with ID {order_id} not found.")
#             raise ValueError(f"order with ID {order_id} not found.")

#         try:
#             exercises = fetch_recommendation(order.target)
#             logger.info(f"Successfully found {len(exercises)} exercise(s) for order with ID {order_id}")
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
            orders: list = db.session.scalars(select(cls)).all() # db.session.all()

            if not orders:
                logger.warning("The orders table is empty.")
                return []

            results = [
                {
                    "order_id": order.order_id,
                    "customer": order.customer,
                    "order_date": order.order_date,
                    "racket": order.racket,
                    "mains_tension": order.mains_tension,
                    "crosses_tension": order.crosses_tension,
                    "mains_string": order.mains_string,
                    "crosses_string": order.crosses_string,
                    "paid": order.paid,
                    "completed": order.completed
                }
                for order in orders
            ]

            logger.info(f"Retrieved {len(results)} orders from the database")
            return results

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving all orders: {e}")
            raise

##########################################
# Update orders
##########################################
    @classmethod
    def update_order(
        cls,
        order_id: int,
        customer: str = None,
        order_date: date = None,
        racket: int = None,
        mains_tension: int = None,
        crosses_tension: int = None,
        mains_string: int = None,
        crosses_string: int = None,
        paid: bool = None,
        completed: bool = None
    ) -> "Orders":
        """
        Updates a order in the database by its ID.

        Args:
            order_id (int): The ID of the order to update.
            customer (int, optional): The new customer value.
            order_date (Date, optional): The new date.
            racket (int, optional): The new racket value.
            mains_tension (int, optional): The new mains_tension value.
            crosses_tension (int, optional): The new crosses_tension value.
            mains_string (str, optional): The new mains_string value.
            crosses_string (int, optional): The new crosses_string value.
            paid (bool, optional): The new paid status.
            completed (bool, optional): The new completion status.

        Returns:
            Orders: The updated order instance.

        Raises:
            ValueError: If the order with the given ID does not exist or inputs are invalid.
            SQLAlchemyError: If a database error occurs.
        """
        logger.info(f"Attempting to update order with ID {order_id}")

        try:
            order: Orders = db.session.get(cls, order_id)

            if not order:
                logger.warning(f"Order with ID {order_id} not found.")
                raise ValueError(f"Order with ID {order_id} not found.")

            # Update only provided fields
            if customer is not None:
                if not isinstance(customer, str):
                    raise ValueError("customer must be an string.")
                order.customer = customer

            if order_date is not None:
                if not isinstance(order_date, str):
                    raise ValueError("order_date must be a date object.")
                order.order_date = order_date

            if racket is not None:
                if not isinstance(racket, str):
                    raise ValueError("racket must be an string.")
                order.racket = racket

            if mains_tension is not None:
                if not isinstance(mains_tension, int):
                    raise ValueError("mains_tension must be an integer.")
                order.mains_tension = mains_tension

            if crosses_tension is not None:
                if not isinstance(crosses_tension, int):
                    raise ValueError("crosses_tension must be an int.")
                order.crosses_tension = crosses_tension

            if mains_string is not None:
                if not isinstance(mains_string, str):
                    raise ValueError("mains_string must be an string.")
                order.mains_string = mains_string

            if crosses_string is not None:
                if not isinstance(crosses_string, str):
                    raise ValueError("crosses_string must be a string.")
                order.crosses_string = crosses_string
            
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
    #     Logs workout progress toward a order, updates completion status, and calculates percentage progress.

    #     Args:
    #         amount (float): The amount of progress to add.

    #     Returns:
    #         str: A message indicating the current progress percentage or order completion.

    #     Raises:
    #         ValueError: If the amount is invalid or negative.
    #     """
    #     if amount <= 0:
    #         raise ValueError("Progress amount must be positive.")

    #     if self.order_progress is None:
    #         self.order_progress = 0.0

    #     self.order_progress += amount

    #     progress_percent = ((float)(self.order_progress) / self.order_value) * 100

    #     if self.order_progress >= self.order_value:
    #         self.completed = True
    #         message = f"order completed! Progress: {progress_percent:.1f}%"
    #     else:
    #         #self.completed = False
    #         message = f"Progress updated: {progress_percent:.1f}% complete."

    #     db.session.commit() 
    #     return message