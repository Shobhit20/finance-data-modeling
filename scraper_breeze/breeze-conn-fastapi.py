from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os
import time
from breeze_connect import BreezeConnect
from breeze_login import get_session_key
import Breezy

app = FastAPI()

# Model for request body (optional)
class FetchDataRequest(BaseModel):
    expiry_date: Optional[str] = "06-Dec-2023"  # Default values
    start_datetime: Optional[str] = "06-Dec-2023 9:15:00"
    end_datetime: Optional[str] = "06-Dec-2023 15:29:59"
    start_strike: Optional[int] = 47000
    end_strike: Optional[int] = 47200
    step: Optional[int] = 100
    ticker_symbol: Optional[str] = "CNXBAN"
    exchange: Optional[str] = "NFO"



# Helper function to initialize BreezeConnect
def initialize_breeze():
    try:
        breeze = BreezeConnect(api_key=os.environ["API_KEY"])
        session_key = get_session_key(force=False)
        breeze.generate_session(api_secret=os.environ["API_SECRET"], session_token=session_key)
        return breeze
    except Exception as e:
        print(e)


@app.post("/fetch_data")
def fetch_data(request: FetchDataRequest):
    unix_start = time.time()
    
    try:
        # Initialize BreezeConnect with environment credentials
        breeze = initialize_breeze()

        # Parse datetime and other inputs
        expiry_date = datetime.strptime(request.expiry_date, "%d-%b-%Y")
        start_datetime = datetime.strptime(request.start_datetime, "%d-%b-%Y %H:%M:%S")
        end_datetime = datetime.strptime(request.end_datetime, "%d-%b-%Y %H:%M:%S")
        
        # Call Breezy's fetch_data function
        Breezy.fetch_data(
            api=breeze,
            scrip=request.ticker_symbol,
            exch=request.exchange,
            expiry_date=expiry_date,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            start_strike=request.start_strike,
            end_strike=request.end_strike,
            step=request.step,
            max_threads=3,
            export_path='HistoricData/'  # Adjust if needed
        )
        
        unix_end = time.time()
        return {"message": "Data fetch complete", "time_elapsed": unix_end - unix_start}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

# Example endpoint for testing server
@app.get("/")
def root():
    return {"message": "BreezeConnect FastAPI is up and running!"}