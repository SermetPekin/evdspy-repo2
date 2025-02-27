
from evdspy import get_series, default_start_date_fnc, default_end_date_fnc
import pandas as pd  
def get_api_key():
    import os
    return os.getenv("EVDS_API_KEY")

assert isinstance(get_api_key(), str) and len(get_api_key()) == 10

def t1():
    df = get_series("TP.ODEMGZS.BDTTOPLAM",
                    frequency="monthly",
                    start_date=default_start_date_fnc(),
                    end_date=default_end_date_fnc(),
                    aggregation=("avg",),
                    cache=False,
                    debug=False,
                    api_key=get_api_key())
    print(df)
    assert isinstance(df, pd.DataFrame)
if __name__ == "__main__":
    t1()