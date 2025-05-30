# Calendar Reminder App

A Python application that reads important dates from a Google Sheet and creates multiple calendar reminders in Google Calendar based on templates defined in the sheet.

## Features

- Read important dates and reminder templates from a Google Sheet
- Generate multiple calendar reminders based on template definitions
- Create events in Google Calendar with appropriate titles and descriptions
- Support for variable substitution in reminder titles and descriptions
- Support for recurring events

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd calendar-reminder-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Google API credentials (see [Google API Credentials Guide](docs/google_api_credentials_guide.md))

## Google Sheet Setup

The application expects a Google Sheet with two sheets (tabs):

1. **Important Dates**: Contains all the important dates you want to track
2. **Templates**: Defines reminder templates for different categories of events

For detailed information on the expected structure, see the [Google Sheet Template Documentation](docs/google_sheet_template.md).

## Usage

### Basic Usage

```
python main.py <spreadsheet_id>
```

Replace `<spreadsheet_id>` with the ID of your Google Sheet. The ID is the part of the URL after `/d/` and before the next `/`.

Example:
```
python main.py 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
```

### List Available Calendars

To see a list of available calendars:

```
python main.py --list-calendars
```

### Specify Calendar

To add events to a specific calendar (other than your primary calendar):

```
python main.py <spreadsheet_id> --calendar-id <calendar_id>
```

### Dry Run

To perform a dry run without creating actual calendar events:

```
python main.py <spreadsheet_id> --dry-run
```

### Other Options

```
python main.py --help
```

## First Run Authentication

The first time you run the app, it will:
1. Use the credentials.json file to request authorization
2. Open a browser window asking you to log in to your Google account
3. Ask for permission to access your Google Sheets and Calendar
4. After granting permission, the app will save a token.json file for future use

## Example

For a quick test of the application logic without accessing Google APIs, run:

```
python test_workflow.py
```

This will generate sample data and show how the events would be created.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
