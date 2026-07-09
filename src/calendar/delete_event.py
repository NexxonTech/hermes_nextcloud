import json

from ..get_nc_instance import get_nc_instance

SCHEMA = {
    "name": "delete_event",
    "description": (
        "Delete an event from a given calendar using its UID."
        "Use this whenever the user asks to delete or remove an event."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "calendar": {
                "type": "string",
                "description": "The name of the calendar containing the event."
            },
            "event_uid": {
                "type": "string",
                "description": "The unique identifier (UID) of the event to delete."
            }
        },
        "required": ["calendar", "event_uid"]
    }
}


def delete_event(args: dict[str, str], **kwargs) -> str:
    target_calendar = args.get("calendar")
    event_uid = args.get("event_uid")
    if not target_calendar:
        return json.dumps({"status": "error", "details": "Missing required parameter: 'calendar'"})
    if not event_uid:
        return json.dumps({"status": "error", "details": "Missing required parameter: 'event_uid'"})

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
        event = calendar.get_event_by_uid(event_uid)
        event.delete()

    except Exception as e:
        return json.dumps({"status": "error", "details": f"Failed to delete event in calendar '{target_calendar}': {str(e)}"})

    return json.dumps({"status": "OK", "details": f"Event deleted in calendar '{target_calendar}'."})
