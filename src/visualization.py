import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def _finish_plot(output_path, show):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()



# --------------------------------
# SCORE DISTRIBUTION
# --------------------------------

def score_distribution(df, output_path="outputs/charts/score_distribution.png", show=True):

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["Average_Score"],
        bins=8,
        kde=True
    )

    plt.title(
        "Distribution of Student Average Scores"
    )

    plt.xlabel(
        "Average Score"
    )

    plt.ylabel(
        "Number of Students"
    )

    plt.tight_layout()

    _finish_plot(output_path, show)


# --------------------------------
# DEPARTMENT PERFORMANCE
# --------------------------------

def department_performance(df, output_path="outputs/charts/department_performance.png", show=True):

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df,
        x="Department",
        y="Average_Score"
    )

    plt.title(
        "Average Performance by Department"
    )

    plt.xlabel(
        "Department"
    )

    plt.ylabel(
        "Average Score"
    )

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    _finish_plot(output_path, show)


# --------------------------------
# ATTENDANCE VS PERFORMANCE
# --------------------------------

def attendance_vs_score(df, output_path="outputs/charts/attendance_vs_score.png", show=True):

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="Attendance",
        y="Average_Score",
        hue="Performance_Level",
        s=100
    )

    plt.title(
        "Attendance vs Student Performance"
    )

    plt.xlabel(
        "Attendance (%)"
    )

    plt.ylabel(
        "Average Score"
    )

    plt.tight_layout()

    _finish_plot(output_path, show)


# --------------------------------
# PERFORMANCE LEVELS
# --------------------------------

def performance_levels(df, output_path="outputs/charts/performance_levels.png", show=True):

    plt.figure(figsize=(9, 6))

    sns.countplot(
        data=df,
        x="Performance_Level"
    )

    plt.title(
        "Students by Performance Level"
    )

    plt.xlabel(
        "Performance Level"
    )

    plt.ylabel(
        "Number of Students"
    )

    plt.tight_layout()

    _finish_plot(output_path, show)


# --------------------------------
# RISK LEVEL
# --------------------------------

def risk_level_chart(df, output_path="outputs/charts/risk_levels.png", show=True):

    risk_counts = df[
        "Risk_Level"
    ].value_counts()

    plt.figure(figsize=(9, 6))

    risk_counts.plot(
        kind="bar"
    )

    plt.title(
        "Students by Risk Level"
    )

    plt.xlabel(
        "Risk Level"
    )

    plt.ylabel(
        "Number of Students"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    _finish_plot(output_path, show)


# --------------------------------
# RISK REASONS
# --------------------------------

def risk_reason_chart(df):

    at_risk = df[
        df["Risk_Reason"] != "No Major Risk"
    ]

    reason_counts = {}

    for reason_list in at_risk["Risk_Reason"]:

        reasons = reason_list.split(", ")

        for reason in reasons:

            if reason in reason_counts:

                reason_counts[reason] += 1

            else:

                reason_counts[reason] = 1

    plt.figure(figsize=(10, 6))

    plt.bar(
        reason_counts.keys(),
        reason_counts.values()
    )

    plt.title(
        "Reasons Students Are At Risk"
    )

    plt.xlabel(
        "Risk Reason"
    )

    plt.ylabel(
        "Number of Students"
    )

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/charts/risk_reasons.png"
    )

    plt.show()

    plt.close()


# --------------------------------
# STUDY HOURS VS PERFORMANCE
# --------------------------------

def study_hours_vs_risk(df):

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="Study_Hours",
        y="Average_Score",
        hue="Risk_Level",
        s=100
    )

    plt.title(
        "Study Hours vs Average Score"
    )

    plt.xlabel(
        "Study Hours"
    )

    plt.ylabel(
        "Average Score"
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/charts/study_hours_vs_score.png"
    )

    plt.show()

    plt.close()


# --------------------------------
# CORRELATION HEATMAP
# --------------------------------

def correlation_heatmap(df, output_path="outputs/charts/correlation_heatmap.png", show=True):

    columns = [
        "Study_Hours",
        "Attendance",
        "Assignments",
        "Midterm",
        "Final",
        "Average_Score"
    ]

    correlation = df[
        columns
    ].corr()

    plt.figure(figsize=(10, 7))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm"
    )

    plt.title(
        "Correlation Between Student Performance Variables"
    )

    plt.tight_layout()
    _finish_plot(output_path, show)

    plt.close()