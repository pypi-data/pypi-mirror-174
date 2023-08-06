from datetime import datetime

def format_datetime_for_api(dt: datetime) -> str:
    # 2022-10-26 00:00:00
    return dt.strftime("%Y-%m-%d %H:%M:%S")
