from flask import Flask, render_template, request, redirect, session, url_for
import openpyxl
import os

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

# Excel setup
excel_file = "results.xlsx"
if not os.path.exists(excel_file):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Name", "Register Number", "Score"])
    wb.save(excel_file)

# Step-by-step question (10 steps)
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

# Start Quiz
@app.route("/", methods=["GET", "POST"])
def start_quiz():
    if request.method == "POST":
        name = request.form.get("name")
        reg_no = request.form.get("reg_no")
        
        # Validate register number: 12-digit numeric
        if not name or not reg_no or not reg_no.isdigit() or len(reg_no) != 12:
            return "<h3>Error: Please enter a valid Name and a 12-digit Register Number.</h3>"
        
        session["name"] = name
        session["reg_no"] = reg_no
        session["score"] = 0
        session["current_step"] = 0
        return redirect(url_for("step_question"))
    
    return render_template("start.html")

# Step-by-step question route
@app.route("/step", methods=["GET", "POST"])
def step_question():
    current = session.get("current_step", 0)
    score = session.get("score", 0)

    if current >= len(steps):
        # Save result to Excel
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active
        ws.append([session["name"], session["reg_no"], score])
        wb.save(excel_file)
        return redirect(url_for("thankyou"))

    step = steps[current]

    if request.method == "POST":
        user_answer = request.form.get("answer")
        if user_answer == step["answer"]:
            session["score"] = score + 1
        session["current_step"] = current + 1
        return redirect(url_for("step_question"))

    return render_template("question.html", step=step, step_no=current + 1, total=len(steps))

# Thank You page
@app.route("/thankyou")
def thankyou():
    name = session.get("name", "User")
    score = session.get("score", 0)
    return f"""
    <h2>Thanks {name}!</h2>
    <p>Your score: {score} / {len(steps)}</p>
    <p>Your results have been saved successfully.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
