# bankday

[![tests](https://github.com/ParsingMAINFRAME/bankday-python/actions/workflows/test.yml/badge.svg)](https://github.com/ParsingMAINFRAME/bankday-python/actions/workflows/test.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Python client for the [Bankday API](https://bankday.dev): business days, bank holidays and settlement dates for each payment system. Covers the US Federal Reserve (FedACH and Fedwire), Payments Canada, TARGET2, UK Bacs, 28 stock exchanges and 247 countries, through 2040.

No dependencies. Python 3.8+.

```bash
pip install bankday
```

Get a free API key at [bankday.dev](https://bankday.dev/#signup) (no card needed), then:

```python
from bankday import Bankday

bd = Bankday()  # reads BANKDAY_API_KEY

bd.is_business_day("us-fed", "2026-11-11")["business_day"]   # False (Veterans Day)
bd.is_business_day("us-fed", "2027-12-24")["business_day"]   # True (see below)
bd.add_business_days("us-fed", "2026-11-25", 2)["result"]    # '2026-11-30'
bd.roll("us-fed", "2027-07-05", "following")["result"]       # '2027-07-06'
bd.is_business_day(["us-fed", "eu-target2"], "2026-04-03")   # joint calendar: open on both rails?
bd.fx_spot("EURUSD", "2026-11-25")["spot_date"]              # '2026-11-27'
bd.ach_settlement(type="same_day")                           # next Same Day ACH settlement
bd.payroll_schedule("us-fed", "semimonthly", year=2027)      # paydays moved off holidays, with submit-by dates
```

## Why not a holiday library?

Federal holidays and Federal Reserve closures are not the same list. When a holiday falls on a Saturday, federal offices close on the Friday before, but the Fed stays open and ACH and wires settle as normal. That happened on July 3, 2026, and it happens again on June 18 and December 24, 2027. Payments Canada, TARGET2 and Bacs each have their own rules too. Bankday follows each operator's published schedule, so you don't have to.

## Methods

Every method returns the parsed JSON response as a dict. Calendars are ids like `us-fed`, `eu-target2`, `uk-bacs`, `ca-payments`, `xnys` or a country code (`gb`, `de`, `jp`), or a list of them for a joint calendar.

| Method | Endpoint |
|---|---|
| `is_business_day(calendar, date)` | [`/v1/business-day`](https://bankday.dev/docs#business-day) |
| `today(calendar, timezone=None)` | [`/v1/today`](https://bankday.dev/docs#today) |
| `add_business_days(calendar, date, days)` | [`/v1/business-days/add`](https://bankday.dev/docs#add) |
| `count_business_days(calendar, start, end, include_start=False)` | [`/v1/business-days/count`](https://bankday.dev/docs#count) |
| `next_business_day(...)` / `previous_business_day(...)` | [`/v1/business-days/next`](https://bankday.dev/docs#next), `/previous` |
| `roll(calendar, date, convention="following")` | [`/v1/business-days/roll`](https://bankday.dev/docs#roll) |
| `list_business_days(calendar, start, end)` | [`/v1/business-days`](https://bankday.dev/docs#list) |
| `holidays(calendar, year=None, start=None, end=None)` | [`/v1/holidays`](https://bankday.dev/docs#holidays) |
| `fx_spot(pair, trade_date)` | [`/v1/fx/spot`](https://bankday.dev/docs#fx) |
| `ach_settlement(submitted_at=None, type=None, amount=None)` | [`/v1/ach/settlement`](https://bankday.dev/docs#ach) |
| `payroll_schedule(calendar, frequency, year=None, anchor=None, ...)` | [`/v1/payroll/schedule`](https://bankday.dev/docs#payroll) |
| `calendars(type=None, q=None)` / `calendar(calendar_id)` | [`/v1/calendars`](https://bankday.dev/docs#calendars) |
| `account()` | [`/v1/account`](https://bankday.dev/docs#account) |

## Configuration

```python
Bankday(
    api_key="bd_live_...",           # or the BANKDAY_API_KEY environment variable
    base_url="https://bankday.dev",  # or BANKDAY_BASE_URL
    timeout=10.0,                    # seconds
)
```

## Errors

Failed requests raise `BankdayError` with `.status` (HTTP status), `.code` (for example `unknown_calendar`, `date_out_of_range`, `quota_exceeded`) and a readable message.

```python
from bankday import BankdayError

try:
    bd.is_business_day("narnia", "2026-01-02")
except BankdayError as e:
    if e.code == "unknown_calendar":
        ...
```

## More

- Full parameter and response reference: [bankday.dev/docs](https://bankday.dev/docs).
- [Pricing](https://bankday.dev/pricing): free tier, then usage based plans.
- [JavaScript client](https://github.com/ParsingMAINFRAME/bankday-js) and an [MCP server](https://bankday.dev/docs#mcp) for AI agents.
- [Free Federal Reserve holiday dataset](https://github.com/ParsingMAINFRAME/fed-holidays)

## License

MIT
