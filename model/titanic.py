from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import seaborn as sns

class TitanicModel:
    _instance = None  # Singleton instance

    def __init__(self):
        # Load and clean dataset
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.model = LogisticRegression(max_iter=1000)
        self.tree = DecisionTreeClassifier()
        self.features = [
            'pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'alone',
            'embarked_C', 'embarked_Q', 'embarked_S'
        ]
        self._prepare_data()

    def _prepare_data(self):
        df = sns.load_dataset('titanic')
        df = df.drop(columns=[
            'deck', 'embark_town', 'alive', 'who',
            'adult_male', 'class'
        ])
        df.dropna(inplace=True)

        df['sex'] = df['sex'].map({'male': 1, 'female': 0})
        df['alone'] = df['alone'].astype(int)

        # Encode embarked
        embarked_encoded = self.encoder.fit_transform(df[['embarked']]).toarray()
        embarked_cols = ['embarked_' + cat for cat in self.encoder.categories_[0]]
        df[embarked_cols] = pd.DataFrame(embarked_encoded, index=df.index)

        df.drop(columns=['embarked'], inplace=True)

        # Train models
        X = df[self.features]
        y = df['survived']

        self.model.fit(X, y)
        self.tree.fit(X, y)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TitanicModel()
        return cls._instance

    def predict(self, passenger_dict):
        df = pd.DataFrame(passenger_dict, index=[0])
        df['sex'] = df['sex'].map({'male': 1, 'female': 0})
        df['alone'] = df['alone'].astype(int)

        embarked_encoded = self.encoder.transform(df[['embarked']]).toarray()
        embarked_cols = ['embarked_' + cat for cat in self.encoder.categories_[0]]
        df[embarked_cols] = pd.DataFrame(embarked_encoded, index=df.index)

        df.drop(columns=['name', 'embarked'], inplace=True)

        probs = self.model.predict_proba(df)[0]
        return {
            'die': float(probs[0]),
            'survive': float(probs[1])
        }

    def feature_importance(self):
        return {
            feat: imp for feat, imp in zip(self.features, self.tree.feature_importances_)
        }
