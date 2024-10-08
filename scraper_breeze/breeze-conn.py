from datetime import datetime
from breeze_connect import BreezeConnect
import time
import os
from datetime import datetime
import Breezy
from breeze_login import get_session_key


# from BreezeHistoricalOptions import autologin, Breezy
unix_start = time.time()

###################################################################
###################### LOGIN STUFF ################################
    
breeze = BreezeConnect(api_key=os.environ["API_KEY"])
print(breeze)

try:
    session_key = get_session_key(force=False)
except Exception as e:
    print(e)
    pass
    # session_key = get_session_key(force=True)

breeze.generate_session(api_secret=os.environ["API_SECRET"],
                    session_token=session_key)
expiry_date = "06-Dec-2023" # 'expiries.json' contains a list of expiry dates in this format
start_datetime = "06-Dec-2023 9:15:00" 
end_datetime = "06-Dec-2023 15:29:59" 
start_strike =  47000
end_strike = 47200

Breezy.fetch_data(
                api = breeze,
                scrip = "CNXBAN",  # 'NIFTY' for Nifty 50 | 'CNXBAN' for Bank Nifty | 'NIFFIN' for Finnifty | 'NIFMID' for Midcap Nifty
                exch = "NFO",
                expiry_date = datetime.strptime(expiry_date, "%d-%b-%Y"),
                start_datetime = datetime.strptime(start_datetime, "%d-%b-%Y %H:%M:%S"),
                end_datetime = datetime.strptime(end_datetime, "%d-%b-%Y %H:%M:%S"),
                start_strike = start_strike,
                end_strike = end_strike,
                step = 100,
                max_threads = 3, #Set this to 1 if you are getting api breeze_historical_v2() error
                export_path = 'HistoricData/' #will auto-create path if it doesn't exist
                )

unix_end = time.time()
print(f"Time elapsed: {unix_end - unix_start} seconds")