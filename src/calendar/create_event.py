import json

from ..get_nc_instance import get_nc_instance

SCHEMA = {
    "name": "create_event",
    "description": (
        "Create a new event in a given calendar."
        "Use this whenever the user asks to schedule, create, add, or insert a new event."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "calendar": {
                "type": "string",
                "description": "The name of the calendar where the event will be created."
            },
            "event": {
                "type": "string",
                "description": "The raw iCalendar (vCal) representation of the event to create."
            }
        },
        "required": ["calendar", "event"]
    }
}


def create_event(args: dict[str, str], **kwargs) -> str:
    target_calendar = args.get("calendar")
    raw_event = args.get("event")
    if not target_calendar:
        return json.dumps({"status": "error", "details": "Missing required parameter: 'calendar'"})
    if not raw_event:
        return json.dumps({"status": "error", "details": "Missing required parameter: 'event'"})

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

    try:
        calendar.add_event(raw_event)
    except Exception as e:
        return json.dumps({"status": "error", "details": f"Failed to create event in calendar '{target_calendar}': {str(e)}"})

    return json.dumps({"status": "OK", "details": f"Event created in calendar '{target_calendar}'."})
