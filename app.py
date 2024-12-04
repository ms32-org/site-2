import os
from time import time
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import json

app = Flask(__name__)

startTime = time()

UPLOAD_FOLDER = os.path.join(os.getcwd(),"static","sounds")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def terminal():
    files = os.listdir(UPLOAD_FOLDER)
    with open(os.path.join(os.getcwd(), "tasks.json"), "r") as file:
        data = json.load(file)

    return render_template("index.html", files=files, tasks=data)


@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        message = request.form["text"]
        with open(os.path.join(os.getcwd(), "message.txt"), "w") as file:
            file.write("sPeAk" + message)
        return redirect("/")
    return "message updated"


@app.route("/command", methods=["GET", "POST"])
def command():
    global startTime
    if request.method == "GET":
        startTime = time()
        cmd = ""
        with open(os.path.join(os.getcwd(), "message.txt"), "r") as file:
            cmd = file.read()
            if cmd == "":
                with open(os.path.join(os.getcwd(), "tasks.json"), "r") as file:
                    tasks = json.load(file)

                tasks_to_delete = None
                for task in tasks["tasks"]:
                    if task["execution_time"] <= datetime.now().strftime("%d-%m-%Y %H:%M"):
                        cmd = task["cmd"]
                        tasks_to_delete = task["id"]
                        break
                tasks["tasks"] = [task for task in tasks["tasks"] if task["id"] != tasks_to_delete]

                with open(os.path.join(os.getcwd(), "tasks.json"), "w") as file:
                    json.dump(tasks, file, indent=4)

        with open(os.path.join(os.getcwd(), "message.txt"), "w") as file:
            file.write("")

        return cmd


@app.route("/audio", methods=["POST", "GET"])
def sounds():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename != "":
            if file.filename.endswith(('.mp3', '.wav')):
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return redirect("/")


@app.route("/play", methods=["POST", "GET"])
def play():
    if request.method == "POST":
        file = request.form["text"]
        if file != "":
            try:
                with open(os.path.join(os.getcwd(), "message.txt"), "w") as a:
                    a.write("pLaY " + file)
            except:
                pass
    return redirect("/")


@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        file = request.form["text"]
        if file != "":
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, file))
            except:
                pass
    return redirect("/")


@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename != "":
            if file.filename.endswith(".exe"):
                file.save(os.path.join(os.getcwd(),"static","updates" "ms32-1.exe"))
                with open(os.path.join(os.getcwd(), "message.txt"), "w") as a:
                    a.write("uPdAtE " + file.filename)
    return redirect("/")


@app.route("/url", methods=["POST", "GET"])
def url():
    if request.method == "POST":
        url = request.form["url"]
        with open(os.path.join(os.getcwd(), "message.txt"), "wt") as file:
            file.write("oPeN " + url)
    return redirect("/")


@app.route("/status", methods=["POST", "GET"])
def status():
    if request.method == "GET":
        deltaTime = time() - startTime
        if deltaTime >= 4:
            redirect("/")
            return "offline"
        else:
            redirect("/ ")
            return "online"


@app.route("/add-task", methods=["POST", "GET"])
def schedule():
    if request.method == "POST":
        data = {"tasks": []}
        cmd = request.form["task"]
        time = datetime.now().strftime("%d-%m-%Y %H:%M")
        execution_time = datetime.strptime(request.form["task-datetime"], "%Y-%m-%dT%H:%M").strftime("%d-%m-%Y %H:%M")
        try:
            with open(os.path.join(os.getcwd(), "tasks.json"), "r") as file:
                data = json.load(file)
        except:
            pass
        task = {
            "id": len(data["tasks"]),
            "cmd": cmd,
            "time": time,
            "execution_time": execution_time
        }
        data["tasks"].append(task)
        with open(os.path.join(os.getcwd(), "tasks.json"), "w") as file:
            json.dump(data, file, indent=4)
        return redirect("/")


@app.route("/delete-task", methods=["POST", "GET"])
def delete_task():
    if request.method == "POST":
        id = request.form["task-id"]
        new_task = {"tasks": []}
        tasks = None
        with open(os.path.join(os.getcwd(), "tasks.json"), "r") as file:
            tasks = json.load(file)
        for task in tasks["tasks"]:
            if str(task["id"]) != id:
                new_task["tasks"].append(task)
        with open(os.path.join(os.getcwd(), "tasks.json"), "w") as file:
            json.dump(new_task, file, indent=4)
    return redirect("/")


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
