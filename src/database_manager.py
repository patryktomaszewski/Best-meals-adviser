import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple


class DatabaseManager:
    """
    Simple sqlite Database Manager to create a database, insert a new record and retrieve data.
    Usage:
    >>> db = DatabaseManager('example.db', 'db')
    >>> db.init_database()
    >>> db.get_records()
    """
    def __init__(self, database: Path, table_name: str):
        connection = sqlite3.connect(database)
        self.database = database
        self.connection = connection
        self.table_name = table_name
        self.cursor = connection.cursor()

    def __str__(self):
        return f'{self.__class__}: {self.database}'

    def __repr__(self):
        return self.__str__()

    def execute_query(self, query: str) -> None:
        self.cursor.execute(query)
        self.connection.commit()

    def init_database(self) -> None:
        self.execute_query(f"""
            CREATE TABLE {self.table_name} (
                hash VARCHAR(50) PRIMARY KEY,
                data JSON NOT NULL
            );
        """)
        self.execute_query(f"""
            CREATE UNIQUE INDEX hash_index ON {self.table_name}(hash);
        """)

    def drop_table(self) -> None:
        self.execute_query(f"""
            DROP TABLE {self.table_name}
        """)

    def insert_record(self, hash: str, data: Dict) -> None:
        self.execute_query(f"""
            INSERT INTO {self.table_name} (hash, data) VALUES ("{hash}", "{data}")
        """)

    def perform_query(self, query: str) -> List[Tuple]:
        return self.cursor.execute(query).fetchall()

    def get_records(self) -> List[Tuple]:
        return self.perform_query(f'SELECT * FROM {self.table_name}')

    def get_record(self, hash: str) -> Tuple:
        return self.cursor.execute(f"""
            SELECT data FROM {self.table_name} WHERE hash="{hash}"
        """).fetchone()
