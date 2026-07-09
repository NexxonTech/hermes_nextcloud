import json

from caldav.calendarobjectresource import Event

from ..get_nc_instance import get_nc_instance

SCHEMA = {
    "name": "update_event",
    "description": (
        "Update an existing event in a given calendar using the updated iCalendar data."
        "Use this whenever the user asks to modify, update, reschedule, or change an event."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "calendar": {
                "type": "string",
                "description": "The name of the calendar containing the event to update."
            },
            "event": {
                "type": "string",
                "description": "The updated raw iCalendar (vCal) representation of the event. It must include the event UID to identify the event."
            }
        },
        "required": ["calendar", "event"]
    }
}


def update_event(args: dict[str, str], **kwargs) -> str:
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
        event = calendar.get_event_by_uid(Event(data=raw_event).id)
        event.data = raw_event
        event.save()

    except Exception as e:
        return json.dumps({"status": "error", "details": f"Failed to update event in calendar '{target_calendar}': {str(e)}"})

    return json.dumps({"status": "OK", "details": f"Event updated in calendar '{target_calendar}'."})
