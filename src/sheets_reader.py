#!/usr/bin/env python3
"""
Google Sheets Reader Module for Calendar Reminder App

This module handles reading data from Google Sheets based on the template structure
defined in the documentation.
"""

import os.path
import sys
from typing import Dict, List, Any, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scopes needed for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Sheet names in the Google Sheet
IMPORTANT_DATES_SHEET = 'Important Dates'
TEMPLATES_SHEET = 'Templates'

class GoogleSheetsReader:
    """Class to handle reading data from Google Sheets."""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """
        Initialize the GoogleSheetsReader.
        
        Args:
            credentials_file: Path to the credentials.json file
            token_file: Path to the token.json file (will be created if it doesn't exist)
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
    
    def authenticate(self) -> None:
        """
        Authenticate with Google Sheets API.
        
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
        self.service = build('sheets', 'v4', credentials=creds)
    
    def read_sheet(self, spreadsheet_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Read data from the Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the Google Sheet to read from
            
        Returns:
            A dictionary containing the parsed data from both sheets:
            {
                'important_dates': [
                    {
                        'event_name': 'John\'s Birthday',
                        'date': '2025-06-15',
                        'category': 'birthday_with_card',
                        'person': 'John Smith',
                        'notes': 'Likes chocolate cake',
                        'recurrence': 'yearly'
                    },
                    ...
                ],
                'templates': [
                    {
                        'template_name': 'birthday_with_card',
                        'description': 'Birthday with card reminder sequence',
                        'reminders': [
                            {
                                'days': -14,
                                'title': 'Buy birthday card for {Person}',
                                'description': '{Person}\'s birthday is coming up on {Date}. Time to buy a card!'
                            },
                            ...
                        ]
                    },
                    ...
                ]
            }
        """
        if not self.service:
            self.authenticate()
        
        try:
            # Read the Important Dates sheet
            important_dates = self._read_important_dates(spreadsheet_id)
            
            # Read the Templates sheet
            templates = self._read_templates(spreadsheet_id)
            
            return {
                'important_dates': important_dates,
                'templates': templates
            }
        
        except HttpError as error:
            print(f"An error occurred: {error}")
            return {'important_dates': [], 'templates': []}
    
    def _read_important_dates(self, spreadsheet_id: str) -> List[Dict[str, Any]]:
        """
        Read and parse the Important Dates sheet.
        
        Args:
            spreadsheet_id: The ID of the Google Sheet
            
        Returns:
            A list of dictionaries, each representing an important date
        """
        # Get the data from the sheet
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{IMPORTANT_DATES_SHEET}!A2:F"  # Skip header row
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("No data found in Important Dates sheet.")
            return []
        
        # Parse the data
        important_dates = []
        for row in values:
            # Ensure row has all required columns
            while len(row) < 6:
                row.append('')
            
            important_date = {
                'event_name': row[0],
                'date': row[1],
                'category': row[2],
                'person': row[3],
                'notes': row[4],
                'recurrence': row[5]
            }
            
            important_dates.append(important_date)
        
        return important_dates
    
    def _read_templates(self, spreadsheet_id: str) -> List[Dict[str, Any]]:
        """
        Read and parse the Templates sheet.
        
        Args:
            spreadsheet_id: The ID of the Google Sheet
            
        Returns:
            A list of dictionaries, each representing a template
        """
        # Get the data from the sheet
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{TEMPLATES_SHEET}!A2:Q"  # Skip header row
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("No data found in Templates sheet.")
            return []
        
        # Parse the data
        templates = []
        for row in values:
            # Ensure row has all required columns
            while len(row) < 17:  # A through Q (17 columns)
                row.append('')
            
            template = {
                'template_name': row[0],
                'description': row[1],
                'reminders': []
            }
            
            # Process up to 5 reminders (columns C through Q)
            for i in range(5):
                base_idx = 2 + (i * 3)  # Starting index for each reminder
                
                # Skip if days field is empty
                if not row[base_idx]:
                    continue
                
                try:
                    days = int(row[base_idx])
                except ValueError:
                    print(f"Warning: Invalid days value '{row[base_idx]}' for template '{template['template_name']}'")
                    continue
                
                reminder = {
                    'days': days,
                    'title': row[base_idx + 1],
                    'description': row[base_idx + 2]
                }
                
                template['reminders'].append(reminder)
            
            templates.append(template)
        
        return templates


def main():
    """Main function for testing the module."""
    if len(sys.argv) != 2:
        print("Usage: python sheets_reader.py <spreadsheet_id>")
        sys.exit(1)
    
    spreadsheet_id = sys.argv[1]
    reader = GoogleSheetsReader()
    data = reader.read_sheet(spreadsheet_id)
    
    print("Important Dates:")
    for date in data['important_dates']:
        print(f"  - {date['event_name']} ({date['date']}): {date['category']}")
    
    print("\nTemplates:")
    for template in data['templates']:
        print(f"  - {template['template_name']}: {len(template['reminders'])} reminders")


if __name__ == '__main__':
    main()
