"""Live test: BANKDAY_API_KEY=... python test_live.py"""
from bankday import Bankday, BankdayError

bd = Bankday()
assert bd.is_business_day("us-fed", "2026-10-12")["business_day"] is False
assert bd.add_business_days("us-fed", "2026-11-25", 2)["result"] == "2026-11-30"
assert bd.is_business_day(["us-fed", "eu-target2"], "2026-04-03")["business_day"] is False
assert bd.fx_spot("EURUSD", "2026-11-25")["spot_date"] == "2026-11-27"
assert bd.is_business_day("xnys", "2026-11-27")["early_closes"][0]["close_time"] == "13:00"
assert bd.count_business_days("gb", "2026-12-24", "2026-12-31", include_start=True)["business_days"] >= 1
try:
    bd.is_business_day("narnia", "2026-01-02")
    raise AssertionError("expected 404")
except BankdayError as e:
    assert e.status == 404 and e.code == "unknown_calendar"
pay = bd.payroll_schedule("us-fed", "semimonthly", year=2027)
assert next(p for p in pay["pay_dates"] if p["scheduled"] == "2027-02-15")["pay_date"] == "2027-02-12"
print("bankday-python: all checks passed")
