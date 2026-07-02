from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        exam_name = request.form.get('exam_name')
        return render_template('result.html', exam_name=exam_name)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
