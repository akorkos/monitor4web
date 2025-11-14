from logger import setup_logger
from monitor import check_website
import time
from cli import cli_arg_parse
from datetime import datetime 
from db_controller import DBController

def convert(date_time: str) -> str:
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").isoformat()

def main() -> None:
    logger = setup_logger("monitor4web")

    args = cli_arg_parse()

    dbc = DBController()

    if args.create_db:
        dbc.create_table()

    dbc.connect_to_db()

    if args.check_website:
        res = check_website(args.url, args.retry_attempts)

        dbc.set_instance(res)
    
    total_attempts, total_retries = dbc.get_all_attempts_by_url(args.url)

    if args.start_date and args.end_date:
        total_attempts, total_retries = dbc.get_all_attempts_by_url_with_dates(
            args.url,
            convert(args.start_date),
            convert(args.end_date)
        )

    if total_attempts > 0:
        availability = total_retries / total_attempts * 100

        print(f"Availability of the webpage {args.url} is: {availability}%.")
    elif total_attempts == 0 and total_retries > 0: 
        print("There are none successfull attempts recorded.")
    elif args.create_db:
        print("Database creation triggered. See logs for more details.")
    else:
        print("Website not found in the database.")

if __name__ == "__main__":
    main()