from src.calendar.create_event import create_event
from src.calendar.update_event import update_event
from src.calendar.delete_event import delete_event


def test_create_event():
    create_event_args = {
        "calendar": "Personale",
        "event": '''
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//NexxonTech//Nyx//EN
BEGIN:VEVENT
UID:nyx-test-20260710@nexxontech.it
DTSTAMP:20260709T120000Z
DTSTART:20260710T090000
DTEND:20260710T100000
SUMMARY:Test event
END:VEVENT
END:VCALENDAR
        '''
    }
    print(create_event(create_event_args))

def test_update_event():
    update_event_args = {
        "calendar": "Personale",
        "event": '''
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//NexxonTech//Nyx//EN
BEGIN:VEVENT
UID:nyx-test-20260710@nexxontech.it
DTSTAMP:20260709T130000Z
DTSTART:20260710T110000
DTEND:20260710T120000
SUMMARY:Test event
END:VEVENT
END:VCALENDAR
        '''
    }
    print(update_event(update_event_args))


def test_delete_event():
    delete_event_args = {
        "calendar": "Personale",
        "event_uid": "nyx-test-20260710@nexxontech.it"
    }
    print(delete_event(delete_event_args))

if __name__ == "__main__":
    #test_create_event()
    #test_update_event()
    test_delete_event()
