import os
import csv
from tqdm import tqdm  # For progress tracking

def combine_all_department_csvs(root_folder, output_file):
    """
    Combines CSV files from all subdirectories into one output file.
    
    Args:
        root_folder (str): Path to parent folder containing department folders
        output_file (str): Path for combined output CSV
    """
    # Collect all CSV file paths
    csv_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for f in filenames:
            if f.lower().endswith('.csv'):
                csv_files.append(os.path.join(dirpath, f))

    if not csv_files:
        print("No CSV files found in the directory structure")
        return

    # Initialize counters
    total_files = len(csv_files)
    total_rows = 0
    header = None

    # Process files
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        # Initialize progress bar
        with tqdm(total=total_files, desc="Combining CSVs") as pbar:
            for i, csv_file in enumerate(csv_files):
                with open(csv_file, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    file_header = next(reader)
                    
                    # Validate consistent structure
                    if i == 0:
                        header = file_header
                        writer.writerow(header)
                    else:
                        if file_header != header:
                            print(f"\nWarning: Header mismatch in {csv_file} - skipping")
                            continue
                    
                    # Write rows
                    file_rows = 0
                    for row in reader:
                        writer.writerow(row)
                        file_rows += 1
                    
                    total_rows += file_rows
                    pbar.update(1)
                    pbar.set_postfix({
                        'Files Done': f"{i+1}/{total_files}",
                        'Total Rows': total_rows
                    })

    print(f"\nSuccessfully combined {total_files} files from {root_folder}")
    print(f"Final output contains {total_rows:,} rows")
    print(f"Output file: {os.path.abspath(output_file)}")

# Usage Example
if __name__ == "__main__":
    # Configure these paths
    ROOT_FOLDER = "/ANEXUS"  # Parent folder containing department subfolders
    OUTPUT_CSV = "TAMUsitedata/all_departments_combined.csv"
    
    combine_all_department_csvs(ROOT_FOLDER, OUTPUT_CSV)