# bankday

Official Python client for the [Bankday API](https://bankday.dev/docs): business days, bank holidays and settlement dates for US ACH/Fedwire, TARGET2, UK Bacs, Payments Canada, 28 stock exchanges and 247 countries.

Standard library only (no dependencies). Python 3.8+.

```bash
pip install bankday
```

```python
from bankday import Bankday

bd = Bankday()  # reads BANKDAY_API_KEY; free key at /#signup

bd.is_business_day("us-fed", "2026-10-12")["business_day"]          # False (Columbus Day)
bd.add_business_days("us-fed", "2026-11-25", 2)["result"]           # '2026-11-30'
bd.is_business_day(["us-fed", "eu-target2"], "2026-04-03")          # joint calendar
bd.fx_spot("EURUSD", "2026-11-25")["spot_date"]                     # '2026-11-27'
bd.ach_settlement(type="same_day")
```

Errors raise `BankdayError` with `.status`, `.code` and the message.

MIT licensed.
