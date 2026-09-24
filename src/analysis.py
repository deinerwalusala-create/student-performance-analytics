def calculate_average_scores(df):

    df["Average_Score"] = (
        df["Assignments"]
        + df["Midterm"]
        + df["Final"]
    ) / 3

    return df


def classify_students(df):

    def classify(score):

        if score >= 80:
            return "Excellent"

        elif score >= 70:
            return "Good"

        elif score >= 60:
            return "Average"

        else:
            return "Needs Improvement"

    df["Performance_Level"] = df["Average_Score"].apply(classify)

    return df


def department_analysis(df):

    return (
        df.groupby("Department")["Average_Score"]
        .mean()
        .sort_values(ascending=False)
    )


def gender_analysis(df):

    return (
        df.groupby("Gender")["Average_Score"]
        .mean()
        .sort_values(ascending=False)
    )


def attendance_analysis(df):

    return df["Attendance"].corr(df["Average_Score"])


def study_hours_analysis(df):

    return df["Study_Hours"].corr(df["Average_Score"])


def top_students(df, number=5):

    return (
        df.sort_values(
            by="Average_Score",
            ascending=False
        )
        .head(number)
    )


def lowest_students(df, number=5):

    return (
        df.sort_values(
            by="Average_Score",
            ascending=True
        )
        .head(number)
    )


def performance_summary(df):

    return df["Performance_Level"].value_counts()


def average_subject_scores(df):

    return {
        "Assignments": df["Assignments"].mean(),
        "Midterm": df["Midterm"].mean(),
        "Final": df["Final"].mean()
    }


def score_range(df):

    highest = df["Average_Score"].max()
    lowest = df["Average_Score"].min()

    return highest, lowest, highest - lowest


def department_statistics(df):

    return department_analysis(df)


def gender_statistics(df):

    return gender_analysis(df)