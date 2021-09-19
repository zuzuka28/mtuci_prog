from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/data', methods=['post'])
def index():
    data = "say your name"
    if request.method == 'POST':
        data = request.form.get("text")

    return render_template("index.html", data=data)


app.run()
