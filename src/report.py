import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path


def _format_score(value):
    return f"{value:.1f}"


def build_recommendations(df):
    recommendations = []

    high_risk_count = int((df["Risk_Level"] == "High Risk").sum())
    medium_risk_count = int((df["Risk_Level"] == "Medium Risk").sum())
    if high_risk_count:
        recommendations.append(
            f"Prioritize a weekly support plan for {high_risk_count} high-risk student(s), "
            "starting with attendance, study habits, and assessment recovery."
        )
    if medium_risk_count:
        recommendations.append(
            f"Set an early-warning check-in for {medium_risk_count} medium-risk student(s) "
            "before the next assessment cycle."
        )

    weakest_subject = df[["Assignments", "Midterm", "Final"]].mean().idxmin()
    recommendations.append(
        f"Review {weakest_subject.lower()} support materials because it is the lowest "
        "average assessment area in this dataset."
    )

    lowest_department = df.groupby("Department")["Average_Score"].mean().idxmin()
    recommendations.append(
        f"Compare teaching practices and student support coverage in {lowest_department}, "
        "the lowest-performing department in this sample."
    )
    return recommendations


def build_summary(df, top_n=5):
    department_scores = df.groupby("Department")["Average_Score"].mean()
    performance_counts = df["Performance_Level"].value_counts()
    risk_counts = df["Risk_Level"].value_counts()
    top_students = df.nlargest(top_n, "Average_Score")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "students_analyzed": int(len(df)),
        "average_score": round(float(df["Average_Score"].mean()), 2),
        "average_attendance": round(float(df["Attendance"].mean()), 2),
        "average_study_hours": round(float(df["Study_Hours"].mean()), 2),
        "attendance_correlation": round(float(df["Attendance"].corr(df["Average_Score"])), 3),
        "study_hours_correlation": round(float(df["Study_Hours"].corr(df["Average_Score"])), 3),
        "high_risk_students": int(risk_counts.get("High Risk", 0)),
        "medium_risk_students": int(risk_counts.get("Medium Risk", 0)),
        "performance_levels": {str(key): int(value) for key, value in performance_counts.items()},
        "department_average_scores": {
            str(key): round(float(value), 2) for key, value in department_scores.items()
        },
        "top_students": [
            {
                "student_id": str(row.Student_ID),
                "name": str(row.Name),
                "average_score": round(float(row.Average_Score), 2),
            }
            for row in top_students.itertuples()
        ],
    }
    summary["recommendations"] = build_recommendations(df)
    return summary


def _metric_card(label, value, detail):
    return (
        '<article class="metric-card">'
        f'<p class="metric-label">{escape(label)}</p>'
        f'<p class="metric-value">{escape(str(value))}</p>'
        f'<p class="metric-detail">{escape(detail)}</p>'
        "</article>"
    )


