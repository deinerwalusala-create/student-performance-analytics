# --------------------------------
# AUTOMATED INSIGHTS
# --------------------------------


# --------------------------------
# OVERALL PERFORMANCE INSIGHT
# --------------------------------

def overall_performance_insight(df):

    average_score = df["Average_Score"].mean()

    if average_score >= 80:

        return (
            f"The overall average student score is "
            f"{average_score:.2f}, indicating strong "
            f"academic performance."
        )

    elif average_score >= 60:

        return (
            f"The overall average student score is "
            f"{average_score:.2f}, indicating moderate "
            f"academic performance."
        )

    else:

        return (
            f"The overall average student score is "
            f"{average_score:.2f}, indicating that "
            f"academic performance requires attention."
        )


# --------------------------------
# STUDY HOURS INSIGHT
# --------------------------------

def study_hours_insight(df):

    correlation = df["Study_Hours"].corr(
        df["Average_Score"]
    )

    if correlation >= 0.7:

        strength = "strong positive"

    elif correlation >= 0.4:

        strength = "moderate positive"

    elif correlation >= 0:

        strength = "weak positive"

    elif correlation <= -0.4:

        strength = "negative"

    else:

        strength = "weak or very weak"

    return (
        f"Study hours have a {strength} relationship "
        f"with average score (correlation = "
        f"{correlation:.2f})."
    )


# --------------------------------
# ATTENDANCE INSIGHT
# --------------------------------

def attendance_insight(df):

    correlation = df["Attendance"].corr(
        df["Average_Score"]
    )

    if correlation >= 0.7:

        strength = "strong positive"

    elif correlation >= 0.4:

        strength = "moderate positive"

    elif correlation >= 0:

        strength = "weak positive"

    else:

        strength = "negative"

    return (
        f"Attendance has a {strength} relationship "
        f"with average score (correlation = "
        f"{correlation:.2f})."
    )


# --------------------------------
# TOP DEPARTMENT INSIGHT
# --------------------------------

def department_insight(df):

    department_scores = (
        df.groupby("Department")["Average_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    top_department = department_scores.index[0]

    top_score = department_scores.iloc[0]

    return (
        f"{top_department} has the highest average "
        f"score in the dataset at {top_score:.2f}."
    )


# --------------------------------
# TOP STUDENT INSIGHT
# --------------------------------

def top_student_insight(df):

    top_student = df.loc[
        df["Average_Score"].idxmax()
    ]

    return (
        f"The highest-performing student is "
        f"{top_student['Name']} with an average "
        f"score of {top_student['Average_Score']:.2f}."
    )


# --------------------------------
# AT-RISK INSIGHT
# --------------------------------

def at_risk_insight(df):

    total_students = len(df)

    at_risk_students = len(
        df[
            df["Risk_Level"].isin(
                ["High Risk", "Medium Risk"]
            )
        ]
    )

    percentage = (
        at_risk_students /
        total_students
    ) * 100

    return (
        f"{at_risk_students} out of "
        f"{total_students} students "
        f"({percentage:.1f}%) are classified "
        f"as medium or high risk."
    )


# --------------------------------
# PERFORMANCE DISTRIBUTION INSIGHT
# --------------------------------

def performance_distribution_insight(df):

    distribution = (
        df["Performance_Level"]
        .value_counts()
    )

    most_common = distribution.idxmax()

    number = distribution.max()

    return (
        f"The most common performance category "
        f"is '{most_common}', containing "
        f"{number} students."
    )


# --------------------------------
# GENERATE ALL INSIGHTS
# --------------------------------

def generate_insights(df):

    insights = [

        overall_performance_insight(df),

        study_hours_insight(df),

        attendance_insight(df),

        department_insight(df),

        top_student_insight(df),

        at_risk_insight(df),

        performance_distribution_insight(df)

    ]

    return insights