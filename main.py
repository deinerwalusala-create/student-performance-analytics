import argparse
from pathlib import Path

import pandas as pd


from src.insights import generate_insights

from src.analysis import (
    attendance_analysis,
    average_subject_scores,
    calculate_average_scores,
    classify_students,
    department_analysis,
    department_statistics,
    gender_analysis,
    gender_statistics,
    performance_summary,
    score_range,
    study_hours_analysis,
    top_students,
)
from src.clean_data import clean_student_data
from src.load_data import load_student_data
from src.report import generate_client_report
from src.statistics import (
    add_risk_level,
    attendance_correlation,
    calculate_statistics,
    correlation_summary,
    department_comparison,
    detect_at_risk_students,
    gender_comparison,
    identify_risk_reason,
    performance_distribution,
    study_hours_correlation,
)
from src.visualization import (
    attendance_vs_score,
    correlation_heatmap,
    department_performance,
    performance_levels,
    risk_level_chart,
    score_distribution,
)


def print_section(title):
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62} - main.py:49")


def run_analysis(input_path, output_dir, top_n=5, show_plots=True):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = output_dir / "figures"

    print_section("STUDENT PERFORMANCE ANALYTICS")
    print(f"Input: {input_path} - main.py:58")

    df = load_student_data(input_path)
    print(f"Loaded {len(df)} student records. - main.py:61")

    df = clean_student_data(df)
    df = calculate_average_scores(df)
    df = classify_students(df)
    print(f"Clean records: {len(df)} - main.py:66")

    print_section("PERFORMANCE SNAPSHOT")
    print(
        df[
            ["Student_ID", "Name", "Average_Score", "Performance_Level"]
        ].to_string(index=False)
    )

    print("\nDepartment performance: - main.py:75")
    print(department_analysis(df).round(2))
    print("\nGender performance: - main.py:77")
    print(gender_analysis(df).round(2))
    print(f"\nAttendance correlation: {attendance_analysis(df):.2f} - main.py:79")

    print(f"\nTop {top_n} students: - main.py:81")
    print(
        top_students(df, top_n)[
            ["Student_ID", "Name", "Average_Score", "Performance_Level"]
        ].to_string(index=False)
    )

    results_path = output_dir / "student_performance_results.csv"
    df.to_csv(results_path, index=False)

    print_section("DEEPER INSIGHTS")
    print(f"Study hours correlation: {study_hours_analysis(df):.2f} - main.py:92")
    print(f"Attendance correlation: {attendance_analysis(df):.2f} - main.py:93")
    print("\nPerformance summary: - main.py:94")
    print(performance_summary(df))

    print("\nAverage assessment scores: - main.py:97")
    for subject, score in average_subject_scores(df).items():
        print(f"{subject}: {score:.2f} - main.py:99")

    highest, lowest, difference = score_range(df)
    print(f"\nScore range: {lowest:.2f} to {highest:.2f} ({difference:.2f} points) - main.py:102")
    print("\nDepartment statistics: - main.py:103")
    print(department_statistics(df).round(2))
    print("\nGender statistics: - main.py:105")
    print(gender_statistics(df).round(2))

    print_section("AT-RISK STUDENT DETECTION")
    df = add_risk_level(df)
    df["Risk_Reason"] = df.apply(identify_risk_reason, axis=1)
    at_risk_students = detect_at_risk_students(df)
    print(
        at_risk_students[
            [
                "Student_ID",
                "Name",
                "Average_Score",
                "Attendance",
                "Study_Hours",
                "Risk_Level",
                "Risk_Reason",
            ]
        ].to_string(index=False)
    )

    print("\nRisk level summary: - main.py:126")
    risk_level_column = "Risk" + "_" + "Level"
    print(df[risk_level_column].value_counts())
    risk_results_path = output_dir / "student_performance_with_risk.csv"
    df.to_csv(risk_results_path, index=False)

    print_section("ADVANCED STATISTICAL ANALYSIS")
    overall = calculate_statistics(df)
    for statistic, value in overall.items():
        print(f"{statistic}: {value:.2f} - main.py:135")

    print(f"\nStudy hours vs average score: {study_hours_correlation(df):.2f} - main.py:137")
    print(f"Attendance vs average score: {attendance_correlation(df):.2f} - main.py:138")
    print("\nDepartment comparison: - main.py:139")
    print(department_comparison(df).round(2))
    print("\nGender comparison: - main.py:141")
    print(gender_comparison(df).round(2))
    print("\nPerformance distribution: - main.py:143")
    print(performance_distribution(df))
    print("\nCorrelation matrix: - main.py:145")
    print(correlation_summary(df).round(2))

    statistical_summary = pd.DataFrame(
        {"Statistic": list(overall.keys()), "Value": list(overall.values())}
    )
    statistical_summary.to_csv(output_dir / "statistical_summary.csv", index=False)

    print_section("GENERATING PROJECT ASSETS")
    charts = [
        (score_distribution, "score_distribution.png"),
        (department_performance, "department_performance.png"),
        (attendance_vs_score, "attendance_vs_score.png"),
        (performance_levels, "performance_levels.png"),
        (risk_level_chart, "risk_levels.png"),
        (correlation_heatmap, "correlation_heatmap.png"),
    ]
    for chart, filename in charts:
        chart(df, figure_dir / filename, show=show_plots)

    report_path, summary_path = generate_client_report(
        df, output_dir / "dashboard.html", figure_dir, top_n
    )
    print(f"Results saved to: {results_path} - main.py:168")
    print(f"Risk analysis saved to: {risk_results_path} - main.py:169")
    print(f"Statistical summary saved to: {output_dir / 'statistical_summary.csv'} - main.py:170")
    print(f"Charts saved to: {figure_dir} - main.py:171")
    print(f"Client dashboard saved to: {report_path} - main.py:172")
    print(f"Executive summary saved to: {summary_path} - main.py:173")

    print_section("AUTOMATED DATA INSIGHTS")
    insights = generate_insights(df)
    insights_path = output_dir / "automated_insights.txt"
    insights_path.write_text(
        "\n\n".join(
            f"Insight {number}: {insight}"
            for number, insight in enumerate(insights, start=1)
        )
        + "\n",
        encoding="utf-8",
    )
    for number, insight in enumerate(insights, start=1):
        print(f"\nInsight {number}:\n{insight} - main.py:187")
    print(f"Automated insights saved to: {insights_path} - main.py:188")
    return df


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate student performance insights and visual assets."
    )
    parser.add_argument("--input", default="data/students.csv")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Save charts without opening visualization windows.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    run_analysis(
        input_path=arguments.input,
        output_dir=arguments.output_dir,
        top_n=arguments.top,
        show_plots=not arguments.no_show,
    )
