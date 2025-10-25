from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
import sqlite3 

app = FastAPI() 
# Modelo de datos 
class Employee(BaseModel): 
    name: str 
    position: str = None 
    salary: float = None 
# Conexión a SQLite 
def get_db(): 
    conn = sqlite3.connect('employees.db') 
    conn.execute('''CREATE TABLE IF NOT EXISTS employees 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT NOT NULL, 
                     position TEXT, 
                     salary REAL)''') 
    return conn 
# CRUD Endpoints 
@app.post("/employees/") 
def create_employee(employee: Employee): 
    conn = get_db() 
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", 
                   (employee.name, employee.position, employee.salary)) 
    conn.commit() 
    return {"id": cursor.lastrowid} 
@app.get("/employees/{employee_id}") 
def read_employee(employee_id: int): 
    conn = get_db() 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,)) 
    row = cursor.fetchone() 
    if row is None: 
        raise HTTPException(status_code=404, detail="Employee not found") 
    return {"id": row[0], "name": row[1], "position": row[2], "salary": row[3]} 
@app.put("/employees/{employee_id}") 
def update_employee(employee_id: int, employee: Employee): 
    conn = get_db() 
    cursor = conn.cursor() 
    cursor.execute("UPDATE employees SET name=?, position=?, salary=? WHERE id=?", 
                   (employee.name, employee.position, employee.salary, employee_id)) 
    conn.commit() 
    if cursor.rowcount == 0: 
        raise HTTPException(status_code=404, detail="Employee not found") 
    return {"message": "Employee updated"} 

@app.delete("/employees/{employee_id}") 
def delete_employee(employee_id: int): 
    conn = get_db() 
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,)) 
    conn.commit() 
    if cursor.rowcount == 0: 
        raise HTTPException(status_code=404, detail="Employee not found") 
    return {"message": "Employee deleted"} 

if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)