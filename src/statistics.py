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