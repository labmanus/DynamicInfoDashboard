# DynamicInfoDashboard
A simple Flask-based dashboard that displays Google Calendar events, current weather, currency conversion rates, and time for various regions. The interface is styled for both aesthetics and usability.

## Features

- Displays Google Calendar events grouped by date.
- Shows the current and next day's weather details.
- Currency conversion rates for selected currencies.
- Current time for different regions (Seattle, India, Sydney, Belgrade).
- Auto-refresh functionality every 60 seconds.

## Prerequisites

### Hardware

- Raspberry Pi (if hosting the server locally).
- Monitor or touchscreen (optional for Raspberry Pi).
- Any computer with a modern web browser for client access.

### Software Requirements

- Python 3.7+
- Flask
- Google API Client Library
- Requests
- pytz (Python Time Zone Library)
- Chromium browser (or equivalent for your operating system).

### Google Calendar API Setup

1. Enable the Google Calendar API from the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a service account and download the credentials JSON file.
3. Place the credentials file in the project directory (default location: `static/my-project-credentials.json`).

### API Keys

- Weather data is fetched using the [Open-Meteo API](https://open-meteo.com/). No API key is required.

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/dashboard-project.git
cd dashboard-project
```

### Create a Virtual Environment and Install Dependencies
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### Add Your Google Calendar Credentials

Save your Google service account credentials JSON file in the path specified in the ```server.py file``` (default: ```static/my-project-credentials.json```).

### Update Configuration
Modify any constants such as the ```calendarId``` in ```server.py``` to match your setup.

## Running the Project

### Option 1: Host and View Locally on Raspberry Pi

#### 1. Start the Flask Server:
```
python server.py
```
### 2. Set Up Auto-Start on Raspberry Pi:
- Create a systemd service to start the Flask server on boot:
```
sudo nano /etc/systemd/system/dashboard.service
```
- Add the following:
```
[Unit]
Description=Dashboard Flask Application
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/dashboard-project
ExecStart=/home/pi/dashboard-project/venv/bin/python /home/pi/dashboard-project/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```
- Save and enable the service:
```
sudo systemctl enable dashboard.service
sudo systemctl start dashboard.service
```
### 3. View the Dashboard:
- Launch Chromium browser in fullscreen mode:
```
chromium-browser --start-fullscreen --kiosk http://127.0.0.1:5000
```
### 4. Hide the Cursor:
- Install ```unclutter```:
```
sudo apt-get install unclutter
unclutter -idle 0
```



