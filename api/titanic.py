# model.py
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import seaborn as sns

class TitanicModel:
    _instance = None

    def __init__(self):
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.model = LogisticRegression(max_iter=1000)
        self.decision_tree = DecisionTreeClassifier()
        self.features = [
            'pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'alone',
            'embarked_C', 'embarked_Q', 'embarked_S'
        ]
        self._load_and_train()

    def _load_and_train(self):
        df = sns.load_dataset('titanic')
        df = df.drop(['deck', 'embark_town', 'alive', 'who', 'adult_male', 'class'], axis=1)
        df.dropna(inplace=True)
        df['sex'] = df['sex'].apply(lambda x: 1 if x == 'male' else 0)
        df['alone'] = df['alone'].apply(lambda x: 1 if x is True else 0)

        onehot = self.encoder.fit_transform(df[['embarked']]).toarray()
        cols = ['embarked_' + val for val in self.encoder.categories_[0]]
        df[cols] = pd.DataFrame(onehot, index=df.index)
        df.drop(['embarked'], axis=1, inplace=True)

        X = df[self.features]
        y = df['survived']

        self.model.fit(X, y)
        self.decision_tree.fit(X, y)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TitanicModel()
        return cls._instance

    def predict(self, passenger_dict):
        df = pd.DataFrame(passenger_dict, index=[0])
        df['sex'] = df['sex'].apply(lambda x: 1 if x == 'male' else 0)
        df['alone'] = df['alone'].apply(lambda x: 1 if x is True else 0)

        embarked = self.encoder.transform(df[['embarked']]).toarray()
        cols = ['embarked_' + val for val in self.encoder.categories_[0]]
        df[cols] = pd.DataFrame(embarked, index=df.index)
        df.drop(['name', 'embarked'], axis=1, inplace=True)

        probabilities = self.model.predict_proba(df)[0]
        return {'die': probabilities[0], 'survive': probabilities[1]}