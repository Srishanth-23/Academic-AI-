import os
import requests
import json
import time

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT37fVb54jS6C5bONw2C-rYyQ198Y0hA9K_z2m4r7qWbI8qQ2vN7aF_t0L/pub?output=csv"
STATE_FILE = "competitions_state.json"

def get_current_count():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('count', 0)
    except Exception as e:
        print(f"Error reading state: {e}")
    return 0

def save_state(count: int, latest_name: str):
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump({"count": count, "latest_name": latest_name}, f)
    except Exception as e:
        print(f"Error saving state: {e}")

def check_sheet():
    print("Checking Google Sheet for new competitions...")
    try:
        response = requests.get(SHEET_CSV_URL)
        response.raise_for_status()
        
        # Count lines (excluding header)
        lines = response.text.strip().split('\n')
        if len(lines) <= 1:
            return
            
        current_count = len(lines) - 1
        previous_count = get_current_count()
        latest_name = lines[-1].split(',')[0] # Assuming first col is Name
        
        if current_count > previous_count:
            diff = current_count - previous_count
            print(f"Found {diff} new competitions! Latest: {latest_name}")
            
            # Here we simulate triggering the Expo push notification.
            # In a real production app, this would use the Expo Push API via `requests.post('https://exp.host/--/api/v2/push/send', ...)`
            # and send it to all registered user tokens.
            print("To trigger real push notifications, configure your Expo Push tokens here.")
            
        elif current_count < previous_count:
            print("Competitions were removed.")
            
        save_state(current_count, latest_name)
        
    except Exception as e:
        print(f"Failed to check sheet: {e}")

if __name__ == "__main__":
    # Force initial check
    check_sheet()
    
    # Simple polling loop (e.g., every 1 hour)
    while True:
        time.sleep(3600) # 1 hour
        check_sheet()
