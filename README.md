# science_fair_unfairness
Statistical analysis of unfairness in science fair judging.

Science fairs typically have a two stage assessment process. In the first stage, many judges review projects and produce numerical scores for each project.  Efforts are made to ensure that these numerical results are fair and unbiased.  In the second stage, a small committee chooses the winners of the contest.  This committee is not required to follow the results from the first stage.

This scenario is like a diving competition where the scores are thrown out at the end of the competition, allowing 1 to 3 judges to pick their favorite diver.  This is far from a statistically optimal process and is **highly biased**.

This project analyzes the judging scores from the first stage to determine the odds that one project should beat another -- in an unbiased way.  This allows the statistical results to be compared to the results from the second stage, in order to identify bias and unfairness in the second stage.

# Install

```bash
pip3 install -r requirements.txt
```

# Run

```bash
python3 ./science_fair_unfairness.py > results.txt
```
