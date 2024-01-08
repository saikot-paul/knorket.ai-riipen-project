from flaml import AutoML
from sklearn.model_selection import train_test_split
from evidently.report import Report
from evidently.metric_preset import RegressionPreset, ClassificationPreset
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_csv('./data.csv')
df = df.dropna()

task = 'regression'
target = 'imdb_score'

print(df.head(10))
print(task)
print(target)

x = df.drop(target, axis=1)
y = df[target]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2)

print(df.head(10))
print(task)
print(target)

x = df.drop(target, axis=1)
y = df[target]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2)

model = AutoML()
metric = "accuracy" if task == "classification" else "r2"

settings = {
    "time_budget": 15,
    "metric": metric,
    "task": task,
    'log_file_name': 'flaml.log'
}

print("Params done set up ")
model.fit(x_train, y_train, **settings)
print("Fitted ")

x_train['prediction'] = model.predict(x_train)
x_train['target'] = y_train

x_test['prediction'] = model.predict(x_test)
x_test['target'] = y_test
print('Done predicting')

print('train')
print(x_train.columns)

print('test')
print(x_test.columns)

preset = RegressionPreset() if task == 'regression' else ClassificationPreset()
report = Report(metrics=[preset])
report.run(reference_data=x_train, current_data=x_test)
html = report.get_html()
print('here')

soup = BeautifulSoup(html, 'html.parser')
iframe = soup.prettify()
