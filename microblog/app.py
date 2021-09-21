from flask import Flask, request, render_template

app = Flask(__name__)
datas = [{"message": "Hello World"}]

@app.route('/')
@app.route('/data', methods=['post'])
def index():
    if request.method == 'POST':
        datas.append({"message": request.form.get("text")})
    print(datas)
    return render_template("index.html", datas=datas)


app.run()
