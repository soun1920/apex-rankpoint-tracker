from datetime import datetime
from typing import Optional


def now():
    return datetime.now()


def rp_diff(self, before: int, after: int) -> Optional[int]:
    diff = after - before
    if diff == 0:
        return None
    else:
        return diff
