"""Prepare additive source tables for the Google Sheets logistics analysis.

Run from the extracted project: python scripts/prepare_data.py
Requires Python 3.8+ and its standard library only. Does not create a workbook.
"""
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "Olist_Logistics_Google_Sheets.csv"
DATA = ROOT / "data"
HEADERS = ["purchase_month", "state", "seller_group", "order_status", "orders",
           "eligible_deliveries", "late_deliveries", "cycle_days_sum", "cycle_observations",
           "transit_days_sum", "transit_observations", "handling_days_sum", "handling_observations",
           "days_late_sum", "recorded_freight_sum", "freight_observations", "recorded_items_sum",
           "missing_delivery_dates", "missing_carrier_dates", "missing_freight_values", "reversed_transit_records"]


def timestamp(value):
    return datetime.fromisoformat(value) if value else None


def monetary(value):
    return float(value) if value else None


def prepare():
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len({row["order_id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate order IDs; resolve them before preparation.")
    groups = defaultdict(lambda: [0.0] * 17)
    cycle_values = []
    for row in rows:
        purchase = timestamp(row["order_purchase_timestamp"])
        carrier = timestamp(row["order_delivered_carrier_date"])
        delivered = timestamp(row["order_delivered_customer_date"])
        estimated = timestamp(row["order_estimated_delivery_date"])
        if purchase is None:
            raise ValueError("A purchase date is missing; review the reporting-month rule.")
        sellers = int(row["distinct_sellers_count"]) if row["distinct_sellers_count"] else None
        seller_group = "Unspecified" if sellers is None else "Single seller" if sellers == 1 else "Multiple sellers"
        key = (purchase.strftime("%Y-%m"), row["customer_state"], seller_group, row["order_status"])
        facts = groups[key]
        eligible = bool(row["order_status"] == "delivered" and delivered and estimated and
                        delivered >= purchase and estimated.date() >= purchase.date())
        late = int(delivered.date() > estimated.date()) if eligible else 0
        facts[0] += 1
        facts[1] += eligible
        facts[2] += late
        if eligible:
            duration = (delivered - purchase).total_seconds() / 86400
            facts[3] += duration
            facts[4] += 1
            cycle_values.append([row["order_id"], duration])
            if carrier and delivered >= carrier:
                facts[5] += (delivered - carrier).total_seconds() / 86400
                facts[6] += 1
            if carrier and carrier >= purchase:
                facts[7] += (carrier - purchase).total_seconds() / 86400
                facts[8] += 1
            if late:
                facts[9] += (delivered.date() - estimated.date()).days
        freight = monetary(row["freight_value"])
        items = monetary(row["items_value"])
        if freight is not None:
            facts[10] += freight
            facts[11] += 1
        if items is not None:
            facts[12] += items
        facts[13] += delivered is None
        facts[14] += carrier is None
        facts[15] += freight is None
        facts[16] += bool(delivered and carrier and delivered < carrier)
    records = [[*key, *groups[key]] for key in sorted(groups)]
    if sum(row[4] for row in records) != len(rows):
        raise ValueError("Grouped order counts do not reconcile to the source.")
    if sum(row[5] for row in records) != len(cycle_values):
        raise ValueError("Eligible counts do not reconcile to the cycle-value list.")
    with (DATA / "prepared_aggregates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADERS)
        writer.writerows(records)
    with (DATA / "delivery_cycles.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["order_id", "delivery_cycle_days"])
        writer.writerows(cycle_values)
    validation = {"source_orders": len(rows), "prepared_groups": len(records),
                  "eligible_cycle_values": len(cycle_values),
                  "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    (DATA / "preparation_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    prepare()
