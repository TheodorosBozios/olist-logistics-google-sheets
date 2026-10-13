# Google Sheets formulas and data preparation

`Source_Summary` contains 1,671 prepared groups, covering all 99,441 source orders. The columns preserve additive totals and their matching observation counts. `Delivery_Cycles` contains every individual eligible duration so that the median and distribution are calculated exactly in the workbook.

Preparation is implemented by `scripts/prepare_data.py` using Python's standard library. It parses dates, validates distinct order IDs, preserves missing outcomes, assigns eligibility and compares actual/expected calendar days. It then groups records by purchase month, state, seller group and status. This is a documented preparation step; the workbook owns final aggregation, rates, weighted means and charts.

## Source ranges

- Grouped rows: `Source_Summary!A5:U1675`.
- Individual durations: `Delivery_Cycles!B5:B96474`.
- E: all orders; F: eligible deliveries; G: late deliveries.
- H/I: cycle-day sum and observations.
- J/K: transit-day sum and observations.
- L/M: handling-day sum and observations.
- N: overdue calendar-day sum, late deliveries only.
- O/P: recorded freight sum and observations.
- Q: recorded item value.

## Formula examples

Total source orders:

```text
=SUM(Source_Summary!$E$5:$E$1675)
```

Eligible deliveries:

```text
=SUM(Source_Summary!$F$5:$F$1675)
```

On-time rate in the Analysis summary:

```text
=IF(C8=0,"",C9/C8)
```

Weighted cycle mean:

```text
=IF(SUM(Source_Summary!$I$5:$I$1675)=0,"",SUM(Source_Summary!$H$5:$H$1675)/SUM(Source_Summary!$I$5:$I$1675))
```

Exact median:

```text
=MEDIAN(Delivery_Cycles!$B$5:$B$96474)
```

Orders for the purchase month in A32:

```text
=SUMIFS(Source_Summary!$E$5:$E$1675,Source_Summary!$A$5:$A$1675,A32)
```

State-level late deliveries for the code in A65:

```text
=SUMIFS(Source_Summary!$G$5:$G$1675,Source_Summary!$B$5:$B$1675,A65)
```

## Rebuild the prepared source

From the extracted project root, run:

```bash
python scripts/prepare_data.py
```

This regenerates `data/prepared_aggregates.csv` and `data/delivery_cycles.csv`. It does not author a workbook or modify the raw CSV. Existing workbook inputs are snapshots; replace both prepared inputs consistently if changing the original source.

Missing actual delivery or expected dates do not produce an on-time outcome. The source preparation compares calendar days, so delivery at 18:00 on the expected date is on time. Missing/reversed stage timestamps are excluded from the relevant sums and observation counts. Final means divide sums by matching counts and do not average group means without weights.

The documentation uses English function names and comma separators. Google Sheets can display locale-specific separators without changing the underlying calculation.
