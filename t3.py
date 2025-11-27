from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("t1.html")

@app.route("/students")
def students():
    students_data = [
        {"id": 1, "name": "Алексей Петров", "age": 20, "grade": 4.5, "faculty": "Информатика"},
        {"id": 2, "name": "Екатерина Сидорова", "age": 19, "grade": 4.8, "faculty": "Математика"},
        {"id": 3, "name": "Дмитрий Иванов", "age": 21, "grade": 4.2, "faculty": "Физика"},
        {"id": 4, "name": "Ольга Козлова", "age": 20, "grade": 4.9, "faculty": "Информатика"},
        {"id": 5, "name": "Михаил Смирнов", "age": 22, "grade": 4.1, "faculty": "Математика"}
    ]
    
    university_info = {
        "name": "Технический Университет",
        "founded": 1950,
        "departments": ["Информатика", "Математика", "Физика", "Химия"],
        "location": "Москва"
    }
    
    return render_template(
        "t3.html",
        students=students_data,
        university=university_info,
        title="Список студентов"
    )

if __name__ == "__main__":
    app.run(debug=True)