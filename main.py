from flask import Flask
from flask import render_template, request
from motor import Motor
from AI import AIOBJ

app = Flask(__name__)
motor = Motor()
AIOBJ.setupMotionControl(motor)


@app.route("/", methods=['GET', 'POST'])
def remote():
    if request.method == "POST":
        what = request.form['what']
        if what == 'power':
            power = request.form['data']
            print(power)
            motor.power(int(power))

        else:
            # pass
            motor.userControl(what)
    return render_template("index.html")


@app.route("/todo")
def todoList():
    with open('static/todo.txt', 'r') as file:
        contents = file.readlines()
        print(contents)
    task = []
    day = []

    for i in contents:
        l = i.split(':')
        task.append(l[0])
        day.append(l[1])

    return render_template('todo.html', task=task, day=day)


@app.route("/speak", methods=['GET', 'POST'])
def speak():
    if request.method == "POST":
        prompt = request.form['data']
        print("Main.py prompt=", prompt)
        if (AIOBJ.main(prompt)):
            return render_template('speech.html')
        else:
            return render_template('speech.html')

    return render_template('speech.html')


@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    if request.method == 'POST':
        pass
    return render_template('')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8000)
