
from typing import List, Dict
import pandas
import numpy as np
import scipy.stats
import math

def load_session(session) -> pandas.DataFrame:
    """Load data for a session."""
    file = f"data/{session.lower()}.csv"
    df = pandas.read_csv(file, sep="|", na_values=["-", chr(8722)])

    # there appear to be some spurious zero values
    for c in df.columns:
        if c != "Judge":
            df[c].replace(0, np.NaN)

    return df

def load_sessions(sessions:List[str]) -> Dict[str,pandas.DataFrame]:
    """Load data for multiple sessions."""
    return {s:load_session(s) for s in sessions}

def compute_means(df:pandas.DataFrame) -> pandas.DataFrame:
    """Compute mean scores and errors."""
    projects = []
    means = []
    std_errs = []

    for c in df.columns:
        if c == "Judge":
            continue

        x = df[c]
        x = x[~np.isnan(x)]
        x = np.sort(x)
        x_drop_high_low = x[1:-1]

        m = np.mean(x_drop_high_low)
        s = scipy.stats.sem(x_drop_high_low)

        projects.append(c)
        means.append(m)
        std_errs.append(s)

    df = pandas.DataFrame({"Project":projects, "Mean":means, "StdErr":std_errs})
    df = df.sort_values(by=['Mean'], ascending=False)
    return df

def analyze_pair_wise_means(means:pandas.DataFrame) -> pandas.DataFrame:
    """Compare the mean estimates in a pairwise way to determine the odds that one project should win over another."""
    project1 = []
    project2 = []
    mean1 = []
    stderr1 = []
    mean2 = []
    stderr2 = []
    mean_diff = []
    ste_diff = []
    z_diff = []
    p_diff = []

    for i in range(len(means)):
        p1 = means["Project"][i]
        m1 = means["Mean"][i]
        s1 = means["StdErr"][i]

        for j in range(i,len(means)):
            p2 = means["Project"][j]
            m2 = means["Mean"][j]
            s2 = means["StdErr"][j]

            if p1 == p2:
                continue

            d = m1-m2
            s = math.sqrt(s1*s1 + s2*s2)
            z = d/s
            p = scipy.stats.norm.sf(-z)

            project1.append(p1)
            project2.append(p2)
            mean1.append(m1)
            stderr1.append(s1)
            mean2.append(m2)
            stderr2.append(s2)
            mean_diff.append(d)
            ste_diff.append(s)
            z_diff.append(z)
            p_diff.append(p)

    return pandas.DataFrame({
        "Project1":project1, 
        "Project2":project2, 
        "Mean1":mean1, 
        "StdErr1":stderr1, 
        "Mean2":mean2,
        "StdErr2":stderr2,
        "MeanDiff":mean_diff,
        "StdErrDiff":ste_diff,
        "ZDiff":z_diff,
        "P1Wins":p_diff,
        })

def analyze_same_judge(df:pandas.DataFrame) -> pandas.DataFrame:
    """Analyze judges that scored pairs of projects to see who they pick as winners."""
    project1 = []
    project2 = []
    n_judges = []
    mean_diff = []
    ste_diff = []
    z_diff = []
    p_diff = []

    df = df.drop(columns=["Judge"])

    for c1 in df.columns:
        for c2 in df.columns:
            if c1 == c2: continue

            dfs = df[[c1,c2]].dropna()
            x1 = dfs.loc[:, c1].to_numpy()
            x2 = dfs.loc[:, c2].to_numpy()
            diffs = x1 - x2
            m = np.mean(diffs)

            if len(diffs) <= 1:
                s = np.nan
                z = np.nan
                p = np.nan
            else:
                s = scipy.stats.sem(diffs)

                if s == 0: 
                    z = np.nan
                    p = np.nan
                else:
                    z = m/s
                    p = scipy.stats.norm.sf(-z)

            # print(f"{c1} {c2} {diffs} {m} {s} {z} {p}")

            project1.append(c1)
            project2.append(c2)
            n_judges.append(len(diffs))
            mean_diff.append(m)
            ste_diff.append(s)
            z_diff.append(z)
            p_diff.append(p)


    df = pandas.DataFrame({
        "Project1":project1, 
        "Project2":project2, 
        "NJudges": n_judges,
        "MeanDiff":mean_diff, 
        "StdErrDiff":ste_diff, 
        "ZDiff":z_diff,
        "P1Wins":p_diff,
        })

    df = df.sort_values(by=['MeanDiff'], ascending=False)
    df = df[df['MeanDiff'] > 0]
    return df


def analyze_session(session:str, df:pandas.DataFrame) -> None:
    """Analyze a science fair session."""
    print("\n\n")
    print("--------------------------------------------------------")
    print(f"Session: {session}")
    print("--------------------------------------------------------")
    print("\nData:")
    print(df.to_string(index=False))

    print("\nMeans:")
    means = compute_means(df)
    print(means.to_string(index=False))

    print("\nPair-Wise Winners:")
    pair_wise = analyze_pair_wise_means(means)
    print(pair_wise.to_string(index=False))

    print("\nSame Judge Winners:")
    same_judge = analyze_same_judge(df)
    print(same_judge.to_string(index=False))

def header() -> str:
    print("\n\n")
    print("--------------------------------------------------------")
    print(f"Data Description")
    print("--------------------------------------------------------")
    print("Data - Raw judging data")
    print("Means - Mean scores and standard errors per project")
    print("Pair-Wise Winners - Predict odds of a project winning based on the means and standard errors of scores")
    print("Same-Judge Winners - Predict odds of a project winning based on judges that scored both projects.")

sessions = ["JA", "JB", "JC", "JD", "SA", "SC", "SD"]
data = load_sessions(sessions)

header()

for session, df in data.items():
    analyze_session(session, df)
