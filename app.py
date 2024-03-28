from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///questions.db")

category = ["reconciliation", "packing", "outcome", "counting", "DIN", "Gennaro", "HSF"]

index = 1

@app.route("/")
def index():
    keys = db.execute("SELECT id, key_word, question, answer FROM querie;")

    return render_template("index.html", args=keys)

@app.route("/query")
def query():
    return render_template("questions.html", keywords=category)


@app.route("/answer")
def answer():
    id = request.args.get("id")
    answer = request.args.get("answer")
    if not answer:
        return redirect("/")
    else:
        db.execute("UPDATE querie SET answer = ? WHERE id = ?;", answer, id)
    return redirect("/")


@app.route("/erase")
def erase():
    id = request.args.get("id")
    db.execute("DELETE FROM querie WHERE id = ?;", id)
    return redirect("/")


@app.route("/del_ans")
def delete_answer():
    id = request.args.get("id")
    db.execute("UPDATE querie SET answer = 'no answer' WHERE id = ?;", id)
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        question = request.form.get("question")
        key = request.form.get("keyword")
        if key == None:
            return redirect("query")
        db.execute("INSERT INTO querie (key_word, question, answer) VALUES(?, ?, ?);", key, question, "no answer")
        return redirect("/")

    else:
        return render_template("questions.html", keywords=category)
