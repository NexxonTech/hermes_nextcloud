from . import src


def register(ctx):
    ctx.register_tool(name="list_calendars", toolset="nextcloud",
                      schema=src.calendar.list_calendars.SCHEMA, handler=src.calendar.list_calendars.list_calendars)
    ctx.register_tool(name="list_events", toolset="nextcloud",
                      schema=src.calendar.list_events.SCHEMA, handler=src.calendar.list_events.list_events)
    ctx.register_tool(name="delete_event", toolset="nextcloud",
                      schema=src.calendar.delete_event.SCHEMA, handler=src.calendar.delete_event.delete_event)
    ctx.register_tool(name="create_event", toolset="nextcloud",
                      schema=src.calendar.create_event.SCHEMA, handler=src.calendar.create_event.create_event)
    ctx.register_tool(name="update_event", toolset="nextcloud",
                      schema=src.calendar.update_event.SCHEMA, handler=src.calendar.update_event.update_event)
