import streamlit as st
import pandas as pd
import sys
import os



# --------------------------------
# CONNECT TO PROJECT
# --------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from src.clean_data import clean_student_data
from src.statistics import add_risk_level, identify_risk_reason
from src.insights import generate_insights
import matplotlib.pyplot as plt
import seaborn as sns


# --------------------------------
# PAGE SETTINGS
# --------------------------------

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------
# CUSTOM DASHBOARD STYLE
# --------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.metric-card {
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# TITLE
# --------------------------------

st.markdown(
    '<div class="main-title">🎓 Student Performance Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An interactive data science dashboard for analyzing '
    'student academic performance.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------
# LOAD DATA
# --------------------------------

file_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "students.csv"
)

df = pd.read_csv(file_path)


# --------------------------------
# CLEAN DATA
# --------------------------------

df = clean_student_data(df)


# --------------------------------
# CALCULATE AVERAGE SCORE
# --------------------------------

df["Average_Score"] = (
    df["Assignments"]
    + df["Midterm"]
    + df["Final"]
) / 3


# --------------------------------
# PERFORMANCE LEVEL
# --------------------------------

def performance_level(score):

    if score >= 80:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Average"

    else:
        return "Needs Improvement"


df["Performance_Level"] = (
    df["Average_Score"]
    .apply(performance_level)
)


# --------------------------------
# RISK ANALYSIS
# --------------------------------

df = add_risk_level(df)

df["Risk_Reason"] = df.apply(
    identify_risk_reason,
    axis=1
)


# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.header(
    "🔎 Student Filters"
)

if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.clear()
    st.rerun()


# Student search

search_name = st.sidebar.text_input(
    "Search Student",
    placeholder="Enter student name..."
)


# Student selector
student_names = ["None"] + sorted(
    df["Name"].dropna().unique().tolist()
)

selected_student = st.sidebar.selectbox(
    "Select Student",
    student_names
)


# Gender filter

genders = [
    "All"
] + sorted(
    df["Gender"].unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    genders
)


departments = [
    "All"
] + sorted(
    df["Department"].unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Department",
    departments
)


performance_levels = [
    "All",
    "Excellent",
    "Good",
    "Average",
    "Needs Improvement"
]

selected_performance = st.sidebar.selectbox(
    "Performance Level",
    performance_levels
)


risk_levels = [
    "All",
    "Low Risk",
    "Medium Risk",
    "High Risk"
]

selected_risk = st.sidebar.selectbox(
    "Risk Level",
    risk_levels
)


# --------------------------------
# APPLY FILTERS
# --------------------------------

filtered_df = df.copy()


if selected_department != "All":

    filtered_df = filtered_df[
        filtered_df["Department"]
        == selected_department
    ]


if selected_performance != "All":

    filtered_df = filtered_df[
        filtered_df["Performance_Level"]
        == selected_performance
    ]


if selected_risk != "All":

    filtered_df = filtered_df[
        filtered_df["Risk_Level"]
        == selected_risk
    ]



# Gender filter

if selected_gender != "All":

    filtered_df = filtered_df[
        filtered_df["Gender"]
        == selected_gender
    ]


# Student name search

if search_name:

    filtered_df = filtered_df[
        filtered_df["Name"]
        .str.contains(
            search_name,
            case=False,
            na=False
        )
    ]

    # Student dropdown filter

if selected_student != "None":
    filtered_df = filtered_df[
        filtered_df["Name"] == selected_student
    ]

# --------------------------------
# SELECTED STUDENT SUMMARY
# --------------------------------

