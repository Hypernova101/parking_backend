import pandas as pd
import os

df = pd.read_csv(os.path.join("datasets", "treas_parking_payments_2025_datasd.csv"))

df['date_trans_start'] = pd.to_datetime(df['date_trans_start'])
df['date_meter_expire'] = pd.to_datetime(df['date_meter_expire'])

df['day_of_week'] = df['date_trans_start'].dt.day_name()
df['hour'] = df['date_trans_start'].dt.hour
df['is_weekend'] = df['date_trans_start'].dt.weekday >= 5  # 5=Saturday, 6=Sunday
df['month'] = df['date_trans_start'].dt.month

df['occupied_duration'] = (df['date_meter_expire'] - df['date_trans_start']).dt.total_seconds() / 60

df['occupied'] = (df['occupied_duration'] > 0).astype(int)

print(df[['pole_id', 'day_of_week', 'hour', 'is_weekend', 'month', 'occupied_duration', 'occupied']].head())
