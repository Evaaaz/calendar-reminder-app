# Google API Credentials Guide

This document provides step-by-step instructions for obtaining the necessary Google API credentials to use with the Calendar Reminder App.

## Prerequisites
- A Google account
- Access to Google Cloud Console

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click on "New Project"
4. Enter a name for your project (e.g., "Calendar Reminder App")
5. Click "Create"
6. Wait for the project to be created and then select it from the dropdown

## Step 2: Enable the Required APIs

1. In the Google Cloud Console, navigate to "APIs & Services" > "Library"
2. Search for and enable the following APIs:
   - Google Sheets API
   - Google Calendar API
   
   For each API:
   - Click on the API name
   - Click "Enable"
   - Wait for the API to be enabled

## Step 3: Create OAuth 2.0 Credentials

1. In the Google Cloud Console, navigate to "APIs & Services" > "Credentials"
2. Click "Create Credentials" and select "OAuth client ID"
3. If prompted to configure the OAuth consent screen:
   - Click "Configure Consent Screen"
   - Select "External" user type (unless you're using Google Workspace)
   - Fill in the required information (App name, user support email, developer contact information)
   - Click "Save and Continue"
   - Add the following scopes:
     - `https://www.googleapis.com/auth/spreadsheets.readonly`
     - `https://www.googleapis.com/auth/calendar.events`
   - Click "Save and Continue"
   - Add test users (including your own email)
   - Click "Save and Continue"
   - Review your settings and click "Back to Dashboard"
4. Return to "Credentials" and click "Create Credentials" > "OAuth client ID"
5. Select "Desktop app" as the application type
6. Enter a name for the OAuth client (e.g., "Calendar Reminder App Client")
7. Click "Create"
8. Click "Download JSON" to download your credentials file
9. Rename the downloaded file to `credentials.json`

## Step 4: Add Credentials to the App

1. Place the `credentials.json` file in the root directory of the Calendar Reminder App
2. Make sure not to commit this file to Git (it's already in the .gitignore file)

## Step 5: First Run Authentication

The first time you run the app, it will:
1. Use the credentials.json file to request authorization
2. Open a browser window asking you to log in to your Google account
3. Ask for permission to access your Google Sheets and Calendar
4. After granting permission, the app will save a token.json file for future use

## Security Notes

- Keep your credentials.json and token.json files secure
- Do not share these files with others
- Do not commit these files to public repositories
- If you suspect your credentials have been compromised, revoke them in the Google Cloud Console and create new ones
