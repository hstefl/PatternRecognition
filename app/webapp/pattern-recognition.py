"""
Web application displaying recognized pattens.
"""
import os
import sys

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.crud import get_all_recognitions

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def home():
    # Query all data from the Recognition table
    recognitions = get_all_recognitions(db.session)

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(
        [(r.id, r.title, r.severity, r.location, r.note) for r in recognitions],
        columns=['Id', 'Title', 'Severity', 'Location', 'Note'])

    # Convert the DataFrame to an HTML table
    recognitions_html_table = (df.to_html(classes='table table-striped', index=False)
                               .replace('\\r\\n', '<br />')
                               .replace('\\n', '<br />')
                               .replace('<td>', '<td class="truncate">'))

    return render_template('home.html', recognitions_html_table=recognitions_html_table)


if __name__ == '__main__':
    app.run(debug=True)
