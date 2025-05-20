# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LogisticRegression
# from sklearn.impute import SimpleImputer
# from sklearn.model_selection import train_test_split

# class ParkingAvailabilityModel:
#     def __init__(self):
#         df = pd.read_csv('datasets/treas_parking_payments_2025_datasd.csv')

#         df['date_trans_start'] = pd.to_datetime(df['date_trans_start'], errors='coerce')
#         df['day_of_week'] = df['date_trans_start'].dt.dayofweek
#         df['hour_of_day'] = df['date_trans_start'].dt.hour
#         df['parking_available'] = 1
#         df['lagged_parking_available'] = df.groupby('pole_id')['parking_available'].shift(1).fillna(0)
#         df['time_slot'] = df['day_of_week'].astype(str) + '_' + df['hour_of_day'].astype(str)
#         df['lagged_day_interaction'] = df['lagged_parking_available'] * df['day_of_week']
#         df['trans_amt_binned'] = pd.cut(df['trans_amt'], bins=[0, 5, 10, 20, 50, 100, float('inf')], labels=False)
#         df = df.drop(['date_trans_start', 'date_meter_expire'], axis=1)

#         pole_id_counts = df['pole_id'].value_counts()
#         filtered_df = df[~df['pole_id'].isin(pole_id_counts[pole_id_counts == 1].index)]
#         filtered_df.loc[:, 'parking_available'] = np.where((filtered_df['hour_of_day'] >= 7) & (filtered_df['hour_of_day'] <= 19), 1, 0)

#         X = filtered_df[['pole_id', 'day_of_week', 'hour_of_day', 'lagged_parking_available',
#                          'time_slot', 'lagged_day_interaction', 'trans_amt_binned']]
#         y = filtered_df['parking_available']

#         X.loc[:, 'pole_id'] = X['pole_id'].astype('category').cat.codes

#         self.imputer = SimpleImputer(strategy='most_frequent')
#         X_train_imputed = self.imputer.fit_transform(X)

#         self.model = LogisticRegression(max_iter=1000, solver='liblinear')
#         self.model.fit(X_train_imputed, y)

#     def predict(self, pole_id, day_of_week, hour_of_day):
#         input_data = pd.DataFrame([[pole_id, day_of_week, hour_of_day, 0, f"{day_of_week}_{hour_of_day}", 0, 0]],
#                                   columns=['pole_id', 'day_of_week', 'hour_of_day',
#                                            'lagged_parking_available', 'time_slot',
#                                            'lagged_day_interaction', 'trans_amt_binned'])
#         input_data.loc[:, 'pole_id'] = input_data['pole_id'].astype('category').cat.codes
#         input_data_imputed = self.imputer.transform(input_data)
#         prob = self.model.predict_proba(input_data_imputed)[0][1]
#         return round(prob * 100, 2)
