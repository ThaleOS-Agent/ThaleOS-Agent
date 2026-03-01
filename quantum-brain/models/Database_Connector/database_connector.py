"""
This module provides the DatabaseConnector class for managing database connections
and executing queries using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


class DatabaseConnector:
    """
    A simple database connector using SQLAlchemy.

    Methods:
        connect(): Establishes a database connection.
        execute_query(query): Executes a SQL query and returns results.
        close(): Closes the database connection.
    """

    def __init__(self, connection_string):
        """
        Initialize the connector with a SQLAlchemy connection string.

        Args:
            connection_string (str): SQLAlchemy database URI.
        """
        self.connection_string = connection_string
        self.engine = None
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the database.

        Raises:
            SQLAlchemyError: If the connection cannot be established.
        """
        try:
            self.engine = create_engine(self.connection_string)
            self.connection = self.engine.connect()
        except SQLAlchemyError as e:
            print(f"Failed to connect to database: {e}")
            raise

    def execute_query(self, query):
        """
        Executes a SQL query and returns the fetched results.

        Args:
            query (str): The SQL query to execute.

        Returns:
            list of tuples: Query results, or None if execution failed.
        """
        if not self.connection:
            self.connect()

        try:
            result = self.connection.execute(query)
            return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Query execution failed: {e}")
            return None

    def close(self):
        """
        Closes the database connection and disposes of the engine.
        """
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()


if __name__ == "__main__":
    # Example usage (replace with real connection details)
    conn_str = "postgresql://user:password@localhost:5432/dbname"
    db = DatabaseConnector(conn_str)
    try:
        db.connect()
        print("Connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        db.close()

