# city-of-saskatoon-smart-util

An unofficial Python module for interacting with the City of Saskatoon's SmartUtil service.

Features:

1. Fetch the meters from your SmartUTIL account
1. Fetch the previous 24 hours of data from your SmartUTIL account

## Usage

```python
from city_of_saskatoon_smart_util import SmartUtil
su = SmartUtil('username', 'password')
su.login()

meters = su.get_meters()

usage = su.get_past_24_hour_usage(meters[0])
# [{'timestamp': '2022-10-26 21:15', 'value': 0.27}, {'timestamp': '2022-10-26 21:30', 'value': 0.29}, {'timestamp': '2022-10-26 21:45', 'value': 0.29}, ...]
```