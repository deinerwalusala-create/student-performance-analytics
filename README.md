
# Student Performance Analytics

A polished Python analytics project that cleans student records, calculates academic performance metrics, identifies students who may need support, and produces a reusable report package with CSV data and presentation-ready charts.

## Features

The program in `main.py` runs the complete analysis pipeline:

- Loads student records from `data/students.csv`.
- Removes duplicate rows and rows containing missing values.
- Converts numeric fields to floating-point values.
- Calculates each student's average across Assignments, Midterm, and Final scores.
- Classifies students into performance levels.
- Compares average performance by department and gender.
- Measures the correlation between attendance, study hours, and average score.
- Lists the top-performing students.
- Reports the highest score, lowest score, and score difference.
- Detects students who may be at academic risk and explains the risk factors.
- Generates five charts for score distribution, department performance, attendance, performance levels, and risk levels.
- Builds a client-ready executive dashboard with KPI cards, recommendations, tables, and visual evidence.
- Exports a machine-readable executive summary for downstream systems or dashboards.
- Saves cleaned and enriched datasets as CSV files.

## Requirements

- Python 3.10 or newer
- pandas
- matplotlib
- seaborn

The exact dependency ranges are recorded in `requirements.txt`.

## Setup

Open a terminal in the project directory and create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

On systems where `python` is not available, use the Python launcher instead:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -r requirements.txt
```

## Run the Project

Run the command from the project root, where the `data` and `outputs` directories are visible:

```powershell
python main.py
```

The program prints a concise analysis dashboard to the terminal, opens the five visualization windows, and saves the report files and chart images in `outputs/`.

For a non-interactive run suitable for CI, servers, screenshots, or a GitHub demo:

```powershell
python main.py --no-show
```

After the run, open `outputs/dashboard.html` in a browser. It is a polished client report that travels with `outputs/figures/` and can be shared as a project demo or attached to a presentation. The matching `outputs/executive_summary.json` file makes the headline metrics easy to connect to another application.

### Command-Line Options

| Option | Purpose | Default |
| --- | --- | --- |
| `--input PATH` | Use a different CSV input file | `data/students.csv` |
| `--output-dir PATH` | Write reports and charts to another directory | `outputs` |
| `--top NUMBER` | Change the number of top students displayed | `5` |
| `--no-show` | Save charts without opening windows | Disabled |

Example:

```powershell
python main.py --input data/students.csv --output-dir outputs/demo --top 3 --no-show
```

## Analysis Rules

### Average score

The average score is calculated as:

```text
(Assignments + Midterm + Final) / 3
```

### Performance classification

| Average score | Performance level |
| --- | --- |
| 80 or higher | Excellent |
| 70 to 79.99 | Good |
| 60 to 69.99 | Average |
| Below 60 | Needs Improvement |

### At-risk detection

A student is included in the at-risk list when at least one of these conditions is true:

- Average score is below 60.
- Attendance is below 75 percent.
- Study hours are below 8.

Risk levels are assigned using the number of triggered conditions:

| Triggered conditions | Risk level |
| --- | --- |
| 0 | Low Risk |
| 1 | Medium Risk |
| 2 or more | High Risk |

The report also lists the specific reasons, such as `Low Academic Score`, `Low Attendance`, or `Low Study Hours`.

## Input Data

The default input file is `data/students.csv`. It contains these columns:

| Column | Description |
| --- | --- |
| `Student_ID` | Unique student identifier |
| `Name` | Student name |
| `Gender` | Student gender |
| `Age` | Student age |
| `Study_Hours` | Study hours used for analysis |
| `Attendance` | Attendance percentage |
| `Assignments` | Assignment score |
| `Midterm` | Midterm score |
| `Final` | Final examination score |
| `Department` | Academic department |

To use another dataset, replace `data/students.csv` while preserving these column names and compatible values.

## Generated Files

The script creates these files in `outputs/`:

- `student_performance_results.csv`: cleaned records with average scores and performance levels.
- `student_performance_with_risk.csv`: the enriched results with risk levels and risk reasons.
- `dashboard.html`: a client-facing executive report with KPI cards, recommendations, tables, and charts.
- `executive_summary.json`: machine-readable KPIs, department scores, top students, and recommendations.
- `figures/score_distribution.png`: distribution of average scores.
- `figures/department_performance.png`: average score by department.
- `figures/attendance_vs_score.png`: attendance and average score relationship.
- `figures/performance_levels.png`: number of students in each performance category.
- `figures/risk_levels.png`: number of students in each risk category.

The charts are displayed with `matplotlib` during an interactive run and saved automatically under `outputs/figures/`. The `--no-show` option is useful when generating assets without opening chart windows.

## Visualizations

The repository includes example charts generated from the supplied student dataset.

### Score Distribution

![Distribution of student average scores](outputs/figures/score_distribution.png)

### Average Performance by Department

![Average performance by department](outputs/figures/department_performance.png)

### Attendance Versus Student Performance

![Attendance versus student performance](outputs/figures/attendance_vs_score.png)

### Student Performance Levels

![Student performance levels](outputs/figures/performance_levels.png)

### Risk Levels

![Students by risk level](outputs/figures/risk_levels.png)

### Risk Level Breakdown

![Risk level breakdown for students](students%20by%20risk%20level.png)

## Project Structure

```text
student-performance-analytics/
|-- data/
|   `-- students.csv
|-- outputs/
|   |-- student_performance_results.csv
|   |-- student_performance_with_risk.csv
|   |-- dashboard.html
|   |-- executive_summary.json
|   `-- figures/
|       |-- attendance_vs_score.png
|       |-- department_performance.png
|       |-- performance_levels.png
|       |-- risk_levels.png
|       `-- score_distribution.png
|-- src/
|   |-- analysis.py       # Scores, classifications, summaries, and correlations
|   |-- clean_data.py     # Duplicate, missing-value, and numeric conversion handling
|   |-- load_data.py      # CSV loading
|   |-- report.py         # Executive HTML and JSON report generation
|   |-- statistics.py     # At-risk detection and risk explanations
|   `-- visualization.py  # Seaborn and Matplotlib charts
|-- requirements.txt      # Reproducible Python dependencies
|-- main.py               # Configurable CLI and end-to-end workflow
`-- README.md
```

## Showcase Highlights

The included dataset produces a useful story for a portfolio or LinkedIn post:

- Computer Science has a higher average score than Information Technology in this sample.
- Attendance and study hours both show a strong positive relationship with average score.
- The pipeline surfaces students who need attention instead of reporting averages alone.
- Every run produces shareable CSV reports and a five-chart visual summary.
- The HTML dashboard turns raw analysis into a deliverable a client can scan without reading Python code.

The charts embedded below are examples generated from the supplied dataset. Run `python main.py --no-show` to regenerate the current versions.

## Troubleshooting

### `ModuleNotFoundError`

Install the dependencies into the same interpreter used to run the project:

```powershell
python -m pip install pandas matplotlib seaborn
```

### Input file not found

Run `main.py` from the project root. The loader uses the relative path `data/students.csv`.

### Charts do not appear

Run the script in a desktop Python environment with a graphical Matplotlib backend. In a headless environment, set a non-interactive backend before importing Matplotlib, for example:

```powershell
$env:MPLBACKEND = "Agg"
python main.py
```

With a non-interactive backend, the analysis runs but chart windows will not be shown.

## Notes

- This project is designed as a command-line analytics script rather than a web application.
- Correlation values describe the relationship in the supplied dataset; they do not establish causation.
- The output CSV files in `outputs/` may be regenerated each time the script runs.
