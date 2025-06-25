# import logging
# import json 
# from sqlalchemy import Text, Integer, Float, Boolean, Date, ForeignKey

# from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# # from sqlalchemy.orm import mapped_column
# # from customerTracker.utils.api_utils import fetch_recommendation
# from typing import Optional, Union
# from datetime import date

# from RacketTracker.models.order_model import Orders

# from RacketTracker.db import db# , Base
# from RacketTracker.utils.logger import configure_logger


# logger = logging.getLogger(__name__)
# configure_logger(logger)

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
#         #     raise ValueError("Recurring goal must be a non-empty customer if provided.")
        
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
#         logger.info(f"Received request to create goal.")

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
#             logger.error(f"Database error while creating goal: {e}")
#             db.session.rollback()
#             raise 

# ##############################################
# # Delete Goals
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
# # # Get Goals 
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
#         logger.info(f"Attempting to retrieve goal with ID {customer_id}")

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
# # Update Goals
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