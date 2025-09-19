from flask import Flask, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# def get_employee_data():
#     scope = ["https://spreadsheets.google.com/feeds",
#              "https://www.googleapis.com/auth/drive"]

#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
#     client = gspread.authorize(creds)

#     sheet = client.open("").sheet1
#     rows = sheet.get_all_records()

#     employees = []
#     for row in rows:
#         emp = {
#             "name": row.get("Your full name", ""),
#             "qualification": row.get("Academic Qualification", ""),
#             "experience": row.get("Overall total experience in years as on 15th August 2025", ""),
#             "designation": row.get("Your current Designation", ""),
#             "id_card": row.get("ID card number", ""),
#             "joining_date": row.get("Date of joining CODE", ""),
#             "bio": row.get("Short Bio - A brief description of yourself that you want to see on our internal webpage", ""),
#             "interests": row.get("Mention 3 lines: about your interests outside of work, your hobby or a fun fact about you.", ""),
#             "photo_url": row.get("Please attach a recent photograph that can be put up on the webpage", ""),
#             "team": row.get("Team", "")
#         }
#         employees.append(emp)

#     return employees


# @app.route("/")
# def home():
#     employees = get_employee_data()
#     return render_template("index.html", employees=employees)


# if __name__ == "__main__":
#     app.run(debug=True)

def get_employee_data():
    return [
        {
            "name": "John Doe",
            "qualification": "M.Tech Computer Science",
            "experience": "5",
            "designation": "Software Engineer",
            "id_card": "CODE123",
            "joining_date": "2021-06-15",
            "bio": "Passionate backend developer.",
            "interests": "Photography, Hiking, Chess",
            "photo_url": "https://via.placeholder.com/150",
            "team": "NPTEL Coding"
        },
        {
            "name": "Jane Smith",
            "qualification": "PhD AI",
            "experience": "8",
            "designation": "Team Lead",
            "id_card": "CODE456",
            "joining_date": "2019-03-10",
            "bio": "AI researcher and mentor.",
            "interests": "Music, Reading, Yoga",
            "photo_url": "https://via.placeholder.com/150",
            "team": "AI Research"
        }
    ]

@app.route("/")
def home():
    employees = get_employee_data()
    return render_template("index.html", employees=employees)

if __name__ == "__main__":
    app.run(debug=True)