from datetime import datetime, timezone
from dateutil import parser

def convertToLTZ(time):
    timeLTZ = parser.parse(time).replace(tzinfo=timezone.utc).astimezone(tz=None)

    return timeLTZ