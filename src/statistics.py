# --------------------------------
# AT-RISK STUDENT DETECTION
# --------------------------------

def detect_at_risk_students(df):

    at_risk = df[
        (df["Average_Score"] < 60) |
        (df["Attendance"] < 75) |
        (df["Study_Hours"] < 8)
    ].copy()

    return at_risk


# --------------------------------
# AT-RISK REASON
# --------------------------------

def identify_risk_reason(row):

    reasons = []

    if row["Average_Score"] < 60:
        reasons.append("Low Academic Score")

    if row["Attendance"] < 75:
        reasons.append("Low Attendance")

    if row["Study_Hours"] < 8:
        reasons.append("Low Study Hours")

    if len(reasons) == 0:
        return "No Major Risk"

    return ", ".join(reasons)


# --------------------------------
# ADD RISK LEVEL
# --------------------------------

def add_risk_level(df):

    def risk_level(row):

        risk_count = 0

        if row["Average_Score"] < 60:
            risk_count += 1

        if row["Attendance"] < 75:
            risk_count += 1

        if row["Study_Hours"] < 8:
            risk_count += 1

        if risk_count >= 2:
            return "High Risk"

        elif risk_count == 1:
            return "Medium Risk"

        else:
            return "Low Risk"

    df["Risk_Level"] = df.apply(
        risk_level,
        axis=1
    )

    return df 


# --------------------------------
# STAGE 5: ADVANCED STATISTICS
# --------------------------------


# --------------------------------
# OVERALL STATISTICAL SUMMARY
# --------------------------------

def overall_statistics(df):

    summary = {
        "Mean Score": df["Average_Score"].mean(),
        "Median Score": df["Average_Score"].median(),
        "Standard Deviation": df["Average_Score"].std(),
        "Highest Score": df["Average_Score"].max(),
        "Lowest Score": df["Average_Score"].min()
    }

    return summary


def calculate_statistics(df):
    return overall_statistics(df)


# --------------------------------
# STUDY HOURS CORRELATION
# --------------------------------

def study_hours_correlation(df):

    return df["Study_Hours"].corr(
        df["Average_Score"]
    )


# --------------------------------
# ATTENDANCE CORRELATION
# --------------------------------

def attendance_correlation(df):

    return df["Attendance"].corr(
        df["Average_Score"]
    )


# --------------------------------
# DEPARTMENT COMPARISON
# --------------------------------

def department_comparison(df):

    result = df.groupby(
        "Department"
    )["Average_Score"].agg([
        "count",
        "mean",
        "median",
        "min",
        "max"
    ])

    return result


# --------------------------------
# GENDER COMPARISON
# --------------------------------

def gender_comparison(df):

    result = df.groupby(
        "Gender"
    )["Average_Score"].agg([
        "count",
        "mean",
        "median",
        "min",
        "max"
    ])

    return result


# --------------------------------
# PERFORMANCE DISTRIBUTION
# --------------------------------

def performance_distribution(df):

    return df[
        "Performance_Level"
    ].value_counts()


# --------------------------------
# CORRELATION SUMMARY
# --------------------------------

def correlation_summary(df):

    result = df[
        [
            "Study_Hours",
            "Attendance",
            "Assignments",
            "Midterm",
            "Final",
            "Average_Score"
        ]
    ].corr()

    return result