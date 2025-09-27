class EducationSystem:
    def __init__(self):
        self.courses = {
            "basic": {"cost": 20, "skill_gain": 1.0},
            "advanced": {"cost": 50, "skill_gain": 2.0},
            "professional": {"cost": 100, "skill_gain": 3.0}
        }
        self.enrolled_students = {}
        
    def enroll_student(self, citizen, course_type):
        """Запись гражданина на курс"""
        if course_type in self.courses:
            cost = self.courses[course_type]["cost"]
            if citizen.pp_balance >= cost:
                citizen.pp_balance -= cost
                self.enrolled_students[citizen.id] = {
                    "course": course_type,
                    "progress": 0,
                    "days_remaining": 30
                }
                return True
        return False
        
    def process_education(self, citizens):
        """Обработка образовательного процесса"""
        completed_courses = []
        
        for citizen_id, enrollment in list(self.enrolled_students.items()):
            enrollment["days_remaining"] -= 1
            enrollment["progress"] += 3.33  # 100% за 30 дней
            
            if enrollment["days_remaining"] <= 0:
                # Завершение курса
                citizen = next((c for c in citizens if c.id == citizen_id), None)
                if citizen:
                    skill_gain = self.courses[enrollment["course"]]["skill_gain"]
                    citizen.education_level = min(10, citizen.education_level + skill_gain)
                    citizen.happiness = min(100, citizen.happiness + 10)
                    completed_courses.append(citizen_id)
                    
        # Удаляем завершенные курсы
        for citizen_id in completed_courses:
            del self.enrolled_students[citizen_id]
            
        return len(completed_courses)