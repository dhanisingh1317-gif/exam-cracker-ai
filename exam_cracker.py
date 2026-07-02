import datetime 
exam_name = input("Oh no ! Exam came to trouble you ! Don't worry let me relive some stress, tell me the name of the exam: ")
date_str = input("So.. When is this EXAM ? (YYYY.MM.DD) :")
syllabus_entry = input("Please enter the syllabus topics, separated by commas: ")
syllabus = []
for topic in syllabus_entry.split(","):
    syllabus.append(topic.strip())
hours = int(input("Well.. If i ask you how many hours per day you can study, what would be your answer ? :"))

class ExamCrackerAI:
    def __init__(self):
        self.exam_name = ""
        self.exam_date = None
        self.syllabus = []
        self.hours_per_day = 0

    def setup_exam(self, exam_name, exam_date_str, syllabus, hours_per_day):
        self.exam_name = exam_name
        self.exam_date = datetime.datetime.strptime(exam_date_str, "%Y.%m.%d").date()
        self.syllabus = syllabus
        self.hours_per_day = hours_per_day
    
    def show_syllabus(self):
        for topic in self.syllabus:
            print(f"- {topic}")
    
    def days_till_exam(self):
        today = datetime.date.today()
        remaining = (self.exam_date - today).days
        return remaining
    
    def generate_schedule(self):
        days_remaining = self.days_till_exam()
        if days_remaining <= 0:
            return{}
        
        schedule = {}
        today = datetime.date.today()

        for i, topic in enumerate(self.syllabus):
            gap_days = i % days_remaining
            study_date = today + datetime.timedelta(days=gap_days)
            schedule.setdefault(study_date, []).append(topic)
        
        return schedule
    
    def build_task(self):
        schedule = self.generate_schedule()
        self.tasks = []
        for date, topics in schedule.items():
            for topic in topics:
                self.tasks.append({"topic": topic, "date": date, "status": "pending"})
    def make_done(self, topic_name):
        for task in self.tasks:
            if task["topic"] == topic_name:
                task["status"] = "task completed"


cracker = ExamCrackerAI()
cracker.setup_exam(exam_name, date_str, syllabus, hours)
cracker.build_task()
for task in cracker.tasks:
    print(f"{task['topic']} - {task['date']} - {task['status']}")

