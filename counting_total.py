import os
import pandas as pd

def is_numerical(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def read_csv_with_encoding(file_path):
    encodings = ['utf-8', 'latin1']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding, low_memory=False)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to read the file {file_path} with available encodings.")

def count_rows_in_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split(',')
            if is_numerical(header[5]):
                has_header = True
            else:
                has_header = False
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as file:
            header = file.readline().strip().split(',')
            if is_numerical(header[5]):
                has_header = True
            else:
                has_header = False

    df = read_csv_with_encoding(file_path)
    if has_header:
        return len(df) - 1
    else:
        return len(df)

def count_total_rows_in_folder(folder_path):
    total_rows = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            try:
                row_count = count_rows_in_csv(file_path)
                total_rows += row_count
            except UnicodeDecodeError:
                print(f"Error reading file {file_path} due to encoding issues.")
    return total_rows

def count_unique_coverage_entries(file_path):
    df = read_csv_with_encoding(file_path)
    unique_coverages = df.iloc[:, 7].unique()
    return len(unique_coverages)

def count_total_unique_coverages_in_folder(folder_path):
    unique_coverages_set = set()
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            try:
                df = read_csv_with_encoding(file_path)
                unique_coverages = df.iloc[:, 7].unique()
                unique_coverages_set.update(unique_coverages)
            except UnicodeDecodeError:
                print(f"Error reading file {file_path} due to encoding issues.")
    return len(unique_coverages_set)

# Example usage
folder_path = r"C:\Users\jt4ha\Dark Sky Data Dropbox\Dark Sky Data Team Folder\MHP\Mail 072324\Mail upload 072324"
total_rows = count_total_rows_in_folder(folder_path)
total_unique_coverages = count_total_unique_coverages_in_folder(folder_path)
print(f'Total rows in folder: {total_rows}')
print(f'Total unique coverage entries in folder: {total_unique_coverages}')