def generate_client_report(df, report_path, figure_dir, top_n=5):
    report_path = Path(report_path)
    figure_dir = Path(figure_dir)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary = build_summary(df, top_n)

    department_table = (
        df.groupby("Department")["Average_Score"]
        .mean()
        .sort_values(ascending=False)
        .round(2)
        .rename("Average Score")
        .to_frame()
        .to_html(classes="data-table", border=0)
    )
    risk_table = df[df["Risk_Level"] != "Low Risk"][
        ["Student_ID", "Name", "Average_Score", "Attendance", "Study_Hours", "Risk_Level", "Risk_Reason"]
    ].copy()
    for column in ["Average_Score", "Attendance", "Study_Hours"]:
        risk_table[column] = risk_table[column].round(1)
    risk_html = risk_table.to_html(index=False, classes="data-table", border=0)
    recommendations_html = "".join(
        f"<li>{escape(item)}</li>" for item in summary["recommendations"]
    )
    top_students_html = "".join(
        f"<tr><td>{escape(item['student_id'])}</td><td>{escape(item['name'])}</td>"
        f"<td>{item['average_score']:.1f}</td></tr>"
        for item in summary["top_students"]
    )

    charts = [
        ("Score distribution", "figures/score_distribution.png"),
        ("Department performance", "figures/department_performance.png"),
        ("Attendance versus score", "figures/attendance_vs_score.png"),
        ("Performance levels", "figures/performance_levels.png"),
        ("Risk levels", "figures/risk_levels.png"),
    ]
    charts_html = "".join(
        f'<figure><img src="{path}" alt="{escape(title)}"><figcaption>{escape(title)}</figcaption></figure>'
        for title, path in charts
        if (figure_dir / Path(path).name).exists()
    )

    generated = datetime.now().strftime("%B %d, %Y at %H:%M")
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Student Performance Intelligence Report</title>
<style>
:root {{ --ink: #17212b; --muted: #60707d; --line: #d9e3e8; --paper: #f5f8f7; --teal: #007f78; --gold: #e5a93d; --coral: #d8664c; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; color: var(--ink); background: var(--paper); font-family: Georgia, 'Times New Roman', serif; }}
.shell {{ max-width: 1180px; margin: 0 auto; padding: 38px 24px 70px; }}
.hero {{ background: var(--ink); color: white; padding: 42px; border-radius: 8px; position: relative; overflow: hidden; }}
.hero:after {{ content: ''; position: absolute; width: 260px; height: 260px; right: -80px; top: -100px; border: 42px solid var(--teal); border-radius: 50%; opacity: .8; }}
.eyebrow {{ color: #a8d8d2; font: 700 12px/1.2 Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase; }}
h1 {{ max-width: 680px; margin: 14px 0 10px; font-size: clamp(36px, 6vw, 68px); line-height: .98; font-weight: 500; }}
.subtitle {{ max-width: 620px; color: #d5e0e5; font: 16px/1.6 Arial, sans-serif; }}
.meta {{ margin-top: 28px; color: #aabac2; font: 12px Arial, sans-serif; }}
h2 {{ margin: 46px 0 16px; font-size: 28px; font-weight: 500; }}
.metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 24px; }}
.metric-card, .panel {{ background: white; border: 1px solid var(--line); border-radius: 6px; padding: 22px; }}
.metric-label, .metric-detail {{ color: var(--muted); font: 12px Arial, sans-serif; }}
.metric-label {{ margin: 0 0 14px; text-transform: uppercase; letter-spacing: 1px; }}
.metric-value {{ margin: 0; color: var(--teal); font-size: 36px; }}
.metric-detail {{ margin: 10px 0 0; }}
.grid-two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
.data-table {{ width: 100%; border-collapse: collapse; font: 14px Arial, sans-serif; }}
.data-table th, .data-table td {{ border-bottom: 1px solid var(--line); padding: 11px 8px; text-align: left; }}
.data-table th {{ color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: .8px; }}
.recommendations {{ padding-left: 22px; font: 15px/1.7 Arial, sans-serif; }}
.recommendations li {{ margin: 8px 0; }}
.chart-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; }}
figure {{ margin: 0; padding: 12px; background: white; border: 1px solid var(--line); border-radius: 6px; }}
figure img {{ display: block; width: 100%; height: auto; }}
figcaption {{ padding: 12px 4px 4px; color: var(--muted); font: 12px Arial, sans-serif; text-transform: uppercase; letter-spacing: .8px; }}
.footer {{ margin-top: 46px; color: var(--muted); font: 12px/1.6 Arial, sans-serif; border-top: 1px solid var(--line); padding-top: 18px; }}
@media (max-width: 760px) {{ .shell {{ padding: 20px 14px 50px; }} .hero {{ padding: 28px 22px; }} .metrics, .grid-two, .chart-grid {{ grid-template-columns: 1fr; }} h1 {{ font-size: 44px; }} }}
</style>
</head>
<body>
<main class="shell">
<section class="hero">
<p class="eyebrow">Executive intelligence report</p>
<h1>Student performance, made actionable.</h1>
<p class="subtitle">A decision-ready view of achievement, engagement, and intervention opportunities across the student dataset.</p>
<p class="meta">Generated {escape(generated)} &middot; {summary['students_analyzed']} students analyzed</p>
</section>
<section class="metrics">
{_metric_card('Average score', f"{summary['average_score']:.1f}", 'out of 100')}
{_metric_card('Average attendance', f"{summary['average_attendance']:.1f}%", 'engagement signal')}
{_metric_card('High-risk students', summary['high_risk_students'], 'priority intervention')}
{_metric_card('Study-hour correlation', f"{summary['study_hours_correlation']:.2f}", 'with average score')}
</section>
<h2>What leaders should know</h2>
<section class="grid-two">
<article class="panel"><h3>Recommended actions</h3><ul class="recommendations">{recommendations_html}</ul></article>
<article class="panel"><h3>Top performers</h3><table class="data-table"><thead><tr><th>ID</th><th>Student</th><th>Score</th></tr></thead><tbody>{top_students_html}</tbody></table></article>
</section>
<h2>Performance by department</h2>
<section class="panel">{department_table}</section>
<h2>Students needing attention</h2>
<section class="panel">{risk_html}</section>
<h2>Visual evidence</h2>
<section class="chart-grid">{charts_html}</section>
<footer class="footer">Methodology: average score is calculated from Assignments, Midterm, and Final. Risk flags use score, attendance, and study-hour thresholds defined in the project source. Correlation indicates association, not causation.</footer>
</main>
</body>
</html>"""

    report_path.write_text(html, encoding="utf-8")
    summary_path = report_path.with_name("executive_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return report_path, summary_path
