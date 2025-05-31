#!/usr/bin/env python3
"""
Main Application for Calendar Reminder App

This script ties together all components of the Calendar Reminder App to create
a complete workflow from reading Google Sheets to creating Google Calendar events.
"""

import argparse
import sys
from typing import Dict, Any

from src.sheets_reader import GoogleSheetsReader
from src.template_parser import TemplateParser
from src.calendar_creator import CalendarEventCreator

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Calendar Reminder App - Create calendar reminders from Google Sheets'
    )
    parser.add_argument(
        'spreadsheet_id',
        help='The ID of the Google Sheet containing important dates and templates'
    )
    parser.add_argument(
        '--calendar-id',
        default='primary',
        help='The ID of the Google Calendar to add events to (default: primary)'
    )
    parser.add_argument(
        '--credentials',
        default='credentials.json',
        help='Path to the credentials.json file (default: credentials.json)'
    )
    parser.add_argument(
        '--token',
        default='token.json',
        help='Path to the token.json file (default: token.json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without creating actual calendar events'
    )
    parser.add_argument(
        '--list-calendars',
        action='store_true',
        help='List available calendars and exit'
    )
    
    return parser.parse_args()

def list_calendars(args):
    """List available calendars."""
    print("Listing available calendars...")
    creator = CalendarEventCreator(args.credentials, args.token)
    calendars = creator.list_calendars()
    
    if not calendars:
        print("No calendars found or unable to access calendars.")
        return
    
    print("\nAvailable calendars:")
    for calendar in calendars:
        print(f"  - {calendar['summary']} (ID: {calendar['id']})")
    
    print("\nUse the calendar ID with the --calendar-id option to specify which calendar to use.")

def main():
    """Main function to run the Calendar Reminder App."""
    args = parse_arguments()
    
    # Handle list calendars request
    if args.list_calendars:
        list_calendars(args)
        return
    
    print(f"Calendar Reminder App - Processing spreadsheet: {args.spreadsheet_id}")
    
    try:
        # Step 1: Read data from Google Sheets
        print("\nStep 1: Reading data from Google Sheets...")
        reader = GoogleSheetsReader(args.credentials, args.token)
        data = reader.read_sheet(args.spreadsheet_id)
        
        important_dates_count = len(data['important_dates'])
        templates_count = len(data['templates'])
        print(f"  - Found {important_dates_count} important dates and {templates_count} templates")
        
        if important_dates_count == 0 or templates_count == 0:
            print("Error: No data found in Google Sheet. Please check the spreadsheet ID and content.")
            return
        
        # Step 2: Parse templates and generate events
        print("\nStep 2: Parsing templates and generating events...")
        parser = TemplateParser(data)
        events = parser.generate_events()
        
        print(f"  - Generated {len(events)} calendar events")
        
        if len(events) == 0:
            print("Warning: No events were generated. Please check your data and templates.")
            return
        
        # Print a summary of the events
        print("\nEvent summary:")
        for i, event in enumerate(events[:5]):  # Show first 5 events
            print(f"  {i+1}. {event['start']['date']}: {event['summary']}")
        
        if len(events) > 5:
            print(f"  ... and {len(events) - 5} more events")
        
        # Step 3: Create events in Google Calendar (unless dry run)
        if args.dry_run:
            print("\nDry run completed. No events were created in Google Calendar.")
            print("Use the command without --dry-run to create the actual events.")
        else:
            print(f"\nStep 3: Creating events in Google Calendar (calendar ID: {args.calendar_id})...")
            creator = CalendarEventCreator(args.credentials)
            created_events = creator.create_events(events, args.calendar_id)
            
            print(f"  - Successfully created {len(created_events)} events in Google Calendar")
            print("\nCalendar Reminder App completed successfully!")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please check your inputs and try again.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
