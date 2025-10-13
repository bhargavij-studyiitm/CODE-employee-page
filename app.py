import requests
import csv
from flask import Flask, render_template

GOOGLE_SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRWxYCp46X3bjAXYFrB0P7By8P8A4kDUkCSpkb09LnSr-NpeVBhbAE3ETgHvkpfszG_U8U9mApXZwmc/pub?gid=1235795060&single=true&output=csv'

app = Flask(__name__)

def get_employee_data():
    """
    Fetches the public Google Sheet CSV and converts it into a list of dictionaries.
    """
    employee_list = []
    try:
        # Using requests
        response = requests.get(GOOGLE_SHEET_CSV_URL)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        csv_data = response.text

        reader = csv.DictReader(csv_data.splitlines()) #csv.DictReader(...)`: This is a powerful CSV parser that treats each row as a dictionary,
        #   using the first row (headers like 'name', 'title', etc.) as the keys.
        
        for row in reader:
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

            employee_list.append(row)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google Sheet: {e}")
        return []
        
    return employee_list

@app.route('/')
def home():

    employees_unsorted = get_employee_data()

    employees = sorted(employees_unsorted, key=lambda emp: emp.get('fullName', ''))
    
    return render_template('index.html', employees=employees) #passes employees to be used in html using jinja 2

if __name__ == '__main__':
    app.run(debug=True)