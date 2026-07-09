import json

from ..get_nc_instance import get_nc_instance

SCHEMA = {
    "name": "list_calendars",
    "description": (
        "List all calendars available in the Nextcloud instance."
        "Use this to get the name of the calendar for the other endpoints."
    )
}

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
