from flask import *
import sqlite3

app = Flask(__name__)
id_list = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/emp_menu')
def first_page():
    return render_template('firstpage.html')


@app.route("/addemp")
def add():
    return render_template("addemp.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            id = request.form["id"]
            name = request.form["name"]
            dept = request.form["dept"]
            deisg = request.form["desig"]
            salary = request.form["salary"]
            grade = request.form["grade"]
            work = request.form["status"]
            bonus = request.form["bonus"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("""INSERT into Employees (id, emp_name, emp_dept, emp_desig, emp_salary, emp_grade, 
                            emp_work_loc, emp_bonus) values (?,?,?,?,?,?,?,?)""",
                            (id, name, dept, deisg, salary, grade, work, bonus))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            return render_template("add_status.html", msg=msg)


@app.route("/view")
def view():
    con = sqlite3.connect("employee.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


@app.route("/delete")
def delete():
    return render_template("delemp.html")


@app.route("/deleterecord", methods=["GET"])
def deleterecord():
    id = request.args.get('id')
    print(id)
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            query = """delete from Employees where id = ?"""
            cur.execute(query, (id,))
            con.commit()
            msg = "Record Successfully Deleted"
        except:
            msg = "Can't be deleted"
        finally:
            return render_template("del_status.html", msg=msg)


@app.route("/update")
def update():
    return render_template("update.html")


@app.route("/getid")
def update_id():
    update_id = request.args.get('id')
    print(update_id)
    id_list.append(update_id)
    return render_template("updateemp.html")


@app.route("/updaterecord", methods=["POST", "GET"])
def updaterecord():
    id_update = id_list.pop()
    with sqlite3.connect("employee.db") as con:
        try:
            update_name = request.form['name']
            update_dept = request.form['dept']
            update_desig = request.form['desig']
            update_salary = request.form['salary']
            update_grade = request.form['grade']
            update_work = request.form['status']
            update_bonus = request.form['bonus']
            cur = con.cursor()
            query = """
            update Employees set emp_name = ?, emp_dept = ?, emp_desig = ?, emp_salary = ?, emp_grade = ?,
             emp_work_loc = ?, emp_bonus = ? where id = ?
            """
            columnValues = (update_name, update_dept, update_desig, update_salary, update_grade, update_work, update_bonus, id_update)
            cur.execute(query, columnValues)
            con.commit()
            msg = "Record successfully updated"
        except:
            msg = "Can't be updated"
        finally:
            return render_template("update_status.html", msg=msg)


@app.route('/get')
def get_emp():
    return render_template("get_emp.html")

@app.route('/getemp_status', methods=["GET"])
def emp_details():
    id = request.args.get('id')
    con = sqlite3.connect("employee.db")
    con = con.cursor()
    query = ("""select * from Employees where id=?""")
    con = con.execute(query,(id,))
    rows = con.fetchall()
    msg = ""
    if rows != []:
        msg = "Employee Details....."
    else:
        msg = "Employee Not in the Database......."
    return render_template("get_employee_details.html",msg=msg,rows=rows)






if __name__ == "__main__":
    app.run(debug=True, port=5003)
