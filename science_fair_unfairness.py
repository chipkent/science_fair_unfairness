
# from tabula import read_pdf
import pandas
import numpy as np

def load_session(session):
    """Load data for a session."""
    file = f"data/{session.lower()}.csv"
    df = pandas.read_csv(file, sep="|", na_values=["-", chr(8722)])

    # there appear to be some spurious zero values
    for c in df.columns:
        if c != "Judge":
            df[c].replace(0, np.NaN)

    return df

def load_sessions(sessions):
    """Load data for multiple sessions."""
    return {s:load_session(s) for s in sessions}

def analyze_session(session, df):
    print("--------------------------------------------------------")
    print(f"Session: {session}")
    print("--------------------------------------------------------")
    print(df)
    print(df.dtypes)


sessions = ["JA", "JB", "JC", "JD", "SA", "SC", "SD"]
data = load_sessions(sessions)

for session, df in data.items():
    analyze_session(session, df)
