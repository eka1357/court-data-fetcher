from flask import Flask, render_template, request
from scraper import get_case_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    cnr_number = request.form.get('cnr_number')
    if not cnr_number:
        return "CNR Number is required", 400

    case_data = get_case_data(cnr_number)
    
    return render_template('result.html', case=case_data, cnr_number=cnr_number)

if __name__ == '__main__':
    app.run(debug=True)
