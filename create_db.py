import sqlite3

con = sqlite3.connect("employee.db")
print("Database opened successfully")

con.execute(
    """create table Employees (id INTEGER PRIMARY KEY, emp_name TEXT NOT NULL, emp_dept TEXT 
    NOT NULL, emp_desig TEXT NOT NULL, emp_salary INTEGER NOT NULL, emp_grade TEXT NOT NULL,
    emp_work_loc TEXT NOT NULL, emp_bonus INTEGER NOT NULL) 
    """)

print("Table created successfully")

con.close()

