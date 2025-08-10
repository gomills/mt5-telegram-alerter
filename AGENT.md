## Project Overview

This is a Python application that integrates with MetaTrader 5 (MT5) to send alerts about trading positions to a Telegram group. It tracks opened and closed positions for a single symbol at a time and supports alerts for new entries, partial closures, and full closures.

## Structure

- `main.py`: Entry point for the application.
- `app/telegram_alerting/`: Handles Telegram alerts for opened and closed positions.
- `app/tracker/`: Orchestrates position tracking.
  - `helpers/`: Logger setup, MT5 login, and user input utilities.
  - `positions_trackers/`: Tracks open and closed positions after going through generic tracker.

## Key Features

- Alerts for new, partially closed, and fully closed positions.
- Designed for one symbol at a time, but supports multiple entries.
- Uses MT5's `positions_get()` to fetch current positions.
- Closed position status is estimated using last tick data (may be imprecise).

## Usage

1. Fill in `credentials.yaml` with required details.
2. Install dependencies with `uv sync`.
3. Compile with PyInstaller: `pyinstaller --onefile main.py`.
4. Run the executable.

## Data Model

MT5 positions are represented as `TradePosition` objects with fields like `ticket`, `volume`, `profit`, `symbol`, etc. Partial closures reduce `volume` and adjust `profit`.