if len(filtered_df) > 0 and (
    search_name or selected_student != "None"
):

    st.header("👤 Student Profile")

    student = filtered_df.iloc[0]

    st.markdown(
        f"""
        ### 🎓 {student["Name"]}

        **Student ID:** {student["Student_ID"]}  
        **Department:** {student["Department"]}  
        **Gender:** {student["Gender"]}  
        **Age:** {student["Age"]}
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📊 Average Score",
            f"{student['Average_Score']:.2f}"
        )

    with col2:
        st.metric(
            "📅 Attendance",
            f"{student['Attendance']:.2f}%"
        )

    with col3:
        st.metric(
            "📚 Study Hours",
            f"{student['Study_Hours']:.2f}"
        )

    with col4:
        st.metric(
            "⚠️ Risk Level",
            student["Risk_Level"]
        )

    st.write(
        f"**Performance Level:** "
        f"{student['Performance_Level']}"
    )

    st.write(
        f"**Risk Reason:** "
        f"{student['Risk_Reason']}"
    )

elif search_name or selected_student != "None":

    st.warning(
        "No student matches the selected filters."
    )



    # --------------------------------
# DASHBOARD OVERVIEW
# --------------------------------

st.info(
    """
    📌 **Dashboard Overview**

    This dashboard analyzes student academic performance using
    assignments, midterm examinations, final examinations,
    attendance, and study hours.

    The system also identifies students who may require
    academic attention based on their performance and risk level.
    """
)

# --------------------------------
# KEY METRICS
# --------------------------------

# --------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------

st.header(
    "📊 Key Performance Indicators"
)


# Calculate KPI values

total_students = len(filtered_df)

average_score = filtered_df[
    "Average_Score"
].mean()

average_attendance = filtered_df[
    "Attendance"
].mean()

average_study_hours = filtered_df[
    "Study_Hours"
].mean()

at_risk_count = len(
    filtered_df[
        filtered_df["Risk_Level"].isin(
            ["Medium Risk", "High Risk"]
        )
    ]
)


high_risk_count = len(
    filtered_df[
        filtered_df["Risk_Level"]
        == "High Risk"
    ]
)


# Create KPI cards

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        label="👨‍🎓 Total Students",
        value=total_students
    )


with col2:

    st.metric(
        label="📊 Average Score",
        value=f"{average_score:.2f}"
    )


with col3:

    st.metric(
        label="📅 Attendance",
        value=f"{average_attendance:.2f}%"
    )


with col4:

    st.metric(
        label="📚 Study Hours",
        value=f"{average_study_hours:.2f}"
    )


with col5:

    st.metric(
        label="⚠️ At-Risk Students",
        value=at_risk_count
    )


# High-risk notification

if high_risk_count > 0:

    st.warning(
        f"⚠️ {high_risk_count} student(s) "
        "are currently classified as High Risk."
    )

else:

    st.success(
        "✅ No students are currently "
        "classified as High Risk."
    )



    # --------------------------------
# ATTENDANCE STATUS
# --------------------------------

if len(filtered_df) > 0 and (
    search_name or selected_student != "None"
):

    student = filtered_df.iloc[0]

    attendance = student["Attendance"]

    st.subheader("📅 Attendance Status")

    if attendance >= 80:
        st.success(
            f"🟢 Good attendance: {attendance:.2f}%"
        )

    elif attendance >= 60:
        st.warning(
            f"🟡 Moderate attendance: {attendance:.2f}%"
        )

    else:
        st.error(
            f"🔴 Low attendance: {attendance:.2f}%"
        )




        # --------------------------------
# ACADEMIC RECOMMENDATION
# --------------------------------

if len(filtered_df) > 0 and (
    search_name or selected_student != "None"
):

    student = filtered_df.iloc[0]

    score = student["Average_Score"]
    attendance = student["Attendance"]
    study_hours = student["Study_Hours"]
    risk = student["Risk_Level"]

    st.subheader("💡 Academic Recommendation")

    recommendations = []

    if score < 60:
        recommendations.append(
            "Focus on improving overall academic performance."
        )

    if attendance < 60:
        recommendations.append(
            "Improve class attendance and avoid unnecessary absences."
        )

    if study_hours < 5:
        recommendations.append(
            "Increase regular study time outside class."
        )

    if risk == "High Risk":
        recommendations.append(
            "The student should receive immediate academic support."
        )

    if risk == "Medium Risk":
        recommendations.append(
            "Monitor the student's progress and provide additional support."
        )

    if not recommendations:
        recommendations.append(
            "Maintain the current study habits and academic performance."
        )

    for recommendation in recommendations:
        st.info("📌 " + recommendation)



# --------------------------------
# PERFORMANCE GAUGE
# --------------------------------

if len(filtered_df) > 0 and (
    search_name or selected_student != "None"
):

    student = filtered_df.iloc[0]

    score = student["Average_Score"]

    st.subheader("🎯 Overall Performance")

    progress = max(0, min(score, 100)) / 100

    st.progress(progress)

    if score >= 80:
        st.success(
            f"🌟 Excellent performance — {score:.2f}%"
        )

    elif score >= 70:
        st.info(
            f"👍 Good performance — {score:.2f}%"
        )

    elif score >= 60:
        st.warning(
            f"📚 Average performance — {score:.2f}%"
        )

    else:
        st.error(
            f"⚠️ Needs improvement — {score:.2f}%"
        )

    # --------------------------------
# SELECTED STUDENT SCORE BREAKDOWN
# --------------------------------

if search_name and len(filtered_df) > 0:

    st.subheader("📈 Student Score Breakdown")

    student = filtered_df.iloc[0]

    score_data = pd.DataFrame({
        "Assessment": [
            "Assignments",
            "Midterm",
            "Final"
        ],
        "Score": [
            student["Assignments"],
            student["Midterm"],
            student["Final"]
        ]
    })

    st.bar_chart(
        score_data.set_index("Assessment")
    )



    # --------------------------------
# PERFORMANCE TREND
# --------------------------------

if len(filtered_df) > 0 and (
    search_name or selected_student != "None"
):

    student = filtered_df.iloc[0]

    trend_data = pd.DataFrame({
        "Assessment": [
            "Assignments",
            "Midterm",
            "Final"
        ],
        "Score": [
            student["Assignments"],
            student["Midterm"],
            student["Final"]
        ]
    })

    st.subheader("📈 Performance Trend")

    st.line_chart(
        trend_data.set_index("Assessment")
    )

    first_score = student["Assignments"]
    final_score = student["Final"]

    if final_score > first_score:
        st.success(
            "📈 Performance improved from Assignments to Final."
        )

    elif final_score < first_score:
        st.warning(
            "📉 Performance declined from Assignments to Final."
        )

    else:
        st.info(
            "➡️ Performance remained at the same level."
        )
   




# --------------------------------
# PERFORMANCE ANALYSIS
# --------------------------------

st.header(
    "🏆 Performance Analysis"
)



# --------------------------------
# PERFORMANCE SUMMARY
# --------------------------------

performance_summary = (
    filtered_df["Performance_Level"]
    .value_counts()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🌟 Excellent",
        performance_summary.get("Excellent", 0)
    )

with col2:
    st.metric(
        "👍 Good",
        performance_summary.get("Good", 0)
    )

with col3:
    st.metric(
        "📚 Average",
        performance_summary.get("Average", 0)
    )

with col4:
    st.metric(
        "⚠️ Needs Improvement",
        performance_summary.get(
            "Needs Improvement",
            0
        )
    )


col1, col2 = st.columns(2)


# --------------------------------
# PERFORMANCE DISTRIBUTION
# --------------------------------

with col1:

    st.subheader(
        "Students by Performance Level"
    )

    performance_counts = (
        filtered_df["Performance_Level"]
        .value_counts()
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.barplot(
        x=performance_counts.index,
        y=performance_counts.values,
        ax=ax
    )

    ax.set_xlabel(
        "Performance Level"
    )

    ax.set_ylabel(
        "Number of Students"
    )

    ax.set_title(
        "Performance Distribution"
    )

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# --------------------------------
# DEPARTMENT COMPARISON
# --------------------------------

with col2:

    st.subheader(
        "Average Score by Department"
    )

    department_scores = (
        filtered_df
        .groupby("Department")[
            "Average_Score"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.barplot(
        x=department_scores.index,
        y=department_scores.values,
        ax=ax
    )

    ax.set_xlabel(
        "Department"
    )

    ax.set_ylabel(
        "Average Score"
    )

    ax.set_title(
        "Department Performance"
    )

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# --------------------------------
# GENDER COMPARISON
# --------------------------------

st.subheader(
    "👥 Average Score by Gender"
)


gender_scores = (
    filtered_df
    .groupby("Gender")[
        "Average_Score"
    ]
    .mean()
)


fig, ax = plt.subplots(
    figsize=(10, 5)
)

sns.barplot(
    x=gender_scores.index,
    y=gender_scores.values,
    ax=ax
)

ax.set_xlabel(
    "Gender"
)

ax.set_ylabel(
    "Average Score"
)

ax.set_title(
    "Average Academic Score by Gender"
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

   
# --------------------------------
# RISK ANALYSIS
# --------------------------------

st.header(
    "⚠️ Student Risk Analysis"
)


col1, col2 = st.columns(2)


# --------------------------------
# RISK LEVEL CHART
# --------------------------------

with col1:

    st.subheader(
        "Students by Risk Level"
    )

    risk_counts = (
        filtered_df["Risk_Level"]
        .value_counts()
        .reindex(
            [
                "Low Risk",
                "Medium Risk",
                "High Risk"
            ],
            fill_value=0
        )
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.barplot(
        x=risk_counts.index,
        y=risk_counts.values,
        ax=ax
    )

    ax.set_xlabel(
        "Risk Level"
    )

    ax.set_ylabel(
        "Number of Students"
    )

    ax.set_title(
        "Student Risk Distribution"
    )

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# --------------------------------
# RISK REASONS
# --------------------------------

with col2:

    st.subheader(
        "Reasons Students Are At Risk"
    )

    risk_reason_counts = {}

    at_risk = filtered_df[
        filtered_df["Risk_Reason"]
        != "No Major Risk"
    ]

    for reasons in at_risk[
        "Risk_Reason"
    ]:

        for reason in reasons.split(", "):

            if reason in risk_reason_counts:

                risk_reason_counts[
                    reason
                ] += 1

            else:

                risk_reason_counts[
                    reason
                ] = 1


    if risk_reason_counts:

        reason_series = pd.Series(
            risk_reason_counts
        ).sort_values(
            ascending=False
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        sns.barplot(
            x=reason_series.values,
            y=reason_series.index,
            ax=ax
        )

        ax.set_xlabel(
            "Number of Students"
        )

        ax.set_ylabel(
            "Risk Reason"
        )

        ax.set_title(
            "Reasons for Academic Risk"
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

    else:

        st.success(
            "No major risk factors found."
        )


# --------------------------------
# STUDENTS REQUIRING ATTENTION
# --------------------------------

st.subheader(
    "🚨 Students Requiring Academic Attention"
)


students_at_risk = filtered_df[
    filtered_df["Risk_Level"].isin(
        [
            "Medium Risk",
            "High Risk"
        ]
    )
]


if len(students_at_risk) > 0:

    risk_columns = [
        "Student_ID",
        "Name",
        "Average_Score",
        "Attendance",
        "Study_Hours",
        "Risk_Level",
        "Risk_Reason"
    ]

    st.dataframe(
        students_at_risk[
            risk_columns
        ].round(2),
        use_container_width=True
    )

else:

    st.success(
        "No students require immediate academic attention."
    )


# --------------------------------
# STUDY HOURS VS SCORE
# --------------------------------

st.header(
    "📚 Study Hours vs Academic Performance"
)


fig, ax = plt.subplots(
    figsize=(10, 5)
)

sns.scatterplot(
    data=filtered_df,
    x="Study_Hours",
    y="Average_Score",
    hue="Risk_Level",
    s=100,
    ax=ax
)

ax.set_title(
    "Study Hours vs Average Score"
)

ax.set_xlabel(
    "Study Hours"
)

ax.set_ylabel(
    "Average Score"
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# --------------------------------
# ATTENDANCE VS SCORE
# --------------------------------

st.header(
    "📅 Attendance vs Academic Performance"
)


fig, ax = plt.subplots(
    figsize=(10, 5)
)

sns.scatterplot(
    data=filtered_df,
    x="Attendance",
    y="Average_Score",
    hue="Risk_Level",
    s=100,
    ax=ax
)

ax.set_title(
    "Attendance vs Average Score"
)

ax.set_xlabel(
    "Attendance (%)"
)

ax.set_ylabel(
    "Average Score"
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# --------------------------------
# CORRELATION HEATMAP
# --------------------------------

st.header(
    "🔗 Correlation Analysis"
)


correlation_columns = [
    "Study_Hours",
    "Attendance",
    "Assignments",
    "Midterm",
    "Final",
    "Average_Score"
]


correlation_matrix = (
    filtered_df[
        correlation_columns
    ].corr()
)


fig, ax = plt.subplots(
    figsize=(10, 7)
)

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    ax=ax
)

ax.set_title(
    "Correlation Between Student Performance Variables"
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)






        







# --------------------------------
# STUDENT RECORDS
# --------------------------------

st.header(
    "👨‍🎓 Student Records"
)


display_columns = [
    "Student_ID",
    "Name",
    "Gender",
    "Age",
    "Department",
    "Study_Hours",
    "Attendance",
    "Assignments",
    "Midterm",
    "Final",
    "Average_Score",
    "Performance_Level",
    "Risk_Level",
    "Risk_Reason"
]


st.dataframe(
    filtered_df[
        display_columns
    ].round(2),
    use_container_width=True
)


# --------------------------------
# AUTOMATED INSIGHTS
# --------------------------------

st.header(
    "💡 Automated Insights"
)


insights = generate_insights(
    filtered_df
)


for number, insight in enumerate(
    insights,
    start=1
):

    st.info(
        f"Insight {number}: {insight}"
    )


    # DATA-DRIVEN INSIGHTS

st.subheader("🧠 Data-Driven Insights")

top_department = (
    df.groupby("Department")["Average_Score"]
    .mean()
    .idxmax()
)

top_department_score = (
    df.groupby("Department")["Average_Score"]
    .mean()
    .max()
)

lowest_department = (
    df.groupby("Department")["Average_Score"]
    .mean()
    .idxmin()
)

lowest_department_score = (
    df.groupby("Department")["Average_Score"]
    .mean()
    .min()
)

highest_student = df.loc[
    df["Average_Score"].idxmax()
]

lowest_student = df.loc[
    df["Average_Score"].idxmin()
]

st.info(
    f"🏆 **Highest performing department:** "
    f"{top_department} with an average score of "
    f"{top_department_score:.2f}."
)

st.warning(
    f"📉 **Department with the lowest average score:** "
    f"{lowest_department} with an average score of "
    f"{lowest_department_score:.2f}."
)

st.success(
    f"🌟 **Top performing student:** "
    f"{highest_student['Name']} with an average score of "
    f"{highest_student['Average_Score']:.2f}."
)

st.error(
    f"⚠️ **Student with the lowest average score:** "
    f"{lowest_student['Name']} with an average score of "
    f"{lowest_student['Average_Score']:.2f}."
)



  


# --------------------------------
# DOWNLOAD DATA
# --------------------------------

st.header(
    "⬇️ Download Filtered Data"
)


csv_data = filtered_df.to_csv(
    index=False
)


st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)



# INDIVIDUAL STUDENT REPORT

if len(filtered_df) > 0 and (
    search_name or selected_student != "None"
):

    student = filtered_df.iloc[0]

    st.subheader("📄 Individual Student Report")

    report_data = pd.DataFrame({
        "Field": [
            "Student ID",
            "Name",
            "Gender",
            "Age",
            "Department",
            "Assignments Score",
            "Midterm Score",
            "Final Score",
            "Average Score",
            "Attendance (%)",
            "Study Hours",
            "Performance Level",
            "Risk Level",
            "Risk Reason"
        ],

        "Value": [
            student["Student_ID"],
            student["Name"],
            student["Gender"],
            student["Age"],
            student["Department"],
            student["Assignments"],
            student["Midterm"],
            student["Final"],
            round(student["Average_Score"], 2),
            round(student["Attendance"], 2),
            round(student["Study_Hours"], 2),
            student["Performance_Level"],
            student["Risk_Level"],
            student["Risk_Reason"]
        ]
    })

    st.dataframe(
        report_data,
        use_container_width=True,
        hide_index=True
    )

    csv_report = report_data.to_csv(index=False)

    st.download_button(
        label="📥 Download Individual Student Report",
        data=csv_report,
        file_name=f"{student['Name']}_Student_Report.csv",
        mime="text/csv"
    )


    # STUDENT COMPARISON

st.subheader("👥 Compare Two Students")

student_list = sorted(
    df["Name"].dropna().unique().tolist()
)

col1, col2 = st.columns(2)

with col1:
    student_1 = st.selectbox(
        "Select First Student",
        ["None"] + student_list,
        key="comparison_student_1"
    )

with col2:
    student_2 = st.selectbox(
        "Select Second Student",
        ["None"] + student_list,
        key="comparison_student_2"
    )

if student_1 != "None" and student_2 != "None":

    student_a = df[df["Name"] == student_1].iloc[0]
    student_b = df[df["Name"] == student_2].iloc[0]

    comparison_data = pd.DataFrame({
        "Metric": [
            "Average Score",
            "Attendance (%)",
            "Study Hours",
            "Assignments",
            "Midterm",
            "Final"
        ],

        student_1: [
            student_a["Average_Score"],
            student_a["Attendance"],
            student_a["Study_Hours"],
            student_a["Assignments"],
            student_a["Midterm"],
            student_a["Final"]
        ],

        student_2: [
            student_b["Average_Score"],
            student_b["Attendance"],
            student_b["Study_Hours"],
            student_b["Assignments"],
            student_b["Midterm"],
            student_b["Final"]
        ]
    })

    st.dataframe(
        comparison_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📊 Performance Comparison")

    chart_data = pd.DataFrame({
        "Student": [student_1, student_2],
        "Average Score": [
            student_a["Average_Score"],
            student_b["Average_Score"]
        ]
    })

    st.bar_chart(
        chart_data.set_index("Student")
    )




    # DEPARTMENT PERFORMANCE ANALYSIS

st.subheader("🏫 Department Performance Analysis")

department_analysis = (
    df.groupby("Department")
    .agg(
        Students=("Student_ID", "count"),
        Average_Score=("Average_Score", "mean"),
        Average_Attendance=("Attendance", "mean"),
        Average_Study_Hours=("Study_Hours", "mean")
    )
    .reset_index()
)

department_analysis["Average_Score"] = (
    department_analysis["Average_Score"].round(2)
)

department_analysis["Average_Attendance"] = (
    department_analysis["Average_Attendance"].round(2)
)

department_analysis["Average_Study_Hours"] = (
    department_analysis["Average_Study_Hours"].round(2)
)

st.dataframe(
    department_analysis,
    use_container_width=True,
    hide_index=True
)

st.subheader("📊 Average Score by Department")

department_chart = department_analysis[
    ["Department", "Average_Score"]
].set_index("Department")

st.bar_chart(department_chart)


# ADVANCED ANALYTICS

st.subheader("🔬 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:

    st.write("### 📚 Study Hours vs Average Score")

    study_analysis = (
        df.groupby("Study_Hours")["Average_Score"]
        .mean()
        .reset_index()
    )

    study_analysis["Average_Score"] = (
        study_analysis["Average_Score"].round(2)
    )

    st.line_chart(
        study_analysis.set_index("Study_Hours")
    )


with col2:

    st.write("### 📅 Attendance vs Average Score")

    attendance_analysis = (
        df.groupby("Attendance")["Average_Score"]
        .mean()
        .reset_index()
    )

    attendance_analysis["Average_Score"] = (
        attendance_analysis["Average_Score"].round(2)
    )

    st.line_chart(
        attendance_analysis.set_index("Attendance")
    )


# KEY PERFORMANCE INSIGHTS

st.subheader("💡 Key Performance Insights")

overall_average = df["Average_Score"].mean()
average_attendance = df["Attendance"].mean()
average_study_hours = df["Study_Hours"].mean()

high_risk_students = len(
    df[df["Risk_Level"] == "High Risk"]
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Overall Average",
        f"{overall_average:.2f}"
    )

with col2:
    st.metric(
        "📅 Average Attendance",
        f"{average_attendance:.2f}%"
    )

with col3:
    st.metric(
        "📚 Average Study Hours",
        f"{average_study_hours:.2f}"
    )

with col4:
    st.metric(
        "⚠️ High Risk Students",
        high_risk_students
    )




    # TOP PERFORMING STUDENTS

st.subheader("🏆 Top Performing Students")

top_students = (
    df[
        [
            "Student_ID",
            "Name",
            "Department",
            "Average_Score",
            "Performance_Level"
        ]
    ]
    .sort_values(
        "Average_Score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_students.round(2),
    use_container_width=True,
    hide_index=True
)



# RISK SUMMARY

st.subheader("⚠️ Risk Summary")

risk_summary = (
    df["Risk_Level"]
    .value_counts()
    .reindex(
        [
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ],
        fill_value=0
    )
)

total_students = len(df)

col1, col2, col3 = st.columns(3)

with col1:
    low_percentage = (
        risk_summary["Low Risk"] / total_students * 100
    )

    st.metric(
        "🟢 Low Risk",
        f"{risk_summary['Low Risk']} "
        f"({low_percentage:.1f}%)"
    )

with col2:
    medium_percentage = (
        risk_summary["Medium Risk"] / total_students * 100
    )

    st.metric(
        "🟡 Medium Risk",
        f"{risk_summary['Medium Risk']} "
        f"({medium_percentage:.1f}%)"
    )

with col3:
    high_percentage = (
        risk_summary["High Risk"] / total_students * 100
    )

    st.metric(
        "🔴 High Risk",
        f"{risk_summary['High Risk']} "
        f"({high_percentage:.1f}%)"
    )
# --------------------------------
# FOOTER
# --------------------------------

st.markdown("---")

st.caption(
    "Student Performance Analytics | "
    "Python • Pandas • Streamlit • Data Science"
)