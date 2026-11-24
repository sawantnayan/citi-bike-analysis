import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load CSV file
df = pd.read_csv("citi-bike-analysis.csv",
                 low_memory=False,
    dtype={
        "start_station_id": "string",
        "end_station_id": "string"
    })

print(df.head())
print("Dataset Shape:", df.shape)
print("Column Names:", df.columns.tolist())


# Exploring Data

print("----- Exploring Data-----")
print("\nFirst 5 records:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())


# Data Cleaning

# Convert date columns into datetime format
df["started_at"] = pd.to_datetime(
    df["started_at"],
    format="mixed",
    errors="coerce"
)

df["ended_at"] = pd.to_datetime(
    df["ended_at"],
    format="mixed",
    errors="coerce"
)

# Remove records with invalid dates
df = df.dropna(subset=["started_at", "ended_at"])

# Calculate ride duration in minutes
df["ride_duration"] = (
    df["ended_at"] - df["started_at"]
).dt.total_seconds() / 60

# Remove invalid ride durations
df = df[
    (df["ride_duration"] > 0) &
    (df["ride_duration"] <= 1440)
].copy()

# Create additional columns
df["hour"] = df["started_at"].dt.hour
print(df["hour"])

df["day_of_week"] = df["started_at"].dt.day_name()
print(df["day_of_week"])

df["month"] = df["started_at"].dt.month_name()
print(df["month"])

print("\nData cleaning completed!")


# RIDER TYPE ANALYSIS

print("\nRider Type Analysis:")
print(df["member_casual"].value_counts())

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="member_casual"
)

plt.title("Number of Rides by Rider Type")
plt.xlabel("Rider Type")
plt.ylabel("Number of Rides")

plt.tight_layout()
plt.savefig("rider_type_analysis.png")
plt.show()

# HOURLY RIDE DEMAND

hourly_rides = df.groupby("hour").size()

plt.figure(figsize=(10, 5))

hourly_rides.plot(kind="bar")

plt.title("Hourly Citi Bike Ride Demand")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Rides")

plt.tight_layout()
plt.savefig("hourly_demand.png")
plt.show()

# WEEKDAY RIDE ANALYSIS

weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

weekday_rides = (
    df.groupby("day_of_week")
    .size()
    .reindex(weekday_order)
)

plt.figure(figsize=(10, 5))

weekday_rides.plot(kind="bar")

plt.title("Citi Bike Rides by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Number of Rides")

plt.tight_layout()
plt.savefig("weekday_demand.png")
plt.show()

# RIDE DURATION ANALYSIS

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="ride_duration",
    bins=40
)

plt.title("Distribution of Ride Duration")
plt.xlabel("Ride Duration (Minutes)")
plt.ylabel("Number of Rides")

plt.tight_layout()
plt.savefig("ride_duration.png")
plt.show()

print("\nAverage Ride Duration:")
print(round(df["ride_duration"].mean(), 2), "minutes")

# TOP START STATIONS

top_stations = (
    df["start_station_name"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(11, 6))

top_stations.sort_values().plot(kind="barh")

plt.title("Top 10 Most Popular Start Stations")
plt.xlabel("Number of Rides")
plt.ylabel("Station")

plt.tight_layout()
plt.savefig("top_start_stations.png")
plt.show()

# RIDER TYPE BY HOUR

rider_hour = (
    df.groupby(["hour", "member_casual"])
    .size()
    .unstack(fill_value=0)
)

rider_hour.plot(
    kind="line",
    figsize=(10, 5),
    marker="o"
)

plt.title("Hourly Demand by Rider Type")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Rides")

plt.tight_layout()
plt.savefig("rider_hour_analysis.png")
plt.show()

# STATION NET FLOW ANALYSIS

start_counts = (
    df["start_station_name"]
    .value_counts()
)

end_counts = (
    df["end_station_name"]
    .value_counts()
)

station_flow = pd.concat(
    [start_counts, end_counts],
    axis=1
).fillna(0)

station_flow.columns = ["rides_started", "rides_ended"]

station_flow["net_flow"] = (
    station_flow["rides_started"] -
    station_flow["rides_ended"]
)

print("\nTop 10 Stations by Net Flow:")
print(
    station_flow.sort_values(
        "net_flow",
        ascending=False
    ).head(10)
)

station_flow.to_csv(
    "station_net_flow.csv"
)

# SAVE CLEANED DATA

df.to_csv(
    "cleaned_citibike_data.csv",
    index=False
)

# FINAL SUMMARY

print("\n====================================")
print("CITI BIKE ANALYSIS COMPLETED")
print("====================================")

print("Total Rides:", len(df))

print(
    "Average Ride Duration:",
    round(df["ride_duration"].mean(), 2),
    "minutes"
)

print("\nRider Type Counts:")
print(df["member_casual"].value_counts())

