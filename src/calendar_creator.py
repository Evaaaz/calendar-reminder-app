#!/usr/bin/env python3
"""
Google Calendar Event Creator Module for Calendar Reminder App

This module handles creating events in Google Calendar based on the generated
events from the template parser.
"""

import os.path
from typing import Dict, List, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes needed for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

class CalendarEventCreator:
    """Class to handle creating events in Google Calendar."""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """
        Initialize the CalendarEventCreator.
        
        Args:
            credentials_file: Path to the credentials.json file
            token_file: Path to the token.json file (will be created if it doesn't exist)
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
    
    def authenticate(self) -> None:
        """
        Authenticate with Google Calendar API.
        
        This method handles the OAuth2 authentication flow, including refreshing
        tokens if they exist or going through the full authentication flow if needed.
        """
        creds = None
        
        # Check if token.json exists and load credentials from it
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_info(
                info=eval(open(self.token_file, 'r').read()), 
                scopes=SCOPES
            )
        
        # If credentials don't exist or are invalid, go through auth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(str(creds.to_json()))
        
        # Build the service
        self.service = build('calendar', 'v3', credentials=creds)
    
    def create_events(self, events: List[Dict[str, Any]], calendar_id: str = 'primary') -> List[Dict[str, Any]]:
        """
        Create events in Google Calendar.
        
        Args:
            events: List of event dictionaries from the TemplateParser
            calendar_id: ID of the calendar to add events to (default: 'primary')
            
        Returns:
            A list of created event responses
        """
        if not self.service:
            self.authenticate()
        
        created_events = []
        
        for event in events:
            try:
                # Create a copy of the event without metadata
                calendar_event = event.copy()
                if 'metadata' in calendar_event:
                    del calendar_event['metadata']
                
                # Create the event in Google Calendar
                created_event = self.service.events().insert(
                    calendarId=calendar_id,
                    body=calendar_event
                ).execute()
                
                print(f"Event created: {created_event.get('htmlLink')}")
                created_events.append(created_event)
            
            except HttpError as error:
                print(f"An error occurred: {error}")
                # Continue with other events even if one fails
        
        return created_events
    
    def list_calendars(self) -> List[Dict[str, Any]]:
        """
        List available calendars.
        
        Returns:
            A list of calendar dictionaries
        """
        if not self.service:
            self.authenticate()
        
        try:
            calendar_list = self.service.calendarList().list().execute()
            return calendar_list.get('items', [])
        
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []


def main():
    """Main function for testing the module."""
    # Sample event for testing
    sample_event = {
        'summary': 'Test Event',
        'description': 'This is a test event created by the Calendar Reminder App',
        'start': {
            'date': '2025-06-01',
            'timeZone': 'UTC',
        },
        'end': {
            'date': '2025-06-01',
            'timeZone': 'UTC',
        },
        'reminders': {
            'useDefault': True
        }
    }
    
    creator = CalendarEventCreator()
    
    # List available calendars
    print("Available calendars:")
    calendars = creator.list_calendars()
    for calendar in calendars:
        print(f"  - {calendar['summary']} ({calendar['id']})")
    
    # Create a test event
    if calendars:
        created_events = creator.create_events([sample_event])
        print(f"Created {len(created_events)} events")


if __name__ == '__main__':
    main()
