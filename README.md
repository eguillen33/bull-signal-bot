# Bull Signal Bot

## Overview

Bull Signal Bot is a Python-based automated stock alert system that fetches and processes financial data to identify potential bullish and bearish stock signals. It integrates with the FinancialModelingPrep API to retrieve stock upgrades and downgrades, then filters and notifies users based on predefined conditions. Note that I am aware that the name of this application - _Bull Signal Bot_ - is a slight misnomer.

⚠ **Important:** This project uses FinancialModelingPrep. Ensure you obtain an API key from [FinancialModelingPrep](https://financialmodelingprep.com/) and configure it accordingly.

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
- [Docker](https://docs.docker.com/get-docker/) (for containerized execution)

## Installation (Local Python)

1. Clone the repository:
   ```
   sh
   git clone https://github.com/yourusername/bull-signal-bot.git
   cd bull-signal-bot
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API credentials:
   ```
   FMP_API_KEY=your_api_key_here
   ```

## Usage
### Run Manually with Python
```
python bull_signal_bot.py
```

### Running with Docker

1. Build the Docker image:
   ```
   docker build -t bull-signal-bot:latest .
   ```

2. Run the container and pass your API key as an environment variable:
   ```
   docker run --rm -e FMP_API_KEY=your_api_key_here bull-signal-bot
   ```
   💡 Tip: You can also use --env-file .env if you'd rather load environment variables from a file.

## Automating Execution with crontab (Linux)

You can schedule the bot to run automatically using cron:

1. Open your crontab:
   ```
   crontab -e
   ```

2. Add a line like this to run it every hour:
   ```
   0 * * * * /usr/bin/python3 /path/to/bull_signal_bot.py >> /path/to/bull_signal_bot.log 2>&1
   ```

## Tips

- Use the full path to Python (use which python3 to find it).
- Make the script executable: `chmod +x bull_signal_bot.py`
- To check if the script is running via cron: `cat /var/log/syslog | grep CRON`

## License

This project is licensed under the MIT License.

## Author

Ed Guillen
