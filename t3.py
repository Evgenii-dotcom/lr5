from flask import Flask, render_template


class Student:
    def __init__(self, id, name, age, grade, faculty):
        self.id = id
        self.name = name
        self.age = age
        self.grade = grade
        self.faculty = faculty


class University:
    def __init__(self, name, founded, departments, location):
        self.name = name
        self.founded = founded
        self.departments = departments
        self.location = location


class StudentService:
    def get_students(self):
        data = [
            Student(1, "Алексей Петров", 20, 4.5, "Информатика"),
            Student(2, "Екатерина Сидорова", 19, 4.8, "Математика"),
            Student(3, "Дмитрий Иванов", 21, 4.2, "Физика"),
            Student(4, "Ольга Козлова", 20, 4.9, "Информатика"),
            Student(5, "Михаил Смирнов", 22, 4.1, "Математика"),
        ]
        return data


class UniversityService:
    def get_info(self):
        return University(
            "Технический Университет",
            1950,
            ["Информатика", "Математика", "Физика", "Химия"],
            "Москва"
        )


student_service = StudentService()
university_service = UniversityService()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("t1.html")


@app.route("/students")
def students():
    return render_template(
        "t3.html",
        students=student_service.get_students(),
        university=university_service.get_info(),
        title="Список студентов"
    )


if __name__ == "__main__":
    app.run(debug=True)
