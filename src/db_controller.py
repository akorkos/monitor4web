import sqlite3
import logging
from pathlib import Path

DB_DIR_NAME = '.db'
logger = logging.getLogger("monitor4web")

class DBController:
    def __init__(self, name='requests.db'):
        self.name = name

    def connect_to_db(self) -> None:
        """
        Establishes a connection to the SQLite database.
        The database file is located inside the '.db' directory.
        """
        self.db = sqlite3.connect(f"./{DB_DIR_NAME}/{self.name}")

    def create_table(self) -> None:
        """
        Creates the database and the 'request_log' table if they do not exist.
        """
        if not Path(DB_DIR_NAME).exists():
            Path(DB_DIR_NAME).mkdir()
            
        if not Path(DB_DIR_NAME, self.name).exists():
            self.connect_to_db()
            self.execute_query( 
            '''
                CREATE TABLE IF NOT EXISTS request_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    timestamp TEXT,
                    elapsed REAL,
                    status_code INTEGER,
                    succesfull_attempts INTEGER,
                    retry_attempts INTEGER,
                    headers TEXT,
                    cookies TEXT
                )
            ''')
            
            self.db.close()
            logger.debug("Closing database connection.")

            logger.info(f"Database: {self.name} has been succesfully created.")
        else:
            logger.warning(f"Database: {self.name} exists already.")

    def execute_query(self, query, params=None) -> tuple:
        """Executes a SQL query on the connected database.

        Args:
            query (str): The query string to execute.
            params (tuple, optional): Parameters to insert into the query.

        Returns:
            tuple: Results of the query as a tuple of tuples. Returns empty tuple on error.
        """
        try:
            logger.debug(f"Executing query: {query}.")

            cursor = self.db.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results: list[tuple] = cursor.fetchall()

            return tuple(results)
        except Exception:
            logger.exception(f"An error occurred, while excuting this query: {query}.")
            return ()
        finally:
            self.db.commit()  # Commit the transaction if needed

    def set_instance(self, params: tuple) -> None:
        """Inserts a new log entry into the 'request_log' table.

        Args:
            params (tuple): Values for the columns.
        """
        self.execute_query(
        '''
            INSERT INTO request_log (
                url, 
                timestamp, 
                elapsed, 
                status_code,
                succesfull_attempts,
                retry_attempts,
                headers,
                cookies
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', params)

        logger.info(f"A new entry has been added.")
    
    def get_all_attempts_by_url(self, url) -> tuple:
        """Retrieves the total number of successful and retry attempts for a URL.

        Args:
            url (str): The URL to query.

        Returns:
            tuple: (total_successful_attempts, total_retry_attempts)
        """
        res = self.execute_query(
        '''
            SELECT SUM(succesfull_attempts),
                   SUM(retry_attempts)
            FROM request_log
            WHERE url = ?
        ''', (url,))

        total_attempts = res[0][0] if res and res[0][0] is not None else 0
        total_retries = res[0][1] if res and res[0][1] is not None else 0

        logger.info(f"The total of succesfull attempts for {url} is: {total_attempts} out of {total_retries}.")

        return (total_attempts, total_retries)

    def get_all_attempts_by_url_with_dates(self, url, start_date, end_date) -> tuple:
        """Retrieves the total number of successful and retry attempts for a URL in a date range.

        Args:
            url (str): The URL to query.
            start_date (str): Start date.
            end_date (str): End date.

        Returns:
            tuple: (total_successful_attempts, total_retry_attempts)
        """
        res = self.execute_query(
        '''
            SELECT SUM(succesfull_attempts),
                   SUM(retry_attempts)
            FROM request_log
            WHERE url = ?
            AND timestamp BETWEEN ? AND ?
        ''', (url, start_date, end_date))

        total_attempts = res[0][0] if res and res[0][0] is not None else 0
        total_retries = res[0][1] if res and res[0][1] is not None else 0

        logger.info(f"The total of succesfull attempts for {url} is, between {start_date} and {end_date} are: {total_attempts} out of {total_retries}.")

        return (total_attempts, total_retries)