from city_of_saskatoon_auth import Session
from datetime import datetime, timedelta
from time import sleep

from .utils import format_datetime_for_api

class SmartUtil:

    def __init__(self, username: str, password: str, archive: bytes = None):
        self.username = username
        self.password = password
        if archive:
            self.session = Session.from_archive(archive)
        else:
            self.session = Session(self.username, self.password)
    
    def login(self) -> None:
        self.session.login()
        self.session.smart_util_login()

    def get_meters(self, commodities: list[str] = None):
        commodities = commodities or self._get_commodoties()
        return [self._get_meter(commodity) for commodity in commodities]
    
    # Returns the last 24 hour's usage in 15-minute intervals
    def get_past_24_hour_usage(self, meter):
        end = datetime.now()
        start = end - timedelta(days=1)
        resp = self.session.post('https://smartutil.saskatoon.ca/HomeConnect/Controller/Usage', json={
            "meterId": meter['meter_id'],
            "startDtm": format_datetime_for_api(start),
            "endDtm": format_datetime_for_api(end),
            "channel": meter['unit'],
            "intervalLengthStr": "15",
            "rollup": "None"
        })
        jr = resp.json()
        return [{
            'timestamp': item[0],
            'value': item[1]
        } for item in jr['resultsTiered'][0][0]]

    # PRIVATE
    
    def _get_commodoties(self) -> list[str]:
        resp = self.session.get('https://smartutil.saskatoon.ca/HomeConnect/Controller/Commodities')
        assert resp.status_code == 200
        jr = resp.json()
        return jr

    def _get_meter(self, commodity: str):
        resp = self.session.post('https://smartutil.saskatoon.ca/HomeConnect/Controller/Usage', json={
            'forceInitialCommodityTp': commodity,
            'showHourlyUsageStatus': False,
            'rollup': 'Day'
        })
        assert resp.status_code == 200
        jr = resp.json()
        return {
            'meter_id': jr['meterId'],
            'unit': jr['uom'],
            'commodity': jr['forceInitialCommodityTp']
        }