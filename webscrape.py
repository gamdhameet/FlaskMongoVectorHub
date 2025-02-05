import pdfplumber
import csv
import re

def extract_grade_data(pdf_path, csv_path):
    # Pattern to match course lines with counts and instructor
    course_pattern = re.compile(
        r'^([A-Z]+-\d+-\d+)\s+'      # Course code
        r'(\d+)\s+'                 # A count
        r'(\d+)\s+'                 # B count
        r'(\d+)\s+'                 # C count
        r'(\d+)\s+'                 # D count
        r'(\d+)\s+'                 # F count
        r'(\d+)\s+'                 # Total A-F
        r'([\d.]+)\s+'              # GPA
        r'(?:\d+\s+){5}'           # Skip I/S/U/Q/X columns
        r'\d+\s+'                  # Skip total column
        r'(.+)$'                   # Instructor
    )

    with pdfplumber.open(pdf_path) as pdf, \
         open(csv_path, 'w', newline='') as csvfile:

        writer = csv.writer(csvfile)
        headers = ['Course', 'A', 'B', 'C', 'D', 'F', 'Total A-F', 'GPA', 'Instructor']
        writer.writerow(headers)

        for page_num, page in enumerate(pdf.pages):
            print(f"\nProcessing page {page_num + 1}")
            text = page.extract_text()
            if not text:
                print("No text found on page")
                continue

            lines = text.split('\n')
            prev_line = None

            for line_num, line in enumerate(lines):
                line = re.sub(r'\s{2,}', ' ', line).strip()
                
                # Skip headers and totals
                if any(s in line for s in ['COURSE TOTAL:', 'TEXAS A&M UNIVERSITY', 'COLLEGE:', 'DEPARTMENT:']):
                    print(f"Skipping line {line_num + 1}: {line[:50]}...")
                    prev_line = None
                    continue
                
                print(f"Checking line {line_num + 1}: {line}")
                
                # Check if current line is a course line
                match = course_pattern.match(line)
                if match:
                    print("MATCH FOUND!")
                    groups = match.groups()
                    try:
                        writer.writerow([
                            groups[0],   # Course
                            groups[1],   # A count
                            groups[2],   # B count
                            groups[3],   # C count
                            groups[4],   # D count
                            groups[5],   # F count
                            groups[6],   # Total A-F
                            groups[7],   # GPA
                            groups[8].strip()  # Instructor
                        ])
                        print(f"Wrote record for {groups[0]}")
                    except IndexError as e:
                        print(f"Error processing line: {e}")
                        print(f"Groups: {groups}")
                    prev_line = None
                else:
                    # Check if previous line was a course line and this is a percentage line
                    if prev_line:
                        print("Checking for percentage line combination")
                        combined_line = f"{prev_line} {line}"
                        match = course_pattern.match(combined_line)
                        if match:
                            print("MATCH FOUND IN COMBINED LINES!")
                            groups = match.groups()
                            try:
                                writer.writerow([
                                    groups[0],   # Course
                                    groups[1],   # A count
                                    groups[2],   # B count
                                    groups[3],   # C count
                                    groups[4],   # D count
                                    groups[5],   # F count
                                    groups[6],   # Total A-F
                                    groups[7],   # GPA
                                    groups[8].strip()  # Instructor
                                ])
                                print(f"Wrote record for {groups[0]} from combined lines")
                            except IndexError as e:
                                print(f"Error processing combined lines: {e}")
                            prev_line = None
                        else:
                            prev_line = None
                    else:
                        # Store line for potential combination with next line
                        prev_line = line

if __name__ == "__main__":
    pdflol = 'ARCHdata\ARCHFALL22.csv' ## Change filepath output location for each different PDF
    extract_grade_data('ARCHpdf\grd2022fallarch.pdf', pdflol) ## Change PDF 
    print("\nProcessing complete. Check ", pdflol)