from datetime import datetime
import json
import logging
import os

from nc_py_api import Nextcloud


logger = logging.getLogger(__name__)

def get_nc_instance() -> Nextcloud:
    nextcloud_url = os.environ.get("NEXTCLOUD_INSTANCE_URL")
    nextcloud_username = os.environ.get("NEXTCLOUD_USER")
    nextcloud_app_password = os.environ.get("NEXTCLOUD_APP_PASSWORD")

    print(f"Connecting to Nextcloud at {nextcloud_url} with user {nextcloud_username}...")

    return Nextcloud(nextcloud_url=nextcloud_url, nc_auth_user=nextcloud_username, nc_auth_pass=nextcloud_app_password)

def list_calendars(args: dict[str, str], **kwargs) -> str:
    try:
        nc = get_nc_instance()
    except Exception as e:
        return json.dumps({"status": "error", "details": f"Failed to connect to Nextcloud: {str(e)}"})

    try:
        principal = nc.cal.get_principal()
        calendars = principal.get_calendars()
    except Exception as e:
        return json.dumps({"status": "error", "details": f"Failed to retrieve calendars: {str(e)}"})

    return json.dumps({"status": "OK", "data": [calendar.name for calendar in calendars]}) #type: ignore

def list_events(args: dict[str, str], **kwargs) -> str:
    target_calendar = args.get("calendar")
    start = args.get("start")
    end = args.get("end")
    if not target_calendar:
        return json.dumps({"status": "error", "details": "Missing required parameter: 'calendar'"})
    if not start:
        return json.dumps({"status": "error", "details": "Missing required parameter: 'start'"})
    if not end:
        return json.dumps({"status": "error", "details": "Missing required parameter: 'end'"})

    try:
        nc = get_nc_instance()
    except Exception as e:
        return json.dumps({"status": "error", "details": f"Failed to connect to Nextcloud: {str(e)}"})

    try:
        principal = nc.cal.get_principal()
        calendar = next(cal for cal in principal.get_calendars() if cal.name == target_calendar) #type: ignore
    except StopIteration:
        return json.dumps({"status": "error", "details": f"Calendar '{target_calendar}' not found."})
    except Exception as e:
        return json.dumps({"status": "error", "details": f"Failed to retrieve calendar '{target_calendar}': {str(e)}"})

    start_date = datetime.fromisoformat(start)
    end_date = datetime.fromisoformat(end)
    events = calendar.search(event=True, start=start_date, end=end_date)
    return json.dumps({"status": "OK", "data": [event.data for event in events]}) #type: ignore
