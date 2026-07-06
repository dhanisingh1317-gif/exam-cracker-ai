from flask import Flask, request, render_template, session,  request, url_for, redirect
from exam_cracker import ExamCrackerAI
from database import init_db, save_exam, get_exam, mark_task_done, get_all_exams, delete_exam
import os

app = Flask(__name__)
app.secret_key = "any-random-string-here-for-now"

init_db()


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/planner', methods=['GET', 'POST'])
def planner():
    if request.method == 'POST':
        exam_name = request.form.get('exam_name')
        exam_date = request.form.get('exam_date')
        exam_syllabus = request.form.get('syllabus')
        hours = int(request.form.get('hours'))
        syllabus = [topic.strip() for topic in exam_syllabus.split(',') if topic.strip()]
        
        cracker = ExamCrackerAI()
        cracker.setup_exam(exam_name, exam_date, syllabus, hours)
        cracker.build_task()
        
        exam_id = save_exam(exam_name, exam_date, hours, cracker.overflow_warning, cracker.tasks)
        return redirect(url_for('view_plan', exam_id=exam_id))
    
    return render_template('index.html')

@app.route('/plan/<int:exam_id>')
def view_plan(exam_id):
    exam, tasks = get_exam(exam_id)
    if exam is None:
        return "Exam Not Found", 404
    
    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "task completed")
    percent = int((completed / total) * 100) if total > 0 else 0
    progress = {"completed": completed, "total": total, "percent": percent}

    return render_template(
        'result.html',
        exam_id=exam_id,
        exam_name=exam["exam_name"],
        tasks=tasks,
        overflow_warning=bool(exam["overflow_warning"]),
        progress=progress
    )

@app.route('/mark_done/<int:exam_id>', methods=['POST'])
def mark_done(exam_id):
    topic_name = request.form.get('topic')
    mark_task_done(exam_id, topic_name)
    return redirect(url_for('view_plan', exam_id=exam_id))

@app.route('/my-plans')
def my_plans():
    exams = get_all_exams()
    return render_template('my_plans.html', exams=exams)

@app.route('/delete/<int:exam_id>', methods=['POST'])
def delete_plan(exam_id):
    delete_exam(exam_id)
    return redirect(url_for('my_plans'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port)

