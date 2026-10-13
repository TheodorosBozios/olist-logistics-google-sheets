# Olist Logistics Analysis for Google Sheets

An analysis of real, anonymised Brazilian e-commerce orders using spreadsheet formulas and editable charts. It examines order-to-delivery cycle time, on-time delivery, destination-state differences, recorded freight charges and fulfilment composition.

**Business question:** Where are delays concentrated, how does delivery performance change across purchase cohorts and destinations, and how do recorded shipping charges vary?

The source contains **99,441 orders** from **September 2016 to October 2018**. The analysis retains every order and calculates delivery performance on **96,470 eligible delivered orders**.

## Key results

| Metric | Result |
| --- | ---: |
| Source orders | 99,441 |
| Eligible deliveries | 96,470 |
| On-time deliveries | 89,936 |
| Late deliveries | 6,534 |
| On-time rate | 93.23% |
| Late rate | 6.77% |
| Mean order-to-delivery cycle | 12.56 days |
| Median order-to-delivery cycle | 10.22 days |
| Average recorded freight charge | 22.82 source currency units |

![Delivery overview](preview/dashboard_overview.png)

![Geographical and distribution comparisons](preview/dashboard_comparisons.png)

## Findings

- Actual and promised **calendar dates** are compared. Delivery later in the day on the promised date is still classified on time.
- SP and RJ contribute 3,315 late deliveries, or **50.73%** of all observed late deliveries. Counts and rates provide complementary views of where to investigate.
- Among states with at least 100 eligible deliveries, AL has the highest late rate: **21.41%**, or 85 of 397 deliveries. All 27 state codes remain in the workbook and exported results.
- The March 2018 purchase cohort has an **18.96%** late rate, compared with the overall **6.77%**. These are descriptive cohort results, not evidence of a particular cause.
- Multi-seller orders have a higher average recorded freight charge than single-seller orders. Item count, destination and order composition can confound that comparison.

## Workbook design

| Sheet | Purpose |
| --- | --- |
| `Dashboard` | Linked KPIs and six editable charts |
| `Analysis` | Formula-based monthly, state, seller-group, status and cycle-distribution analyses |
| `Source_Summary` | 1,671 input groups preserving counts and sums for every source order |
| `Delivery_Cycles` | All 96,470 individual eligible durations for exact median and distribution |
| `Guide` | Eligibility definitions, source-field mapping, quality measures and licence notes |

## How to use

1. Open `Logistics_Google_Sheets_Analysis.xlsx` in Excel or upload it to Google Drive and open with Google Sheets.
2. The `Dashboard` sheet shows the main KPIs and charts.
3. The `Analysis` sheet holds the formula calculations that the dashboard references.
4. To rebuild prepared inputs from a revised raw CSV, run `python scripts/prepare_data.py` from the project root, then re-import the two prepared tables into the workbook.

See [formula documentation](docs/FORMULAS.md) for the calculation logic. Formula ranges cover 1,671 prepared groups representing all 99,441 orders and all 96,470 individual eligible durations. Regenerate both prepared inputs together when changing the raw source, then review and extend ranges if necessary.

## Project files

| Path | Contents |
| --- | --- |
| `Logistics_Google_Sheets_Analysis.xlsx` | Formula-based workbook with six charts |
| `data/` | Unified CSV, prepared aggregates, delivery cycles and source metadata |
| `results/` | Result snapshots in CSV (monthly, state, seller group, status) |
| `preview/` | Workbook previews for the GitHub README |
| `docs/ANALYSIS.md` | Detailed interpretation and suggested follow-up questions |
| `docs/FORMULAS.md` | Field formulas, aggregate examples and denominator definitions |
| `scripts/prepare_data.py` | Standard-library Python preparation of additive source tables |

## Interpretation boundaries

- Cancelled and undelivered orders remain in order counts but do not count as on-time outcomes.
- Eight delivered-status records lack an actual delivery date and are excluded from delivery KPIs.
- There are 2,965 missing actual-delivery dates and 775 missing freight values in the full source. Missing freight is not imputed as zero.
- Carrier transit and handling means use their own valid timestamp samples. Reversed timestamps are omitted from stage-duration calculations, so stage means need not sum to the overall mean.
- Freight values are **recorded shipping charges** in the source units. Actual carrier operating expenses, margins and delivery-provider identifiers are absent.
- The first and last purchase months are partial. Late-rate charts omit months with no eligible deliveries; the complete monthly table retains them.
- Destination rates should be read with their sample sizes. No causal effect, forecast or statistical significance is claimed.

## Source and licence

Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), provided by Olist and collaborators. The original publisher describes it as real anonymised commercial data.

The source and derived data/analysis are distributed under **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**: attribution, non-commercial use and share-alike. Adaptations are described above. Use does not imply publisher endorsement. See [LICENSE.md](LICENSE.md).

This project is intended for non-commercial educational analysis. Native Google Sheets import and verification is a separate step when opening the workbook online.
