from flask import Flask, request, flash, render_template
from wtforms import Form, TextField, validators
import requests
import config
import os

# App config.
DEBUG = False
app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.urandom(30)

class WebForm(Form):
    link = TextField('link', validators=[validators.Regexp('^https://javhd.com/en/id/[\d]+/[\w\d\-?=]+$', message="Incorrect JavHD URL"),
                                         validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = WebForm(request.form)

    if request.method == 'POST' and form.validate():
        url = request.form['link']
        payload = {'service': 'javhd', 'apikey': config.keys, 'data': url}
        try:
            data = requests.post("https://api.area3.org", data=payload).json()
            player = data['link']
            flash("Get link thành công", 'success')
            flash(player, 'player')
        except:
            flash("Get link thất bại", 'fail')

    return render_template('main.html', form=form)

if __name__ == "__main__":
    app.run()