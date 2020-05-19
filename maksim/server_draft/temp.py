from flask import Flask
from flask import render_template
import pandas as pd

data = pd.read_csv('rosstat7y.csv')

data = data.iloc[0, :]
data = data.to_dict()
name = data['0']
inn = int(data['5'])
okpo = data['1']
okopf = data['2']
okfs = data['3']
okved = data['4']
data = [(k, v) for k, v in data.items()] 
data = data[9:200]
imp = pd.read_csv('imp.csv', index_col = 0)
imp = imp.iloc[:, 0]
imp = imp.to_dict()

print(okved)

data = sorted(data[6:], key=lambda data: imp[int(data[0])], reverse=True)

result = []
for i in data:
    if(i[1] != 0):
        result.append((i[0], i[1]))

app = Flask(__name__, static_folder="static_dir")

@app.route('/result')
def result_page():
    return render_template('template.html', name = name,
                           okpo = okpo, okopf = okopf,
                           okfs = okfs, okved = okved,
                           inn = inn, result = result)

if __name__ == '__main__':
    app.run()
