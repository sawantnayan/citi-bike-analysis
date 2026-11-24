# Citi Bike Sharing Demand & Station Imbalance Analysis

## Business problem
A bike-share operator needs to understand when rides occur, how member and casual riders behave, and which stations experience high departures or arrivals. This analysis uses trip records to identify demand patterns and net station flows.

## Business questions
1. How many rides are taken by members and casual riders?
2. Which hours and weekdays have the highest demand?
3. How does ride duration differ by rider type?
4. Which start stations are busiest?
5. Which stations have the largest net departures or arrivals?
6. How does demand change by month?

## Analysis and data-quality rules
- Parse start/end timestamps and calculate ride duration in minutes.
- Remove missing timestamps and impossible/non-positive durations.
- Consider flagging rides longer than 24 hours for review rather than assuming they are valid.
- A trip table measures completed rides, not real-time bike availability.
- Net station flow is `arrivals - departures`; it is not proof of actual stock-outs or station inventory.

## Outputs
-citi_bike_cleaned.csv
- station_net_flow.csv
- hourly_demand.png
- weekday_demand.png
- rider_type_analysis.png
- top_start_stations.png
- rider_hour_analysis.png
- ride_duration.png


## Key insights to fill in after running
- Total valid rides: [208898]
- Member share counts: [182554]
- Casual share: [26344]
- Peak hour/day: [17:00/Wednesday]
- Median ride duration by rider type: [10.5,15.2]
- Top start station: [W 21 St & 6 Ave]
