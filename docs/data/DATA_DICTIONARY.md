# Data dictionary

The seven business-case CSV files below contain synthetic teaching observations. The notebooks also use the observed datasets listed after the table. Simulations are labelled separately from observed records.

| File | Unit of analysis | Key fields | Teaching purpose |
| --- | --- | --- | --- |
| `cafe_service.csv` | One café service interval | `arrivals`, `staff_on_shift`, `mean_wait_minutes`, `satisfaction` | Evidence, comparisons, and outcomes |
| `quickbite_pilot.csv` | One customer order | `offer_group`, `delivery_minutes`, `rating`, `repeat_order_30d` | Business question and evaluation design |
| `freshcart_deliveries.csv` | One delivery | `distance_km`, `rain`, `riders_available`, `late` | Lifecycle artefacts and success criteria |
| `project_handoffs.csv` | One project hand-off | `from_role`, `to_role`, `artefact`, `days_waiting`, `accepted` | Roles, hand-offs, and accountability |
| `hotel_bookings.csv` | One hotel booking | `lead_time_days`, `channel`, `deposit_type`, `cancelled` | Grain, sources, and data fitness |
| `service_demand.csv` | One daily service total | `date`, `demand`, `holiday`, `promotion` | Forecast origin, seasonality, and validation |
| `delivery_regression.csv` | One delivery | `distance_km`, `items`, `rain_mm`, `delivery_minutes` | Regression, loss functions, residuals, influence |

## Observed datasets

| Dataset | Recorded unit and target | Use |
| --- | --- | --- |
| Wine Recognition | 178 wine samples, 13 chemical measurements, three cultivars | Lectures 1–5: a complete supervised workflow viewed through each lecture's project question. Lectures 7–8: predict flavanoids from total phenols to study loss geometry. Lectures 9–10: classification and representation. |
| Diabetes study | 442 participants with baseline measurements and progression one year later | Lectures 1, 3, 7 and 8: association and held-out regression. Baseline features supplied by the loader are already standardised; interpret coefficients accordingly. |
| Wisconsin diagnostic breast cancer | 569 diagnostic records, 30 measured features and a recorded class | Lectures 2 and 9: probabilities, discrimination, calibration and thresholds. |
| Annual sunspot activity | Annual observed activity, 1700–2008 | Lecture 6: chronological hold-out forecasting. |

Wine source: Aeberhard and Forina, [UCI Wine Recognition](https://archive.ics.uci.edu/dataset/109/wine), DOI 10.24432/C5PC7J, CC BY 4.0. The scikit-learn loader codes the original classes 1–3 as 0–2. The source does not specify physical units for every field; figures retain the recorded feature names rather than inventing units. Predicting flavanoids is a course-defined regression task on two observed fields, distinct from the dataset's original classification task.

The [scikit-learn dataset documentation](https://scikit-learn.org/stable/datasets/toy_dataset.html) gives provenance and field definitions for Wine, Diabetes and Wisconsin diagnostic data. The `statsmodels.datasets.sunspots` dataset supplies annual sunspot activity. These datasets are bundled with installed dependencies and need no network access when a student runs the notebooks. Small historical datasets support classroom examples; external deployment needs evidence from the intended population.
