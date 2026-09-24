def clean_student_data(df):

    # Remove duplicate records
    df = df.drop_duplicates()

    # Check for missing values
    df = df.dropna()

    # Make sure numerical columns contain numbers
    numerical_columns = [
        "Age",
        "Study_Hours",
        "Attendance",
        "Assignments",
        "Midterm",
        "Final"
    ]

    for column in numerical_columns:
        df[column] = df[column].astype(float)

    return df