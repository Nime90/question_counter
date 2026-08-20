# Group Question Tracker

A lightweight Streamlit app for tracking how many questions students ask during class, grouped by team or class group.

The app lets students submit questions from a simple form, stores each submission in a Google Sheet, and shows live analytics for group totals and question trends over time.

## Features

- Submit a question with a selected group name
- Record each question with a timestamp in Google Sheets
- View total questions by group
- See cumulative question activity over time in a line chart
- Supports groups 1 through 7 by default

## What the app does

The application has two tabs:

1. Ask a Question
   - Choose a group from Group 1 to Group 7
   - Enter the question text
   - Submit the form
   - The app appends the group, question, and timestamp to the connected Google Sheet

2. Group Rankings & Analytics
   - Summarizes how many questions each group has submitted
   - Displays a trend chart showing cumulative questions over time
   - Shows a friendly empty-state message when no questions have been submitted yet

## Tech stack

- Python
- Streamlit
- Google Sheets via gspread
- Pandas

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a Google Cloud service account and download the JSON key file
5. Save the file as `service_account.json` in the project root
6. Update the spreadsheet ID in `app.py` if needed:

   ```python
   SPREADSHEET_ID = "YOUR_GOOGLE_SHEET_ID"
   ```

7. Run the app:

   ```bash
   streamlit run app.py
   ```

## Required files

- `app.py` — Streamlit app logic and UI
- `service_account.json` — Google service account credentials for accessing the spreadsheet
- `requirements.txt` — Python dependencies

## Notes

- The app connects to the first worksheet in the spreadsheet using `gspread`
- It appends rows in the format: Group, Question, Timestamp
- If no data exists yet, the analytics tab will display a message instead of charts

## Example workflow

A student selects their group, writes a question, and submits it. The submission is logged to the spreadsheet and appears in the rankings and time-series analytics on the second tab.
