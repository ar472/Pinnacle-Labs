import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import datetime

# Function to display calendar
def show_calendar():
    year = int(year_entry.get())
    month = int(month_entry.get())

    cal = calendar.month(year, month)

    calendar_text.delete("1.0", tk.END)
    calendar_text.insert(tk.END, cal)

# Function to save reminder
def save_reminder():
    date = date_entry.get()
    reminder = reminder_entry.get()

    if date == "" or reminder == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    with open("reminders.txt", "a") as file:
        file.write(f"{date} - {reminder}\n")

    messagebox.showinfo("Success", "Reminder Saved!")

    date_entry.delete(0, tk.END)
    reminder_entry.delete(0, tk.END)

# Function to view reminders
def view_reminders():
    try:
        with open("reminders.txt", "r") as file:
            data = file.read()

        reminder_window = tk.Toplevel(root)
        reminder_window.title("All Reminders")
        reminder_window.geometry("500x400")

        text = tk.Text(reminder_window)
        text.pack(fill="both", expand=True)

        text.insert(tk.END, data)

    except FileNotFoundError:
        messagebox.showinfo("Info", "No reminders found!")

# Main Window
root = tk.Tk()
root.title("Calendar and Reminder App")
root.geometry("700x600")
root.config(bg="#f0f8ff")

# Heading
title = tk.Label(
    root,
    text="Calendar & Reminder App",
    font=("Arial", 20, "bold"),
    bg="#f0f8ff",
    fg="darkblue"
)
title.pack(pady=10)

# Calendar Section
frame1 = tk.Frame(root, bg="#f0f8ff")
frame1.pack(pady=10)

tk.Label(frame1, text="Year:", bg="#f0f8ff").grid(row=0, column=0)

year_entry = tk.Entry(frame1, width=10)
year_entry.grid(row=0, column=1, padx=5)
year_entry.insert(0, datetime.now().year)

tk.Label(frame1, text="Month:", bg="#f0f8ff").grid(row=0, column=2)

month_entry = tk.Entry(frame1, width=10)
month_entry.grid(row=0, column=3, padx=5)
month_entry.insert(0, datetime.now().month)

tk.Button(
    frame1,
    text="Show Calendar",
    command=show_calendar,
    bg="green",
    fg="white"
).grid(row=0, column=4, padx=10)

calendar_text = tk.Text(root, height=10, width=50, font=("Courier", 12))
calendar_text.pack(pady=10)

# Reminder Section
tk.Label(
    root,
    text="Set Reminder",
    font=("Arial", 14, "bold"),
    bg="#f0f8ff"
).pack()

frame2 = tk.Frame(root, bg="#f0f8ff")
frame2.pack(pady=10)

tk.Label(frame2, text="Date (DD-MM-YYYY):", bg="#f0f8ff").grid(row=0, column=0)

date_entry = tk.Entry(frame2, width=20)
date_entry.grid(row=0, column=1)

tk.Label(frame2, text="Reminder:", bg="#f0f8ff").grid(row=1, column=0)

reminder_entry = tk.Entry(frame2, width=30)
reminder_entry.grid(row=1, column=1)

tk.Button(
    root,
    text="Save Reminder",
    command=save_reminder,
    bg="blue",
    fg="white"
).pack(pady=5)

tk.Button(
    root,
    text="View Reminders",
    command=view_reminders,
    bg="orange",
    fg="black"
).pack(pady=5)

show_calendar()

root.mainloop()
