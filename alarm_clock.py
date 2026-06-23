import tkinter as tk
from tkinter import messagebox
import datetime
import threading
import time

# Function to check alarm
def alarm():
    alarm_time = entry.get()

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        if current_time == alarm_time:
            messagebox.showinfo("Alarm", "Wake Up! Alarm Time Reached!")
            break

        time.sleep(1)

# Start alarm thread
def start_alarm():
    threading.Thread(target=alarm, daemon=True).start()
    messagebox.showinfo("Success", "Alarm Set Successfully!")

# Update digital clock
def update_clock():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    root.after(1000, update_clock)

# Main Window
root = tk.Tk()
root.title("Alarm Clock")
root.geometry("500x300")
root.config(bg="#E8F6F3")

title = tk.Label(
    root,
    text="Alarm Clock",
    font=("Arial", 20, "bold"),
    bg="#E8F6F3",
    fg="darkblue"
)
title.pack(pady=10)

clock_label = tk.Label(
    root,
    text="",
    font=("Arial", 30, "bold"),
    bg="#E8F6F3",
    fg="green"
)
clock_label.pack(pady=10)

tk.Label(
    root,
    text="Enter Alarm Time (HH:MM:SS)",
    font=("Arial", 12),
    bg="#E8F6F3"
).pack()

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

btn = tk.Button(
    root,
    text="Set Alarm",
    font=("Arial", 12),
    bg="blue",
    fg="white",
    command=start_alarm
)
btn.pack(pady=10)

update_clock()

root.mainloop()
