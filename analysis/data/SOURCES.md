# Data sources

Every number in this project comes from a public source. The CSVs are snapshots taken in October 2026. Re-run `fetch_ons.py` to refresh the ONS series from the official API.

| File | What it holds | Source |
|---|---|---|
| `online_share.csv` | Internet sales as % of total UK retail sales, annual average (ONS series J4MC) | ONS Retail Sales Index, series J4MC ([ONS](https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/j4mc/drsi)). Annual values as reported in [Eightx, *UK online retail share 2026*](https://eightx.co/blog/uk-online-retail-share-2026), citing the ONS release of 22 May 2026. Years not reported there are left out, not estimated. |
| `store_closures.csv` | UK store closures and job losses, chains vs independents | Centre for Retail Research, as reported by [Insight DIY, 31 Dec 2024](https://www.insightdiy.co.uk/news/crr-2024-retail-job-losses-and-store-closures/14569.htm). 2025 is CRR's forecast (17,349 closures, 201,953 job losses), with no chain/independent split. |
| `vacancy_by_location.csv` | GB shop vacancy rate by location type | BRC–Local Data Company Vacancy Monitor, via [Insight DIY (Q3 2021)](https://www.insightdiy.co.uk/news/brc-shop-vacancy-rate-plateaus/10496.htm), [Bira (Q2 2022)](https://bira.co.uk/news/retail-vacancy-rates-on-the-high-street/), [Furniture News (Q2 2023)](https://furniturenews.net/news/retail-parks-continue-to-prove-resilient-reports-brc-ldc), [Green Street News (Q4 2023, and the Q4 2019 baseline)](https://greenstreetnews.com/article/retail-vacancies-flatline-as-high-street-struggles-temper-recovery/). |
| `vacancy_by_region_q4_2023.csv` | Vacancy by region, Q4 2023 | Local Data Company, via [Green Street News](https://greenstreetnews.com/article/retail-vacancies-flatline-as-high-street-struggles-temper-recovery/) |
| `footfall_2025.csv` | Footfall change year on year | [BRC–Sensormatic IQ footfall monitor, 9 Jan 2026](https://brc.org.uk/news-and-events/news/corporate-affairs/2026/ungated/footfall-falters-as-shoppers-hold-out-for-sales/) |
| `business_rates_england.csv` | Business rates multipliers and retail, hospitality and leisure (RHL) relief, England | 2024/25 and 2025/26: [Armstrong Watson, May 2025](https://www.armstrongwatson.co.uk/news/2025/05/changes-business-rates-and-targeted-retail-hospitality-and-leisure-support). 2026/27: [Spelthorne Borough Council](https://www.spelthorne.gov.uk/page/661/business-rates-multipliers-20262027). |

Also used in the case write-up:

- Centre for Cities, *Checking out: the varying performance of high streets across the country* (July 2025), summarised by [Specification Online](https://specificationonline.co.uk/articles/2025-07-16/centre-for-cities/empty-shops-indicate-an-oversupply-of-retail-space-in-city-centres)
- High Street Rental Auctions, in force in England from 2 December 2024 ([Trowers & Hamlins](https://www.trowers.com/insights/2024/december/a-festive-frenzy-for-high-streets-with-rental-auctions-coming-into-force))

**Caveats.** Vacancy data before 2024 is the latest quarterly series publicly reported in full. Figures from secondary reports should be checked against the original publisher before being cited in anything formal.
