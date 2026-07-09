from flask import Flask, request, render_template, session, url_for, redirect, Response
from exam_cracker import ExamCrackerAI
from database import init_db, save_exam, get_exam, mark_task_done, get_all_exams, delete_exam, init_journal_table, save_journal, get_journal
import os

app = Flask(__name__)
app.secret_key = "any-random-string-here-for-now"

init_db()
init_journal_table()

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
        hours_per_day=exam["hours_per_day"],
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

TIME_SLOT = ["6-7 AM", "7-8 AM", "8-9 AM", "9-10 AM", "10-11 AM", "11-12 AM",
              "12-1 PM", "1-2 PM", "2-3 PM", "3-4 PM", "4-5 PM", "6-7 PM", "7-8 PM", "8-9 PM"]

import datetime

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    today_str = datetime.date.today().isoformat()

    if request.method == 'POST':
        schedule = {}
        for slot in TIME_SLOT:
            schedule[slot] = request.form.get(f"slot_{slot}", "")

        priorities = [
            request.form.get("priority_1", ""),
            request.form.get("priority_2", ""),
            request.form.get("priority_3", ""),
            request.form.get("priority_4", ""),
        ]
        
        todos_raw = request.form.get("todos", "")
        todos = [t.strip() for t in todos_raw.split("\n") if t.strip()]

        notes = request.form.get("notes", "")
        for_tomorrow = request.form.get("for_tomorrow", "")
        meals = request.form.get("meals", "")
        workout = request.form.get("workout", "")
        mood = request.form.get("mood", "")

        save_journal(today_str, schedule, priorities, todos, notes, for_tomorrow, meals, workout, mood)
        return redirect(url_for('journal'))

    existing = get_journal(today_str)
    return render_template('journal.html', entry=existing, time_slots=TIME_SLOT)
         
@app.route('/export/<int:exam_id>')
def export_calendar(exam_id):
    exam, tasks = get_exam(exam_id)
    if exam is None:
        return "Exam not found", 404
    
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Exam Cracker AI//EN"
    ]

    for t in tasks:
        date_str = t["date"].replace("-", "")
        ics_lines.append("BEGIN:VEVENT")
        ics_lines.append(f"SUMMARY:{t['topic']}")
        ics_lines.append(f"DTSTART;VALUE=DATE:{date_str}")
        ics_lines.append(f"DTEND;VALUE=DATE:{date_str}")
        ics_lines.append(f"DESCRIPTION:{t['minutes']} minutes - Status: {t['status']}")
        ics_lines.append("END:VEVENT")
    
    ics_lines.append("END:VCALENDAR")
    ics_content = "\r\n".join(ics_lines)

    return Response(
        ics_content,
        mimetype="text/calendar",
        headers={"Content-Disposition": f"attachment;filename={exam['exam_name']}_plan.ics"}
    )

import sqlite3

@app.route('/log-time', methods=['POST'])
def log_time():
    exam_id = request.form.get('exam_id')
    hours_spent = float(request.form.get('hours_spent', 0))

    if not exam_id:
        return "Missing exam_id in form submission", 400
    exam_id = int(exam_id)

    conn = sqlite3.connect('exam_cracker.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE exams
        SET hours_per_day = ?
        WHERE id = ?
    ''', (hours_spent, exam_id))
    
    conn.commit()
    conn.close()

    return redirect(url_for('view_plan', exam_id=exam_id))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port)

