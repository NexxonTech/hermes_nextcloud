LIST_CALENDARS = {
    "name": "list_calendars",
    "description": (
        "List all calendars available in the Nextcloud instance."
        "Use this to get the name of the calendar for the other endpoints."
    )
}

LIST_EVENTS = {
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
