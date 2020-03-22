import datetime
from typing import List, Set, Tuple

import dateutil.parser
from dateutil.tz import tzlocal
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GoogleCalendarEvents(object):
    def __init__(self, credentials: Credentials) -> None:
        self._credentials = credentials
        self._service = build('calendar', 'v3', credentials=self.credentials)
        self._selected_calendars: List[str] = []
        self._available_calendars: Set[str] = set()  
        self._all_events: List[Tuple[datetime.datetime, str]] = []   
        self.list_calendars()

    @property
    def credentials(self) -> Credentials:
        return self._credentials

    @property
    def selected_calendars(self) -> List[str]:
        return self._selected_calendars

    def select_calendar(self, calendar_id: str) -> None:
        if calendar_id in self._available_calendars:
            self._selected_calendars.append(calendar_id)

    def list_calendars(self, max_result: int = 100) -> List[Tuple[str, str]]:
        """
        Get a list of calendars with id and summary
        Args:
            max_result: Max number of results

        Returns:
            List of pairs. Each pair contains id and summary
        """
        try:
            calendar_results = self._service.calendarList().list(
                maxResults=max_result).execute()
            calendars = calendar_results.get('items', [])
            calendar_with_id = []
            for calendar in calendars:
                calendar_with_id.append((calendar['id'], calendar['summary']))
                self._available_calendars.add(calendar['id'])
            return calendar_with_id
        except Exception as exception:
            print(exception)
        return []

    def get_sorted_events(
            self,
            max_results: int = 10) -> List[Tuple[datetime.datetime, str]]:
        """
        Events are sorted in time in ascending order
        :param max_results: Max amount of events to return
        :return: List of pairs. Each pair contains date of the event and text
        """
        # TODO: Handle read timeout
        all_events: List[Tuple[datetime.datetime, str]] = []  

        # 'Z' indicates UTC time
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            for calendar_id in self._selected_calendars:
                events = self._service.events().list(
                    calendarId=calendar_id,
                    timeMin=now,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy='startTime').execute()
                events = events.get('items', [])
                for event in events:
                    start_time = event['start'].get('dateTime',
                                                    event['start'].get('date'))
                    summary = event['summary']
                    time_parsed = dateutil.parser.parse(start_time)
                    if time_parsed.tzinfo is None:
                        time_parsed = time_parsed.replace(tzinfo=tzlocal())
                    all_events.append(
                        (time_parsed.astimezone(tzlocal()), summary))
            all_events.sort(key=lambda e: e[0])
            if len(all_events) > max_results:
                all_events = all_events[:max_results]
            self._all_events = all_events
        except Exception as exception:
            print(exception)
        return self._all_events
