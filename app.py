from flask import Flask, render_template, request, redirect, session, url_for
import json, os

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

# -------------------------
# Step-by-step questions
# -------------------------
steps = [
    {"q": "Look at the first two numbers: 3, 6. How do they relate?",
     "options": ["Add 3", "Multiply by 2", "Add 6", "Subtract 3"],
     "answer": "Multiply by 2"},
    {"q": "Check next two numbers: 6, 12. Is the same pattern holding?",
     "options": ["Add 6", "Multiply by 2", "Multiply by 3", "Add 2"],
     "answer": "Multiply by 2"},
    {"q": "Next: 12 → 24. Same pattern?",
     "options": ["Multiply by 2", "Multiply by 3", "Add 12", "Add 6"],
     "answer": "Multiply by 2"},
    {"q": "Identify the operation consistently applied across terms",
     "options": ["Addition", "Multiplication", "Alternating", "Random"],
     "answer": "Multiplication"},
    {"q": "How many times has the operation been applied so far?",
     "options": ["1", "2", "3", "4"],
     "answer": "3"},
    {"q": "Predict next number using the operation",
     "options": ["36", "48", "50", "60"],
     "answer": "48"},
    {"q": "Verify if pattern fits all previous numbers",
     "options": ["Yes", "No", "Sometimes", "Cannot decide"],
     "answer": "Yes"},
    {"q": "Form a general formula for nth term",
     "options": ["a_n = 3*2^(n-1)", "a_n = 2n", "a_n = n^2 + 2", "a_n = 3n"],
     "answer": "a_n = 3*2^(n-1)"},
    {"q": "Using the formula, what is the 5th term?",
     "options": ["48", "50", "45", "54"],
     "answer": "48"},
    {"q": "Confirm if 5th term fits the sequence",
     "options": ["Yes", "No", "Only sometimes", "Not enough info"],
     "answer": "Yes"},
]

# -------------------------
# Save results in JSON file
# -------------------------
def save_result(name, reg_no, score):
    data = {"name": name, "reg_no": reg_no, "score": score}
    file_path = "results.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                results = json.load(f)
            except json.JSONDecodeError:
                results = []
    else:
        results = []

    results.append(data)

    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)


# -------------------------
# Start Quiz
# -------------------------
@app.route("/", methods=["GET", "POST"])
def start_quiz():
    if request.method == "POST":
        name = request.form.get("name")
        reg_no = request.form.get("reg_no")

        # Validate 12-digit numeric register number
        if not name or not reg_no or not reg_no.isdigit() or len(reg_no) != 12:
            return "<h3>Error: Enter a valid Name and a 12-digit Register Number.</h3>"

        session["name"] = name
        session["reg_no"] = reg_no
        session["score"] = 0
        session["current_step"] = 0
        return redirect(url_for("step_question"))

    return render_template("start.html")


# -------------------------
# Step-by-step question route
# -------------------------
@app.route("/step", methods=["GET", "POST"])
def step_question():
    current = session.get("current_step", 0)
    score = session.get("score", 0)

    if current >= len(steps):
        # Save result to JSON file
        save_result(session["name"], session["reg_no"], session["score"])
        return redirect(url_for("thankyou"))

    step = steps[current]

    if request.method == "POST":
        user_answer = request.form.get("answer")
        if user_answer == step["answer"]:
            session["score"] = score + 1
        session["current_step"] = current + 1
        return redirect(url_for("step_question"))

    return render_template("question.html", step=step, step_no=current + 1, total=len(steps))


# -------------------------
# Thank You page
# -------------------------
@app.route("/thankyou")
def thankyou():
    name = session.get("name", "User")
    score = session.get("score", 0)
    return f"""
    <h2>Thanks {name}!</h2>
    <p>Your score: {score} / {len(steps)}</p>
    <p>Your results have been saved successfully (in results.json).</p>
    """


# -------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
