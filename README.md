# bankday

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

## More

- Every method maps to one endpoint in the [API docs](https://bankday.dev/docs).
- Errors raise `BankdayError` with `.status`, `.code` and the message.
- [Pricing](https://bankday.dev/pricing): free tier, then usage based plans.
- [JavaScript client](https://github.com/ParsingMAINFRAME/bankday-js) and an [MCP server](https://bankday.dev/docs#mcp) for AI agents.

MIT licensed.
