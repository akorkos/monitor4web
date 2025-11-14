import requests
import logging
from datetime import datetime 
import time
import json

logger = logging.getLogger("monitor4web")

def check_website(url: str, retry_attempts: int, delay: int=30) -> tuple:
    """Checks the availability of a website by performing HTTP GET requests.

    Args:
        url (str): The URL of the website to check.
        retry_attempts (int): Number of retry attempts if the request fails.
        delay (int, optional): Delay in seconds between retry attempts. Defaults to 30.

    Returns:
        tuple: A tuple containing various infoermation.
    """
    timestamp = datetime.now().isoformat()
    succesfull_attempts = 0

    for attempt in range(retry_attempts):
        try:
            response = requests.get(url, timeout=10)
            headers = json.dumps(dict(response.headers))
            cookies = json.dumps(requests.utils.dict_from_cookiejar(response.cookies))

            if response.status_code == 200:
                succesfull_attempts += 1
                logger.info(f"Site {url} is online, time elapsed: {response.elapsed}.")
            else:
                logger.warning(f"Attempt: {attempt + 1} failed with status code: {response.status_code}.")
            if attempt < retry_attempts - 1:
                time.sleep(delay)
        except requests.RequestException as e:
            logger.error(f"Error: {e} at attempt: {attempt + 1}.")
            if attempt < retry_attempts - 1:
                time.sleep(delay)
            return (url, timestamp, None, response.status_code, 
                    succesfull_attempts, retry_attempts, headers, cookies)
    
    return (url, timestamp, response.elapsed.total_seconds(), 
            response.status_code, succesfull_attempts, retry_attempts, headers, cookies)