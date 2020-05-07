from flask import Flask
from flask import render_template
import pandas as pd

data = pd.read_csv('rosstat7y.csv')

data = data.iloc[0, :]
data = data.to_dict()
result = {}
for i in data:
    if(data[i] != 0):
        result[i] = data[i]
name = result['0']
inn = result['1']
result.pop('0')
result.pop('1')
app = Flask(__name__)

@app.route('/result')
def result_page():
    return render_template('template.html', name = name,
                           inn = inn, result = result)

if __name__ == '__main__':
    app.run()
