"""
Module that downloads a file and then returns profiling iframe
"""
from io import BytesIO
from fastapi import APIRouter, UploadFile
from ydata_profiling import ProfileReport
from bs4 import BeautifulSoup
import pandas as pd

router = APIRouter()


@router.post("/profile")
async def generate_profile(file: UploadFile):

    """
    API downloads the file from HTTP request then uses ydata for profiling, 
    removes the samples and footers and returns an iframe
    """

    # Read the file content
    file_contents = file.file.read()

    # Read the csv file
    df = pd.read_csv(BytesIO(file_contents))

    # Generate the report
    report = ProfileReport(df, samples=None)
    report_html = report.to_html()

    # Remove the footer
    soup = BeautifulSoup(report_html, 'html.parser')
    footer = soup.find('footer')
    if footer:
        footer.decompose()

    # Create iframe
    iframe = soup.prettify()

    # Return the iframe
    return {"iframe": iframe}
