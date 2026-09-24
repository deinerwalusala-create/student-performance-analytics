import pandas as pd

def load_student_data():
    file_path = "data/students.csv"
    df = pd.read_csv(file_path)
    return df