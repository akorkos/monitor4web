# monitor4web

`monitor4web` is a Python CLI tool for monitoring website availability.

## Features

- Monitor website availability.
- Retry failed access attempts.
- Log requests to a SQLite database.
- Query historical availability by URL and date range.
- Simple command-line interface (CLI).

## Requirements
- Python 3.8+
- requirements.txt

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd monitor4web
```

## Usage

```bash
python src/main.py --url <website_url> [options]
```

### Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `--create-db` | Create the SQLite database and the `request_log` table. | No | False |
| `-u, --url` | URL of the website to monitor. | Yes | None |
| `--retry-attempts` | Number of times to retry accessing the website. | No | 1 |
| `--check-website` | Check the website and log the results in the database. | No | False |
| `--start-date` | Start date for querying historical availability (`YYYY-MM-DD H:M:S`). | No | None |
| `--end-date` | End date for querying historical availability (`YYYY-MM-DD H:M:S`). | No | None |
| `-v, --version` | Display the program version. | No | None |

