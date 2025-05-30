# Google Sheet Template Documentation

## Overview
This document describes the structure of the Google Sheet template used by the Calendar Reminder App to manage important dates and generate calendar reminders.

## Sheet Structure
The Google Sheet should contain two sheets (tabs):

### 1. Important Dates
This sheet contains all the important dates you want to track and create reminders for.

| Column | Name | Description | Example |
|--------|------|-------------|---------|
| A | Event Name | Name of the event | John's Birthday |
| B | Date | Date of the event (YYYY-MM-DD) | 2025-06-15 |
| C | Category | Category of the event (must match a template name in the Templates sheet) | birthday_with_card |
| D | Person | Person associated with the event | John Smith |
| E | Notes | Additional notes for the event | Likes chocolate cake |
| F | Recurrence | How often the event repeats (yearly, monthly, none) | yearly |

### 2. Templates
This sheet defines the reminder templates for different categories of events.

| Column | Name | Description | Example |
|--------|------|-------------|---------|
| A | Template Name | Unique identifier for the template | birthday_with_card |
| B | Description | Description of the template | Birthday with card reminder sequence |
| C | Reminder 1 Days | Days before/after event for first reminder (-14 means 14 days before) | -14 |
| D | Reminder 1 Title | Title for the first reminder | Buy birthday card for {Person} |
| E | Reminder 1 Description | Description for the first reminder | {Person}'s birthday is coming up on {Date}. Time to buy a card! |
| F | Reminder 2 Days | Days before/after event for second reminder | -7 |
| G | Reminder 2 Title | Title for the second reminder | Send birthday card to {Person} |
| H | Reminder 2 Description | Description for the second reminder | {Person}'s birthday is in a week on {Date}. Send the card now! |
| I | Reminder 3 Days | Days before/after event for third reminder | 0 |
| J | Reminder 3 Title | Title for the third reminder | Send birthday message to {Person} |
| K | Reminder 3 Description | Description for the third reminder | Today is {Person}'s birthday! Send them a message! |

... and so on for additional reminders (columns L through Q for reminders 4 and 5)

## Template Variables
The following variables can be used in reminder titles and descriptions:

- `{Event Name}`: The name of the event
- `{Date}`: The date of the event
- `{Person}`: The person associated with the event
- `{Notes}`: Additional notes for the event

## Example
For the "birthday with card" example mentioned in the requirements:

1. In the Templates sheet:
   - Template Name: birthday_with_card
   - Description: Birthday with card reminder sequence
   - Reminder 1: -14 days, "Buy birthday card for {Person}", "Time to buy a card for {Person}'s birthday on {Date}"
   - Reminder 2: -10 days, "Buy birthday card for {Person}", "Last reminder to buy a card for {Person}'s birthday on {Date}"
   - Reminder 3: -7 days, "Send birthday card to {Person}", "Time to send the card for {Person}'s birthday on {Date}"
   - Reminder 4: 0 days, "Send birthday message to {Person}", "Today is {Person}'s birthday! Send them a message!"
   - Reminder 5: 0 days, "Call {Person} for birthday", "Don't forget to call {Person} today for their birthday!"

2. In the Important Dates sheet:
   - Event Name: John's Birthday
   - Date: 2025-06-15
   - Category: birthday_with_card
   - Person: John Smith
   - Notes: Likes chocolate cake
   - Recurrence: yearly
