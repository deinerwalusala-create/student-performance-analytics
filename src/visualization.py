import matplotlib.pyplot as plt
import seaborn as sns


def score_distribution(df):

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
    plt.show()


def department_performance(df):

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
    plt.show()


def attendance_vs_score(df):

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
    plt.show()


def performance_levels(df):

    plt.figure(figsize=(9, 6))

    sns.countplot(
        data=df,
        x="Performance_Level"
    )

    plt.title("Students by Performance Level")
    plt.xlabel("Performance Level")
    plt.ylabel("Number of Students")

    plt.tight_layout()
    plt.show()