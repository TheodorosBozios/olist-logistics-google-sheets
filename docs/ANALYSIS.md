# Logistics analysis

## Scope

The unit of analysis is one order. The input contains 99,441 distinct order IDs, customer destination codes, five operational timestamps, source order status, item and seller counts, item values and recorded freight charges.

Eligibility requires delivered status, numeric purchase/actual/expected timestamps, actual delivery at or after purchase, and an expected calendar day at or after the purchase day. In this snapshot the eligible population is 96,470. Every percentage uses its stated denominator.

## Delivery reliability

89,936 eligible orders arrived on or before the promised calendar day. 6,534 arrived afterwards. The on-time rate is 93.23% and the late rate is 6.77%.

Comparing full actual timestamps to a promised date at midnight would incorrectly mark many same-day deliveries late. The workbook therefore uses `INT(actual)` and `INT(expected)` for the lateness decision.

## Cycle and operational stages

The mean purchase-to-customer cycle is 12.56 elapsed days and the median is 10.22 days. The gap between mean and median indicates a right tail in cycle durations; the distribution chart retains longer-cycle orders rather than dropping them.

The mean valid carrier-to-customer interval is 9.33 days. The mean valid purchase-to-carrier interval is 3.23 days. There are 23 source records with customer delivery before carrier hand-off, so those reversed transit intervals are not used in the transit mean. Samples differ across stage measures.

Late deliveries exceed the promised calendar day by 10.62 days on average. This late-only average excludes on-time orders rather than averaging their legitimate zero overdue days into the delay severity measure.

## Destination differences

The table below ranks states with at least 100 eligible deliveries by late rate. The workbook and `state_results.csv` retain every state, including smaller samples.

| State | Eligible | Late | Late rate | Mean cycle days |
| --- | ---: | ---: | ---: | ---: |
| AL | 397 | 85 | 21.41% | 24.54 |
| MA | 717 | 125 | 17.43% | 21.57 |
| SE | 335 | 51 | 15.22% | 21.52 |
| PI | 476 | 66 | 13.87% | 19.46 |
| CE | 1,279 | 176 | 13.76% | 21.27 |

The largest observed late counts are SP (1,820) and RJ (1,495). Together they account for 50.73% of all late deliveries. SP's late rate is 4.49%, while RJ's is 12.11%. Reviewing only rates would miss a high-volume destination such as SP; reviewing only counts would miss smaller destinations with poor observed reliability.

## Purchase cohorts

All 26 purchase months are included in the monthly table. September 2016 has only one eligible delivery; its 100% observed late rate should be read with that sample size. November 2016 contains no orders. September and October 2018 have no eligible delivered outcomes in this snapshot, so their performance rates remain unavailable. The performance-chart helper includes only the 23 cohorts with eligible outcomes and does not plot unavailable rates as zero.

The March 2018 cohort has 1,328 late deliveries among 7,003 eligible deliveries, a rate of 18.96%. February 2018 records 14.13%, and November 2017 records 12.40%. These differences identify cohorts for follow-up; this source alone cannot explain the causes.

## Freight and seller composition

Recorded freight charges total 2,251,909.54 source currency units across 98,666 observed orders. The mean charge is 22.82. The weighted charge share, calculated as total freight divided by total recorded items plus freight, is 14.21%. This is a ratio of totals rather than an unweighted average of order-level percentages.

Single-seller orders have an average recorded charge of 22.51; multiple-seller orders have an average of 46.63. Multiple-seller orders are only a small subset of the source, and item count and destination mix may explain part of the difference. No causal effect or carrier profitability is inferred.

## Suggested follow-up

1. Investigate high-volume late destinations SP and RJ together with higher-rate states AL and MA, using the individual order records.
2. Examine the March and February 2018 cohorts with valid stage timestamps to separate observed handling and transit patterns.
3. Add carrier identifiers, origin-destination routes, service levels and actual transport expenses before assessing provider performance or cost efficiency.
4. Retain eligibility and missing-outcome rules when replacing or expanding the source so that changes in data coverage do not masquerade as performance improvements.
