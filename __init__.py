from . import schemas
from . import tools


def register(ctx):
    ctx.register_tool(name="list_calendars", toolset="nextcloud",
                      schema=schemas.LIST_CALENDARS, handler=tools.list_calendars)
    ctx.register_tool(name="list_events", toolset="nextcloud",
                      schema=schemas.LIST_EVENTS, handler=tools.list_events)
