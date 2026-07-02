from flask import Flask, request, render_template_string
from exam_cracker import ExamCrackerAI

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ExamCracker AI</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    label { display: block; margin: 0.5rem 0 0.2rem; }
    input, textarea, button { width: 100%; max-width: 500px; padding: 0.5rem; margin-bottom: 1rem; }
    button { width: auto; }
    pre { background: #f7f7f7; padding: 1rem; border: 1px solid #ddd; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>ExamCracker AI</h1>
  <form method="post">
    <label for="exam_name">Exam name</label>
    <input id="exam_name" name="exam_name" required placeholder="e.g. Math Final">

    <label for="exam_date">Exam date (YYYY-MM-DD)</label>
    <input id="exam_date" name="exam_date" type="date" required>

    <label for="syllabus">Syllabus topics (comma separated)</label>
    <textarea id="syllabus" name="syllabus" rows="3" required placeholder="Topic 1, Topic 2, Topic 3"></textarea>

    <label for="hours">Hours available per day</label>
    <input id="hours" name="hours" type="number" min="1" value="2" required>

    <button type="submit">Generate plan</button>
  </form>

  {% if timetable %}
    <h2>Daily timetable</h2>
    <pre>{{ timetable }}</pre>
    <h2>Dashboard</h2>
    <pre>{{ dashboard }}</pre>
  {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    timetable = None
    dashboard = None
    if request.method == 'POST':
        exam_name = request.form.get('exam_name', '').strip()
        exam_date = request.form.get('exam_date', '').strip()
        syllabus_text = request.form.get('syllabus', '')
        hours = int(request.form.get('hours', '0') or 0)

        ai = ExamCrackerAI()
        ai.setup_exam(
            exam_name,
            exam_date,
            [topic.strip() for topic in syllabus_text.split(',') if topic.strip()],
            hours,
        )

        timetable = '\n'.join(ai.get_daily_timetable())
        dashboard = ai.get_dashboard()

    return render_template_string(TEMPLATE, timetable=timetable, dashboard=dashboard)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
