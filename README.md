# Bull Signal Bot

## Overview

Bull Signal Bot is a Python-based automated stock alert system that fetches and processes financial data to identify potential bullish stock signals. It integrates with the FinancialModelingPrep API to retrieve stock upgrades and downgrades, then filters and notifies users based on predefined conditions.

⚠ **Warning:** This project uses FinancialModelingPrep instead of Benzinga. Ensure you obtain an API key from [FinancialModelingPrep](https://financialmodelingprep.com/) and configure it accordingly.

## Features

- Fetches stock upgrade/downgrade data from FinancialModelingPrep API.
- Filters and processes relevant stock signals.
- Sends notifications based on detected bullish trends.
- Can be scheduled to run at regular intervals using `crontab`.

## Prerequisites

Ensure you have the following installed:

- Python 3.10+
- `pip` (Python package manager)
- `requests` and other dependencies (install via `requirements.txt`)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/bull-signal-bot.git
   cd bull-signal-bot
   ```

2. Create a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up your API credentials:

   - Create a `.env` file in the project root and add your API key:
     ```env
     FMP_API_KEY=your_api_key_here
     ```

## Usage

Run the bot manually:

```sh
python bull-signal-bot.py
```

## Automating Execution with `crontab` (Linux Users)

To schedule the script to run automatically, follow these steps:

1. Open the crontab editor:
   ```sh
   crontab -e
   ```
2. Add the following line to run the bot every hour:
   ```sh
   0 * * * * /usr/bin/python3 /path/to/bull-signal-bot.py >> /path/to/bull-signal-bot.log 2>&1
   ```

### Advisory for Linux Users

- Use the full path to Python to avoid environment issues.
- Ensure the script has execute permissions:
  ```sh
  chmod +x bull-signal-bot.py
  ```
- If using a virtual environment, reference the Python binary inside `venv`:
  ```sh
  0 * * * * /path/to/venv/bin/python /path/to/bull-signal-bot.py >> /path/to/bull-signal-bot.log 2>&1
  ```
- To check if cron is running the script, view logs:
  ```sh
  cat /var/log/syslog | grep CRON
  ```

## License

This project is licensed under the MIT License.

## Author

Ed Guillen