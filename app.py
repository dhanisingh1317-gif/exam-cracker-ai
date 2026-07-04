from flask import Flask, request, render_template, session
from exam_cracker import ExamCrackerAI
import os

app = Flask(__name__)
app.secret_key = "any-random-string-here-for-now"

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
        progress = cracker.get_progress()
        session['progress'] = progress
        session['overflow_warning'] = cracker.overflow_warning
        session['tasks'] =[{"topic" : t["topic"], "date": t ["date"].isoformat(), "status": t["status"], "minutes": t["minutes"]} for t in cracker.tasks]
        session['exam_name'] = exam_name
        return render_template('result.html', exam_name=exam_name, tasks=session['tasks'], overflow_warning=cracker.overflow_warning, progress=progress)
    return render_template('index.html')

@app.route('/mark_done', methods=['POST'])
def mark_done():
    topic_name = request.form.get('topic')
    tasks = session.get('tasks', [])
    for t in tasks:
        if t['topic'] == topic_name:
            t['status'] = 'task completed'
    session['tasks'] = tasks
    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "task completed")
    percent = int((completed / total) * 100) if total> 0 else 0
    progress = {"completed": completed, "total": total, "percent": percent}
    session['progress'] = progress 
    return render_template('result.html', exam_name=session.get('exam_name'), tasks=tasks, overflow_warning=session.get('overflow_warning'), progress=progress)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port)
  