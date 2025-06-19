import logging
import json 
from sqlalchemy import Text, Integer, Float, Boolean, Date, ForeignKey

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import mapped_column
# from stringTracker.utils.api_utils import fetch_recommendation
from typing import Optional, Union
from datetime import date


from RacketTracker.db import db, Base
from RacketTracker.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

class Strings(Base):
    """Represents a string.

    This model maps to the 'strings' table and stores metadata for desired target areas.

    Used in a Flask-SQLAlchemy application for string management.
    """

    __tablename__ = "strings"
    
    string_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand = mapped_column(Text, nullable=False)
    model = mapped_column(Text, nullable=False)
    gauge = mapped_column(Integer, nullable=True)
    shape = mapped_column(Text, nullable=True)
    type = mapped_column(Text, nullable=False)

    def validate(self) -> None:
        """Validates the string instance before committing to the database.

        Raises:
            ValueError: If any required fields are invalid.
        """
        
        # If a field is provided, check that it's a non-empty string
        # Checks only if field is provided (because it is nullable) and if provided, must be a non-empty string
        # if self.recurring is not None and (not isinstance(self.recurring, str) or not self.recurring.strip()):
        #     raise ValueError("Recurring goal must be a non-empty string if provided.")
        
        if not self.brand or not isinstance(self.brand, str):
            raise ValueError("brand must be a non-empty string")
        if not self.model or not isinstance(self.model, str):
            raise ValueError("model must be a non-empty string.")
        if not self.gauge or not isinstance(self.gauge, int) and self.gauge >= 0:
            raise ValueError("gauge must be a valid integer greater than 0.")
        if not isinstance(self.shape, str):
            raise ValueError("shape must be a string.")
        if not self.type or not isinstance(self.type, str):
            raise ValueError("type must be a non-empty string.")
        
    @classmethod
    def create_string(cls, brand: str, model: str, gauge: int, shape: str, type: str) -> None:
        """
        Creates a new string in the strings table using SQLAlchemy.

        Args:
            brand (str): Brand of the string.
            model (str): Model of the string.
            gauge (int): Gauge of the string.
            shape (str, optional): Shape of the string.
            type (str): Type size of the string.

        Raises:
            ValueError: If any field is invalid. 
            SQLAlchemyError: For any other database-related issues.
        """
        logger.info(f"Received request to create goal.")

        try:
            string = Strings(
                brand=brand,
                model=model,
                gauge=gauge,
                shape=shape,
                type=type
            )
            string.validate()
        except ValueError as e:
            logger.warning(f"Validation failed: {e}")
            raise

        try:           
            db.session.add(string)
            db.session.commit()
            
            logger.info(f"string successfully created: {brand} {model} - {type}")

        except SQLAlchemyError as e:
            logger.error(f"Database error while creating goal: {e}")
            db.session.rollback()
            raise 

##############################################
# Delete Goals
##############################################

    @classmethod
    def delete_string(cls, string_id: int) -> None:
        """
        Permanently deletes an string by ID.

        Args:
            string_id (int): The ID of the string to delete.

        Raises:
            ValueError: If the string with the given ID does not exist.
            SQLAlchemyError: For any database-related issues.
        """
        logger.info(f"Received request to delete string with ID {string_id}")

        try:
            string = cls.query.get(string_id)
            if not string:
                logger.warning(f"Attempted to delete non-existent string with ID {string_id}")
                raise ValueError(f"string with ID {string_id} not found")

            db.session.delete(string)
            db.session.commit()
            logger.info(f"Successfully deleted string with ID {string_id}")

        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting string with ID {string_id}: {e}")
            db.session.rollback()
            raise

# ###############################################
# # Get Goals 
# ###############################################

    @classmethod
    def get_string_by_id(cls, string_id: int) -> "Strings":
        """
        Retrieves a string by its ID.

        Args:
            string_id (int): The ID of the string to retrieve.

        Returns:
            strings: The string instance corresponding to the ID.

        Raises:
            ValueError: If no string with the given ID is found.
            SQLAlchemyError: If a database error occurs.
        """
        logger.info(f"Attempting to retrieve goal with ID {string_id}")

        try:
            string = cls.query.get(string_id)

            if not string:
                logger.info(f"string with ID {string_id} not found")
                raise ValueError(f"string with ID {string_id} not found")

            logger.info(f"Successfully retrieved string: ID={string.string_id}")
            return string

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving string by ID {string_id}: {e}")
            raise

    @classmethod
    def get_all_strings(cls) -> list[dict]:
        """
        Retrieves all strings from the database as dictionaries.

        Returns:
            list[dict]: A list of dictionaries representing all strings.

        Raises:
            SQLAlchemyError: If any database error occurs.
        """
        logger.info("Attempting to retrieve all strings from the database")

        try:
            strings = cls.query.all()

            if not strings:
                logger.warning("The strings table is empty.")
                return []

            results = [
                {
                    "string_id": string.string_id,
                    "brand": string.brand,
                    "model": string.model,
                    "gauge": string.gauge,
                    "shape": string.shape,
                    "type": string.type
                }
                for string in strings
            ]

            logger.info(f"Retrieved {len(results)} strings from the database")
            return results

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving all strings: {e}")
            raise

##########################################
# Update Goals
##########################################
    @classmethod
    def update_string(
        cls,
        string_id: int,
        brand: str,
        model: str,
        gauge: int,
        shape: str,
        type: str
    ) -> "Strings":
        """
        Updates a string in the database by its ID.

        Args:
            string_id (int): The ID of the string to update.
            brand (str, optional): The new brand value.
            model (str, optional): The new model value.
            gauge (int, optional): The new gauge value.
            shape (str, optional): The new shape value.
            type (str, optional): The new type value.
        
        Returns:
            Strings: The updated string instance.

        Raises:
            ValueError: If the string with the given ID does not exist or inputs are invalid.
            SQLAlchemyError: If a database error occurs.
        """
        logger.info(f"Attempting to update string with ID {string_id}")

        try:
            string = cls.query.get(string_id)

            if not string:
                logger.warning(f"String with ID {string_id} not found.")
                raise ValueError(f"String with ID {string_id} not found.")

            # Update only provided fields
            if brand is not None:
                if not isinstance(brand, str):
                    raise ValueError("brand must be a string.")
                string.brand = brand

            if model is not None:
                if not isinstance(model, str):
                    raise ValueError("model must be a string.")
                string.model = model

            if gauge is not None:
                if not isinstance(gauge, int):
                    raise ValueError("gauge must be an integer.")
                string.gauge = gauge

            if shape is not None:
                if not isinstance(shape, str):
                    raise ValueError("shape must be a string.")
                string.shape = shape
            
            if type is not None:
                if not isinstance(type, str):
                    raise ValueError("type must be a string")
                string.type = type

            db.session.commit()
            logger.info(f"Successfully updated string with ID {string_id}")
            return string

        except SQLAlchemyError as e:
            logger.error(f"Database error while updating string with ID {string_id}: {e}")
            db.session.rollback()
            raise