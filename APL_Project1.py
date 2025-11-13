import tkinter as tk
from tkinter import messagebox
from plyer import notification
import threading
import time
from datetime import datetime

reminders = []

def add_reminder():
    name = med_name_entry.get().strip()
    time_str = med_time_entry.get().strip()

    if not name or not time_str:
        messagebox.showwarning("Input Error", "Please enter both medicine name and time (HH:MM).")
        return
    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        messagebox.showerror("Invalid Time", "Please enter time in 24-hour format (HH:MM).")
        return

    reminders.append({"name": name, "time": time_str})
    update_reminder_list()

    med_name_entry.delete(0, tk.END)
    med_time_entry.delete(0, tk.END)
    messagebox.showinfo("Success", f"Reminder set for {name} at {time_str}")

def update_reminder_list():
    reminder_list.delete(0, tk.END)
    for med in reminders:
        reminder_list.insert(tk.END, f"{med['time']} - {med['name']}")

def show_notification(med_name):
    notification.notify(
        title="💊 Medicine Reminder",
        message=f"It's time to take your {med_name}",
        timeout=10
    )

def check_reminders():
    while True:
        now = datetime.now().strftime("%H:%M")
        for med in reminders:
            if med["time"] == now:
                show_notification(med["name"])
                time.sleep(60)  
        time.sleep(10)
root = tk.Tk()
root.title("💊 Medicine Reminder App")
root.geometry("400x400")
root.config(bg="#f0f4f7")

tk.Label(root, text="Medicine Reminder", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#333").pack(pady=10)

tk.Label(root, text="Medicine Name:", bg="#f0f4f7").pack()
med_name_entry = tk.Entry(root, width=30)
med_name_entry.pack(pady=5)

tk.Label(root, text="Time (24-hour format HH:MM):", bg="#f0f4f7").pack()
med_time_entry = tk.Entry(root, width=30)
med_time_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Reminder", command=add_reminder, bg="#4CAF50", fg="white", width=20)
add_button.pack(pady=10)

tk.Label(root, text="Scheduled Reminders:", bg="#f0f4f7").pack()
reminder_list = tk.Listbox(root, width=40, height=8)
reminder_list.pack(pady=10)

threading.Thread(target=check_reminders, daemon=True).start()

root.mainloop()