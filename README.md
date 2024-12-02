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
#### 2. Set Up Auto-Start on Raspberry Pi:
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
#### 3. View the Dashboard:
- Launch Chromium browser in fullscreen mode:
```
chromium-browser --start-fullscreen --kiosk http://127.0.0.1:5000
```
#### 4. Hide the Cursor:
- Install ```unclutter```:
```
sudo apt-get install unclutter
unclutter -idle 0
```

### Option 2: Host on Raspberry Pi and View from Another Device

#### 1. Start the Flask Server:
```
python server.py
```
#### 2. Find the Raspberry Pi's IP Address:
```
hostname -I
```
Note the IP address (e.g., ```192.168.0.100```).

#### 3. Access the Dashboard:
- Open a browser on any device connected to the same network and navigate to:
```
http://<Raspberry Pi IP>:5000
```
### Option 3: Host Locally on Windows/MacOS

#### 1. Start the Flask Server:
```
python server.py
```
#### 2. Access the Dashboard:
Open a browser on the same machine and navigate to:
```
http://127.0.0.1:5000
```
#### 3. Access from Other Devices:
Replace ```127.0.0.1``` with your machine's IP address to access the dashboard on other devices.

## Project Structure
```
.
├── server.py                          # Backend logic and API integrations
├── templates/
│   └── index.html                     # HTML for rendering the dashboard
├── static/
│   ├── images/                        # Static images for styling
│   ├── my-project-credentials.json    # google calendar api credentials
├── requirements.txt                   # List of Python dependencies
└── README.md                          # Project documentation
```
## Features Overview
- **Google Calendar Integration:** Displays events fetched from the Google Calendar API, grouped by date, and limited to the next 7 days.

- **Weather Information:** Fetches and displays the current and next day's weather using Open-Meteo's API. Weather symbols and descriptions are included.

- **Regional Time:** Shows current times for selected regions.

- **Currency Conversion:** Hardcoded exchange rates as placeholders (can be extended for dynamic updates).

## Future Improvements
- Dynamic weather icons using Unicode-friendly emojis.
- Fetch real-time currency conversion rates via an API.
- Add authentication for Google Calendar API to allow multiple user accounts.


## Google Calendar API Setup

Follow the steps below to set up the Google Calendar API.

#### Steps to Get Google Calendar API Credentials

1. **Create a Project on Google Cloud Console**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on **Select a Project** and then **New Project**.
   - Enter a project name and click **Create**.

2. **Enable the Google Calendar API**:
   - Open the [Google API Library](https://console.cloud.google.com/apis/library).
   - Search for "Google Calendar API" and click on it.
   - Click the **Enable** button.

3. **Create a Service Account**:
   - Navigate to the [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts).
   - Click **Create Service Account**.
   - Provide a name for the service account and click **Create and Continue**.
   - Assign the role **Project -> Editor** and click **Continue**.
   - Click **Done** to finish.

4. **Generate a Key for the Service Account**:
   - In the Service Accounts page, click the three dots next to your service account and select **Manage keys**.
   - Click **Add Key -> Create New Key** and choose **JSON**.
   - Download the JSON key file and place it in your project directory (e.g., `static/my-project-credentials.json`).

5. **Share Your Google Calendar with the Service Account**:
   - Open Google Calendar in your browser.
   - Click on the **Options (three dots)** next to the calendar you want to share and select **Settings and Sharing**.
   - Under **Share with specific people**, click **Add People**.
   - Add the email address of your service account (it ends with `iam.gserviceaccount.com`) and give it **Make Changes to Events** access.

6. **Update the Project Configuration**:
   - Replace the placeholder path to the JSON file in `server.py` with the actual path to your downloaded file:
     ```python
     SERVICE_ACCOUNT_FILE = '/path/to/your-credentials-file.json'
     ```
