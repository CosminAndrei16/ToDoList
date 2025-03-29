import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:5000/todos"

def refresh_list():
    listbox.delete(0, tk.END)
    response = requests.get(API_URL)
    todos = response.json()

    for todo in todos:
        status = "[✓]" if todo["completed"] else "[ ]"
        listbox.insert(tk.END, f"{status} {todo['text']} (ID: {todo['id']})")

def add_task():
    text = entry.get()
    if text:
        requests.post(API_URL, json={"text": text})
        entry.delete(0, tk.END)
        refresh_list()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def toggle_task():
    try:
        selected = listbox.get(listbox.curselection())
        task_id = int(selected.split("(ID: ")[1].split(")")[0])
        requests.put(f"{API_URL}/{task_id}")
        refresh_list()
    except:
        messagebox.showwarning("Warning", "Please select a task!")

def delete_task():
    try:
        selected = listbox.get(listbox.curselection())
        task_id = int(selected.split("(ID: ")[1].split(")")[0])
        requests.delete(f"{API_URL}/{task_id}")
        refresh_list()
    except:
        messagebox.showwarning("Warning", "Please select a task!")

app = tk.Tk()
app.title("To-Do List")

entry = tk.Entry(app, width=40)
entry.pack()

btn_add = tk.Button(app, text="Add Task", command=add_task)
btn_add.pack()

listbox = tk.Listbox(app, width=50, height=10)
listbox.pack()

btn_complete = tk.Button(app, text="Mark as Complete", command=toggle_task)
btn_complete.pack()

btn_delete = tk.Button(app, text="Delete Task", command=delete_task)
btn_delete.pack()

refresh_list()

app.mainloop()
