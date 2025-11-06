import requests
import csv
from flask import Flask, render_template






GOOGLE_SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRWxYCp46X3bjAXYFrB0P7By8P8A4kDUkCSpkb09LnSr-NpeVBhbAE3ETgHvkpfszG_U8U9mApXZwmc/pub?gid=1235795060&single=true&output=csv'

app = Flask(__name__)



TEAM_NAME_MAP = {
    # --- BS DEGREE ---
    "POD Ops": "BS Degree - Support",
    "Portal": "BS Degree - Portal",
    "Tech & Data": "BS Degree - Tech and Data",
    "Course Instructor": "BS Degree - Instructors",
    "IIC": "BS Degree - IIC",
    "Student affairs": "BS Degree - Student Affairs",
    "CODE Chapter": "BS Degree - CODE Chapters",

    # --- NPTEL ---
    "NPTEL Support": "NPTEL - Support",
    "NPTEL Portal": "NPTEL - Portal",
    "Local chapter": "NPTEL - Local Chapter",
    "NPTEL Tech": "NPTEL - Tech",

    # --- WMT ---
    "Support": "WMT - Support and Portal",
    "Portal (WMT)": "WMT - Course Management",
    "Industry relationships & Outreach": "WMT - Industry Relationship",

    # --- OTHER CODE ---
    "School Connect Team": "School Connect",
    "Executive Education": "Executive Education",
    "Code ex/workshops": "Workshops",
    "ICMAI": "ICMAI",

    # --- FUNCTIONS ---
    "Accounts - CODE/NPTEL": "Accounts",
    "BS Degree Accounts": "Accounts",
    "CODE - Accounts": "Accounts",
    "CODE Marketing": "Marketing",
    "Marketing": "Marketing",
    "Text / Translation": "Translation and Transcription",
    "Text Transcription": "Translation and Transcription",
    "Translation": "Translation and Transcription",
    "LC + Exam": "Exam",
    "Exams + Soft skill": "Exam",
    "Studio Team": "Studio",
    "CSR": "CSR",

    # --- TECH/DEV TEAMS ---
    "Dev": "Tech team",
    "Developer": "Tech team",
    "CODE - Development": "Tech team",
    "SEEK": "SEEK",
    "Workflow": "Workflow"
}


def get_employee_data():
    """
    Fetches employee data from the Google Sheet and processes columns
    including 'Program names' and 'Team Names' directly.
    """
    employee_list = []
    try:
        response = requests.get(GOOGLE_SHEET_CSV_URL)
        response.raise_for_status()

        response.encoding = 'utf-8'
        csv_data = response.text

        reader = csv.DictReader(csv_data.splitlines())

        for row in reader:
            # ✅ --- Clean up text values ---
            for key, value in row.items():
                if isinstance(value, str):
                    row[key] = (
                        value.strip()
                        .replace('\r\n', '\n')
                        .replace('\r', '\n')
                        .replace("â€“", "–")
                        .replace("â€”", "—")
                        .replace("â€˜", "‘")
                        .replace("â€™", "’")
                        .replace("â€œ", "“")
                        .replace("â€�", "”")
                    )

            # ✅ --- Handle employee photo ---
            if 'photoURL' in row and row['photoURL']:
                file_id = None
                try:
                    file_id = row['photoURL'].split('/d/')[1].split('/')[0]
                except IndexError:
                    try:
                        file_id = row['photoURL'].split('?id=')[1]
                    except IndexError:
                        file_id = None

                if file_id:
                    row['directPhotoURL'] = f"https://lh3.googleusercontent.com/d/{file_id}"
                else:
                    row['directPhotoURL'] = '/static/images/default-avatar.png'
            else:
                row['directPhotoURL'] = '/static/images/default-avatar.png'

            # ✅ --- Use dropdown values directly ---
            row['program'] = row.get('Program names', '').strip()
            row['team'] = row.get('Team Names', '').strip()



            original_team = row.get("teamname", "").strip()
            normalized_team = TEAM_NAME_MAP.get(original_team, original_team)
            row["normalized_teamname"] = normalized_team

            employee_list.append(row)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google Sheet: {e}")
        return []

    return employee_list


@app.route('/')
def home():
    employees_unsorted = get_employee_data()
    employees = sorted(employees_unsorted, key=lambda emp: emp.get('fullName', ''))

    return render_template('index.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
