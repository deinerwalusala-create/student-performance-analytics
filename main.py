import pandas as pd
import matplotlib.pyplot as plt


from src.visualization import (
    score_distribution,
    department_performance,
    attendance_vs_score,
    performance_levels
)

from src.statistics import (
    detect_at_risk_students,
    identify_risk_reason,
    add_risk_level
)

from src.load_data import load_student_data
from src.clean_data import clean_student_data

from src.analysis import (
    calculate_average_scores,
    classify_students,
    department_analysis,
    gender_analysis,
    attendance_analysis,
    study_hours_analysis,
    top_students,
    lowest_students,
    performance_summary,
    average_subject_scores,
    score_range,
    department_statistics,
    gender_statistics
)


# --------------------------------
# 1. LOAD DATA
# --------------------------------

df = load_student_data()

print("\n============================== - main.py:44")
print("STUDENT PERFORMANCE ANALYTICS - main.py:45")
print("============================== - main.py:46")

print("\nOriginal Data: - main.py:48")
print(df.head())


# --------------------------------
# 2. CLEAN DATA
# --------------------------------

df = clean_student_data(df)

print("\nData after cleaning: - main.py:58")
print(df.head())


# --------------------------------
# 3. CALCULATE AVERAGE SCORES
# --------------------------------

df = calculate_average_scores(df)


# --------------------------------
# 4. CLASSIFY STUDENTS
# --------------------------------

df = classify_students(df)


# --------------------------------
# 5. DISPLAY STUDENT RESULTS
# --------------------------------

print("\nStudent Performance: - main.py:80")

print(
    df[
        [
            "Student_ID",
            "Name",
            "Average_Score",
            "Performance_Level"
        ]
    ]
)


# --------------------------------
# 6. DEPARTMENT ANALYSIS
# --------------------------------

print("\nDepartment Performance: - main.py:98")

department_result = department_analysis(df)

print(department_result)


# --------------------------------
# 7. GENDER ANALYSIS
# --------------------------------

print("\nGender Performance: - main.py:109")

gender_result = gender_analysis(df)

print(gender_result)


# --------------------------------
# 8. ATTENDANCE CORRELATION
# --------------------------------

correlation = attendance_analysis(df)

print("\nAttendance vs Average Score Correlation: - main.py:122")

print(round(correlation, 2))


# --------------------------------
# 9. TOP STUDENTS
# --------------------------------

print("\nTop 5 Students: - main.py:131")

top = top_students(df)

print(
    top[
        [
            "Student_ID",
            "Name",
            "Average_Score",
            "Performance_Level"
        ]
    ]
)


# --------------------------------
# 10. SAVE RESULTS
# --------------------------------

df.to_csv(
    "outputs/student_performance_results.csv",
    index=False
)

print("\nResults saved successfully! - main.py:156")

# --------------------------------
# 11. DATA VISUALIZATION
# --------------------------------

print("\nGenerating visualizations... - main.py:162")

score_distribution(df)

department_performance(df)

attendance_vs_score(df)

performance_levels(df)



# --------------------------------
# 12. DEEPER DATA ANALYSIS
# --------------------------------

print("\n============================== - main.py:178")
print("DEEPER DATA ANALYSIS - main.py:179")
print("============================== - main.py:180")


# --------------------------------
# STUDY HOURS VS PERFORMANCE
# --------------------------------

study_correlation = study_hours_analysis(df)

print("\nStudy Hours vs Average Score Correlation: - main.py:189")

print(round(study_correlation, 2))


# --------------------------------
# ATTENDANCE VS PERFORMANCE
# --------------------------------

attendance_correlation = attendance_analysis(df)

print("\nAttendance vs Average Score Correlation: - main.py:200")

print(round(attendance_correlation, 2))


# --------------------------------
# PERFORMANCE SUMMARY
# --------------------------------

print("\nPerformance Level Summary: - main.py:209")

print(performance_summary(df))


# --------------------------------
# AVERAGE SUBJECT SCORES
# --------------------------------

print("\nAverage Scores by Assessment: - main.py:218")

subject_scores = average_subject_scores(df)

for subject, score in subject_scores.items():

    print(
        f"{subject}: {score:.2f}"
    )


# --------------------------------
# TOP STUDENTS
# --------------------------------

print("\nTop 5 Students: - main.py:233")

top_students_result = top_students(
    df,
    5
)

print(
    top_students_result[
        [
            "Student_ID",
            "Name",
            "Average_Score",
            "Performance_Level"
        ]
    ].to_string(index=False)
)


# --------------------------------
# SCORE RANGE
# --------------------------------

print("\nScore Range: - main.py:256")

highest, lowest, difference = score_range(df)

print(
    f"Highest Score: {highest:.2f}"
)

print(
    f"Lowest Score: {lowest:.2f}"
)

print(
    f"Score Difference: {difference:.2f}"
)


# --------------------------------
# DEPARTMENT STATISTICS
# --------------------------------

print("\nDepartment Statistics: - main.py:277")

department_result = department_statistics(df)

print(
    department_result.round(2)
)


# --------------------------------
# GENDER STATISTICS
# --------------------------------

print("\nGender Statistics: - main.py:290")

gender_result = gender_statistics(df)

print(
    gender_result.round(2)
)


# --------------------------------
# 12. AT-RISK STUDENT DETECTION
# --------------------------------

print("\n============================== - main.py:303")
print("ATRISK STUDENT DETECTION - main.py:304")
print("============================== - main.py:305")


# Add risk levels

df = add_risk_level(df)


# Identify risk reasons

df["Risk_Reason"] = df.apply(
    identify_risk_reason,
    axis=1
)


# Detect at-risk students

at_risk_students = detect_at_risk_students(df)


# Display at-risk students

print("\nStudents Requiring Academic Attention: - main.py:328")

print(
    at_risk_students[
        [
            "Student_ID",
            "Name",
            "Average_Score",
            "Attendance",
            "Study_Hours",
            "Risk_Level",
            "Risk_Reason"
        ]
    ].to_string(index=False)
)


# --------------------------------
# RISK LEVEL SUMMARY
# --------------------------------

print("\n============================== - main.py:349")
print("RISK LEVEL SUMMARY - main.py:350")
print("============================== - main.py:351")

risk_summary = df["Risk_Level"].value_counts()

print("\nNumber of Students in Each Risk Level: - main.py:355")

print(risk_summary)

# --------------------------------
# SAVE RISK ANALYSIS
# --------------------------------

df.to_csv(
    "outputs/student_performance_with_risk.csv",
    index=False
)

print("\nRisk analysis saved successfully! - main.py:368")