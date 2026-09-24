import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def _finish_plot(output_path=None, show=True):
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=180, bbox_inches="tight")

    if show:
        plt.show()

    plt.close()


def score_distribution(df, output_path=None, show=True):

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["Average_Score"],
        bins=8,
        kde=True
    )

    plt.title("Distribution of Student Average Scores")
    plt.xlabel("Average Score")
    plt.ylabel("Number of Students")

    plt.tight_layout()
    _finish_plot(output_path, show)


def department_performance(df, output_path=None, show=True):

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df,
        x="Department",
        y="Average_Score"
    )

    plt.title("Average Performance by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Score")

    plt.xticks(rotation=15)

    plt.tight_layout()
    _finish_plot(output_path, show)


def attendance_vs_score(df, output_path=None, show=True):

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="Attendance",
        y="Average_Score",
        hue="Performance_Level",
        s=100
    )

    plt.title("Attendance vs Student Performance")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Average Score")

    plt.tight_layout()
    _finish_plot(output_path, show)


def performance_levels(df, output_path=None, show=True):

    plt.figure(figsize=(9, 6))

    sns.countplot(
        data=df,
        x="Performance_Level"
    )

    plt.title("Students by Performance Level")
    plt.xlabel("Performance Level")
    plt.ylabel("Number of Students")

    plt.tight_layout()
    _finish_plot(output_path, show)


def risk_level_chart(df, output_path=None, show=True):

    risk_counts = df["Risk_Level"].value_counts()

    plt.figure(figsize=(9, 6))

    risk_counts.plot(
        kind="bar"
    )

    plt.title("Students by Risk Level")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Students")

    plt.xticks(rotation=0)

    plt.tight_layout()
    _finish_plot(output_path, show)