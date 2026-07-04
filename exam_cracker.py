import datetime 
class ExamCrackerAI:
        
        def __init__(self):
            self.exam_name = ""
            self.exam_date = None
            self.syllabus = []
            self.hours_per_day = 0

        def setup_exam(self, exam_name, exam_date_str, syllabus, hours_per_day):
            self.exam_name = exam_name
            self.exam_date = datetime.datetime.strptime(exam_date_str, "%Y-%m-%d").date()
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
                study_date = today + datetime.timedelta(days=gap_days)
                schedule.setdefault(study_date, []).append(topic)
            
            return schedule
        
        def build_task(self):
            self.tasks = []
            schedule = self.generate_schedule()
            total_minutes = self.hours_per_day * 60
            learn_minutes = total_minutes // 2
            practice_minutes = total_minutes - learn_minutes

            for date, topics in schedule.items():
                for topic in topics:
                    self.tasks.append({
                         "topic": f"{topic} - Learn", 
                         "date": date, 
                         "status": "pending",
                         "minutes": learn_minutes
                         })
                    self.tasks.append({
                         "topic": f"{topic} - Practice",
                         "date": date,
                         "status": "pending",
                         "minutes": practice_minutes
                    })

            self.add_revision_day()
                
        def add_revision_day(self):
            revision_date = self.exam_date - datetime.timedelta(days=1)
            total_minutes = self.hours_per_day * 60
            per_topic_minutes = total_minutes // max(1, len(self.syllabus))
            for topic in self.syllabus:
                self.tasks.append({
                    "topic": f"Rapid Revision: {topic}",
                    "date": revision_date,
                    "status": "pending",
                    "minutes": per_topic_minutes
                })    
        def make_done(self, topic_name):
            for task in self.tasks:
                if task["topic"] == topic_name:
                    task["status"] = "task completed"
#imputs by the user
if __name__ == "__main__":
    exam_name = input("Oh no ! Exam came to trouble you ! Don't worry let me relive some stress, tell me the name of the exam: ")
    date_str = input("So.. When is this EXAM ? (YYYY.MM.DD) :")
    syllabus_entry = input("Please enter the syllabus topics, separated by commas: ")
    syllabus = []
    for topic in syllabus_entry.split(","):
        syllabus.append(topic.strip())
    hours = int(input("Well.. If i ask you how many hours per day you can study, what would be your answer ? :"))

    cracker = ExamCrackerAI()
    cracker.setup_exam(exam_name, date_str, syllabus, hours)
    cracker.build_task()
    for task in cracker.tasks:
        print(f"{task['topic']} - {task['date']} - {task['status']}")
#loop to keep user indulged
    while True:
                action = input(" If you want to see the (current task list) type- Show," \
                " If you want to (mark a task done) type- Done, " \
                "If you want to (exit) type- Exit : ")
                if action == "Show" :
                    for task in cracker.tasks:
                        print(f"{task['topic']} - {task['date']} - {task['status']}")
                elif action == "Done" :
                    topic_name = input("Enter the exact topic name that you entered before and now you got rid of !! : ")
                    cracker.make_done(topic_name)

                elif action == "Exit" :
                    print("Wish you the best for the exam, Go break a leg !! BYIEE !")
                    break
                else:
                    print("I didn't get that — try Show, Done, or Exit.") 



