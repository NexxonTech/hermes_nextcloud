from datetime import datetime
import json

from ..get_nc_instance import get_nc_instance

SCHEMA = {
    "name": "list_events",
    "description": (
        "List events in a given calendar, filtrable by a date range. The date range is specified by the 'start' and 'end' parameters."
        "Use this whenever the user asks to fetch events from their calendar."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "calendar": {
                "type": "string",
                "description": "The name of the calendar to list events from."
            },
            "start": {
                "type": "string",
                "description": "The start date of the range to list events from."
            },
            "end": {
                "type": "string",
                "description": "The end date of the range to list events from."
            }
        },
        "required": ["calendar"]
    }
}

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
