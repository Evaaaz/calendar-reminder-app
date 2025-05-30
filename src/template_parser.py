#!/usr/bin/env python3
"""
Template Parser and Event Generator Module for Calendar Reminder App

This module handles parsing templates and generating calendar events based on
important dates and their associated templates.
"""

import datetime
from typing import Dict, List, Any
from dateutil import parser as date_parser

class TemplateParser:
    """Class to handle parsing templates and generating events."""
    
    def __init__(self, data: Dict[str, List[Dict[str, Any]]]):
        """
        Initialize the TemplateParser.
        
        Args:
            data: The data dictionary from the GoogleSheetsReader
        """
        self.important_dates = data['important_dates']
        self.templates = data['templates']
        self.template_map = {t['template_name']: t for t in self.templates}
    
    def generate_events(self) -> List[Dict[str, Any]]:
        """
        Generate calendar events based on important dates and templates.
        
        Returns:
            A list of dictionaries, each representing a calendar event
        """
        events = []
        
        for date_entry in self.important_dates:
            category = date_entry['category']
            
            # Skip if no category or category doesn't match any template
            if not category or category not in self.template_map:
                print(f"Warning: No template found for category '{category}' for event '{date_entry['event_name']}'")
                continue
            
            template = self.template_map[category]
            
            # Generate events for each reminder in the template
            for reminder in template['reminders']:
                event = self._create_event(date_entry, reminder)
                events.append(event)
        
        return events
    
    def _create_event(self, date_entry: Dict[str, Any], reminder: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a calendar event based on a date entry and a reminder template.
        
        Args:
            date_entry: Dictionary containing important date information
            reminder: Dictionary containing reminder information
            
        Returns:
            A dictionary representing a calendar event
        """
        # Parse the base date
        try:
            base_date = date_parser.parse(date_entry['date']).date()
        except (ValueError, TypeError):
            print(f"Warning: Invalid date '{date_entry['date']}' for event '{date_entry['event_name']}'")
            # Use today as a fallback
            base_date = datetime.date.today()
        
        # Calculate the reminder date
        reminder_date = base_date + datetime.timedelta(days=reminder['days'])
        
        # Replace template variables in title and description
        title = self._replace_variables(reminder['title'], date_entry)
        description = self._replace_variables(reminder['description'], date_entry)
        
        # Create the event
        event = {
            'summary': title,
            'description': description,
            'start': {
                'date': reminder_date.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'date': reminder_date.isoformat(),
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': True
            },
            # Store original data for reference
            'metadata': {
                'original_event': date_entry['event_name'],
                'original_date': date_entry['date'],
                'days_offset': reminder['days'],
                'category': date_entry['category']
            }
        }
        
        return event
    
    def _replace_variables(self, text: str, date_entry: Dict[str, Any]) -> str:
        """
        Replace template variables in text with values from date_entry.
        
        Args:
            text: The template text with variables
            date_entry: Dictionary containing important date information
            
        Returns:
            The text with variables replaced
        """
        if not text:
            return ""
        
        # Define variable mappings
        variables = {
            '{Event Name}': date_entry['event_name'],
            '{Date}': date_entry['date'],
            '{Person}': date_entry['person'],
            '{Notes}': date_entry['notes']
        }
        
        # Replace each variable
        for var, value in variables.items():
            text = text.replace(var, value or '')
        
        return text


def main():
    """Main function for testing the module."""
    # Sample data for testing
    sample_data = {
        'important_dates': [
            {
                'event_name': "John's Birthday",
                'date': '2025-06-15',
                'category': 'birthday_with_card',
                'person': 'John Smith',
                'notes': 'Likes chocolate cake',
                'recurrence': 'yearly'
            }
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
                    {
                        'days': -7,
                        'title': 'Send birthday card to {Person}',
                        'description': '{Person}\'s birthday is in a week on {Date}. Send the card now!'
                    },
                    {
                        'days': 0,
                        'title': 'Send birthday message to {Person}',
                        'description': 'Today is {Person}\'s birthday! Send them a message!'
                    }
                ]
            }
        ]
    }
    
    parser = TemplateParser(sample_data)
    events = parser.generate_events()
    
    print(f"Generated {len(events)} events:")
    for event in events:
        print(f"  - {event['start']['date']}: {event['summary']}")
        print(f"    {event['description']}")


if __name__ == '__main__':
    main()
