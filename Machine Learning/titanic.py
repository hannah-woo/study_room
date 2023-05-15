import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

titanic_df = sns.load_dataset('titanic')
titanic_df.head()
titanic_df.info()

titanic_df['age'].fillna(titanic_df['age'].mean(), inplace = True)
titanic_df['embarked'].fillna('N', inplace=True)
titanic_df['embark_town'].fillna('N', inplace=True)
titanic_df['deck'] = titanic_df['deck'].astype('object')
titanic_df['deck'].fillna('N', inplace=True)

titanic_df['class'] = titanic_df['class'].astype('object')
titanic_df.isnull().sum().sum()

col_list = ['sex', 'embarked', 'who', 'embark_town', 'alive']
for col in col_list:
    print(titanic_df[col].value_counts())
    print('________________________')

sns.barplot(x='sex', y='survived', data=titanic_df)
sns.barplot(x='pclass', y='survived', hue='sex', data=titanic_df)
sns.barplot(x='class', y='survived', hue='sex', data=titanic_df)

def get_category(age):
    cat = ''
    if age <= -1:
        cat = 'unknown'
    elif age <= 5:
        cat = 'baby'
    elif age <= 12:
        cat = 'child'
    elif age <= 18:
        cat = 'teenage'
    elif age <= 25:
        cat = 'student'
    elif age <= 35:
        cat = 'young adult'
    elif age <= 60:
        cat = 'adult'
    else:
        cat = 'elderly'

    return cat

plt.figure(figsize=(10,6))
group_names = ['unknown', 'baby', 'child', 'teenage', 'student', 'young adult', 'adult', 'elderly']
titanic_df['age_cat'] = titanic_df['age'].apply(lambda x: get_category(x))
sns.barplot(x = 'age_cat', y = 'survived', hue = 'sex', data = titanic_df, order = group_names)

from sklearn.preprocessing import LabelEncoder

def encode_features(data_df):
    features = ['sex', 'embarked', 'deck', 'embark_town',  'alive', 'alone']
    for feature in features:
        le = LabelEncoder()
        le = le.fit(data_df[feature])
        data_df[feature] = le.transform(data_df[feature])
    return data_df

titanic_df = encode_features(titanic_df)
titanic_df.head()



"""정리"""

# null 처리 함수
def fillna(data_df):
    data_df['age'].fillna(data_df['age'].mean(), inplace=True)
    data_df['deck'] = data_df['deck'].astype('object')
    data_df['deck'].fillna('N', inplace=True)
    data_df['embarked'].fillna('N', inplace=True)
    data_df['fare'].fillna(0, inplace=True)
    return data_df

# 머신러닝 알고리즘에 불필요한 피처 제거
def drop_features(data_df):
    data_df.drop(['who', 'adult_male', 'embark_town', 'alive', 'alone'], axis=1, inplace=True)
    return data_df

# 레이블 인코딩 수행
def format_features(data_df):
    features = ['sex', 'embarked', 'deck', 'class']
    from sklearn.preprocessing import LabelEncoder
    encoder = LabelEncoder()
    for feature in features:
        encoder = encoder.fit(data_df[feature])
        data_df[feature] = encoder.transform(data_df[feature])
    return data_df

# 앞에서 설정한 데이터 전처리 함수 호출
def transform_features(data_df):
    data_df = fillna(data_df)
    data_df = drop_features(data_df)
    data_df = format_features(data_df)
    return data_df

# 함수 호출
titanic_df = sns.load_dataset('titanic')
titanic_df.head(2)

target_df = titanic_df[['survived']]
titanic_df.drop(['survived'], axis=1, inplace=True)

titanic_df = transform_features(titanic_df)
titanic_df.head(2)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(titanic_df, target_df, test_size=0.2, random_state=0)

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

dt_clf = DecisionTreeClassifier(random_state=0)
rf_clf = RandomForestClassifier(random_state=0)
lr_clf = LogisticRegression(solver='liblinear')

import warnings
warnings.filterwarnings('ignore')
models = [dt_clf, rf_clf, lr_clf]
for model in models:
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    class_name = model.__class__.__name__
    print('{0} 모델의 성능은 {1:.4f} 입니다.'.format(class_name, accuracy))