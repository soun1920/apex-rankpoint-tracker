from datetime import datetime
from typing import Optional


def now():
    return datetime.now()


def rp_diff(before: int, after: int) -> Optional[int]:
    return after - before
