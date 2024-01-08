import logging
from io import BytesIO
from fastapi import APIRouter, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from flaml import AutoML
from sklearn.model_selection import train_test_split
from evidently.report import Report
from evidently.metric_preset import RegressionPreset, ClassificationPreset
from bs4 import BeautifulSoup
import pandas as pd

router = APIRouter()
logging.basicConfig(level=logging.INFO)


@router.post("/automl")
async def automl(file: UploadFile = File(...), task: str = Form(...), target: str = Form(...)):
    try:
        # Read the csv file
        file_contents = file.file.read()
        df = pd.read_csv(BytesIO(file_contents))

        df = df.dropna()

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

        preset = RegressionPreset() if task == 'regression' else ClassificationPreset()
        report = Report(metrics=[preset])
        report.run(reference_data=x_train, current_data=x_test)
        html = report.get_html()

        soup = BeautifulSoup(html, 'html.parser')
        iframe = soup.prettify()
        print('here')

        return {"iframe": iframe}

    except Exception as e:
        logging.error(f"An error occurred during AutoML process: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)
