import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# Load the data
df = pd.read_csv('datasets/treas_parking_payments_2025_datasd.csv')

# Data wrangling
df['date_trans_start'] = pd.to_datetime(df['date_trans_start'], errors='coerce')
df['day_of_week'] = df['date_trans_start'].dt.dayofweek
df['hour_of_day'] = df['date_trans_start'].dt.hour
df['parking_available'] = 1

# Feature engineering
df['lagged_parking_available'] = df.groupby('pole_id')['parking_available'].shift(1)
df['lagged_parking_available'] = df['lagged_parking_available'].fillna(0)
df['time_slot'] = df['day_of_week'].astype(str) + '_' + df['hour_of_day'].astype(str)
df['lagged_day_interaction'] = df['lagged_parking_available'] * df['day_of_week']
df['trans_amt_binned'] = pd.cut(df['trans_amt'], bins=[0, 5, 10, 20, 50, 100, float('inf')], labels=False)
df = df.drop(['date_trans_start', 'date_meter_expire'], axis=1)

# Filter infrequent pole_ids
pole_id_counts = df['pole_id'].value_counts()
single_occurrence_pole_ids = pole_id_counts[pole_id_counts == 1].index
filtered_df = df[~df['pole_id'].isin(single_occurrence_pole_ids)]

# Create target variable based on time of day
filtered_df.loc[:, 'parking_available'] = np.where((filtered_df['hour_of_day'] >= 7) & (filtered_df['hour_of_day'] <= 19), 1, 0)

# Define features and target
X = filtered_df[['pole_id', 'day_of_week', 'hour_of_day', 'lagged_parking_available', 'time_slot', 'lagged_day_interaction', 'trans_amt_binned']]
y = filtered_df['parking_available']

# Convert 'pole_id' to numerical representation
X.loc[:, 'pole_id'] = X['pole_id'].astype('category').cat.codes

# Data splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=filtered_df['pole_id'])

# Impute missing values
imputer = SimpleImputer(strategy='most_frequent')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Model training
logreg_model = LogisticRegression(max_iter=1000, solver='liblinear')
logreg_model.fit(X_train_imputed, y_train)

# Function to predict parking availability
def predict_parking_availability(pole_id, day_of_week, hour_of_day):
  # Create input data
  input_data = pd.DataFrame([[pole_id, day_of_week, hour_of_day, 0, str(day_of_week) + '_' + str(hour_of_day), 0, 0]], 
                            columns=['pole_id', 'day_of_week', 'hour_of_day', 'lagged_parking_available', 'time_slot', 'lagged_day_interaction', 'trans_amt_binned'])
  
  # Convert 'pole_id' to numerical representation
  input_data.loc[:, 'pole_id'] = input_data['pole_id'].astype('category').cat.codes
  
  # Impute missing values (if any)
  input_data_imputed = imputer.transform(input_data)

  # Make prediction
  probability = logreg_model.predict_proba(input_data_imputed)[0][1]
  
  return probability * 100
  
# Predict parking availability for pole_id 'P510', on Tuesday (day_of_week=1) at 10 AM (hour_of_day=10)
availability_percentage = predict_parking_availability('P510', 1, 10) 
print(f"Parking availability percentage: {availability_percentage:.2f}%")