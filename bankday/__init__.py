"""Bankday API client: business days, bank holidays and settlement dates.

Standard library only. Python 3.8+.

    from bankday import Bankday
    bd = Bankday()  # reads BANKDAY_API_KEY
    bd.add_business_days("us-fed", "2026-11-25", 2)["result"]  # '2026-11-30'
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, Optional, Union

__version__ = "1.0.0"
__all__ = ["Bankday", "BankdayError"]

DEFAULT_BASE_URL = "https://bankday.dev"
Calendar = Union[str, Iterable[str]]


class BankdayError(Exception):
    def __init__(self, status: int, code: str, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.details = details or {}


def _cal(calendar: Calendar) -> str:
    return calendar if isinstance(calendar, str) else ",".join(calendar)


class Bankday:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: float = 10.0):
        self.api_key = api_key or os.environ.get("BANKDAY_API_KEY") or os.environ.get("BANKDAY_KEY")
        self.base_url = (base_url or os.environ.get("BANKDAY_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        if not self.api_key:
            raise BankdayError(0, "missing_api_key", f"Pass api_key= or set BANKDAY_API_KEY. Free key: {self.base_url}/#signup")

    def request(self, path: str, **params: Any) -> Dict[str, Any]:
        query = {k: (str(v).lower() if isinstance(v, bool) else v) for k, v in params.items() if v is not None}
        url = f"{self.base_url}{path}" + (f"?{urllib.parse.urlencode(query)}" if query else "")
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.api_key}", "User-Agent": f"bankday-python/{__version__}"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                err = json.loads(e.read().decode("utf-8")).get("error", {})
            except ValueError:
                err = {}
            raise BankdayError(e.code, err.get("code", "http_error"), err.get("message", f"HTTP {e.code}"), err) from None

    def is_business_day(self, calendar: Calendar, date: str): return self.request("/v1/business-day", calendar=_cal(calendar), date=date)
    def today(self, calendar: Calendar, timezone: Optional[str] = None): return self.request("/v1/today", calendar=_cal(calendar), timezone=timezone)
    def add_business_days(self, calendar: Calendar, date: str, days: int): return self.request("/v1/business-days/add", calendar=_cal(calendar), date=date, days=days)
    def count_business_days(self, calendar: Calendar, start: str, end: str, include_start: bool = False):
        return self.request("/v1/business-days/count", calendar=_cal(calendar), start=start, end=end, include_start=include_start)
    def next_business_day(self, calendar: Calendar, date: Optional[str] = None, inclusive: bool = False):
        return self.request("/v1/business-days/next", calendar=_cal(calendar), date=date, inclusive=inclusive)
    def previous_business_day(self, calendar: Calendar, date: Optional[str] = None, inclusive: bool = False):
        return self.request("/v1/business-days/previous", calendar=_cal(calendar), date=date, inclusive=inclusive)
    def roll(self, calendar: Calendar, date: str, convention: str = "following"): return self.request("/v1/business-days/roll", calendar=_cal(calendar), date=date, convention=convention)
    def list_business_days(self, calendar: Calendar, start: str, end: str): return self.request("/v1/business-days", calendar=_cal(calendar), start=start, end=end)
    def holidays(self, calendar: Calendar, year: Optional[int] = None, start: Optional[str] = None, end: Optional[str] = None):
        return self.request("/v1/holidays", calendar=_cal(calendar), year=year, start=start, end=end)
    def fx_spot(self, pair: str, trade_date: str): return self.request("/v1/fx/spot", pair=pair, trade_date=trade_date)
    def ach_settlement(self, submitted_at: Optional[str] = None, type: Optional[str] = None, amount: Optional[float] = None):  # noqa: A002
        return self.request("/v1/ach/settlement", submitted_at=submitted_at, type=type, amount=amount)
    def calendars(self, type: Optional[str] = None, q: Optional[str] = None): return self.request("/v1/calendars", type=type, q=q)  # noqa: A002
    def calendar(self, calendar_id: str): return self.request(f"/v1/calendars/{urllib.parse.quote(calendar_id)}")
    def account(self): return self.request("/v1/account")
