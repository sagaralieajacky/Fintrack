import tkinter as tk 
from tkinter import ttk, messagebox 
from tkinter.filedialog import asksaveasfilename 
from datetime import datetime 
import csv 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
 
data = [] 
categories = ["Food", "Travel", "Utilities", "Shopping", "Others"] 
 
def add_expense(): 
    date = date_entry.get() 
    category = category_var.get() 
    amount = amount_entry.get() 
    description = description_entry.get() 
 
    if not date or not category or not amount: 
        messagebox.showwarning("Input Error", "Please fill all fields.") 
        return 
 
    try: 
        amount = float(amount)  
    except ValueError: 
        messagebox.showerror("Invalid Amount", "Enter a valid number for amount.") 
        return 
 
    data.append([date, category, amount, description]) 
    update_summary() 
    update_chart() 
    clear_inputs() 
 
def clear_inputs(): 
    category_var.set("") 
    amount_entry.delete(0, tk.END) 
    description_entry.delete(0, tk.END) 
 
def update_summary(): 
    if not data: 
        total_label.config(text="₹0.00") 
        avg_label.config(text="₹0.00") 
        high_label.config(text="₹0.00") 
        entries_label.config(text="0") 
        return 
 
    amounts = [entry[2] for entry in data] 
    total = sum(amounts) 
    avg = total / len(amounts) 
    high = max(amounts) 
 
    total_label.config(text=f"₹{total:.2f}") 
    avg_label.config(text=f"₹{avg:.2f}") 
    high_label.config(text=f"₹{high:.2f}") 
    entries_label.config(text=str(len(data))) 
 
def export_data(): 
    if not data: 
        messagebox.showinfo("No Data", "Nothing to export.") 
        return 
 
    file_path = asksaveasfilename(defaultextension=".csv", 
                                   filetypes=[("CSV files", "*.csv")]) 
    if not file_path: 
        return 
 
    with open(file_path, mode='w', newline='', encoding='utf-8') as file: 
        writer = csv.writer(file) 
        writer.writerow(["Date", "Category", "Amount", "Description"]) 
        for row in data: 
            writer.writerow([row[0], row[1], f"{row[2]:.2f}", row[3]]) 
 
 
 
    messagebox.showinfo("Exported", "Data exported successfully in clean table 
format!") 
 
def update_chart(): 
    for widget in chart_frame.winfo_children(): 
        widget.destroy() 
 
    if not data: 
        tk.Label(chart_frame, text="No data to display.", bg="#1e1e2e", 
fg="white").pack() 
        return 
 
    category_totals = {} 
    for _, cat, amt, _ in data: 
        category_totals[cat] = category_totals.get(cat, 0) + amt 
 
    fig, ax = plt.subplots(figsize=(4.5, 3), dpi=100) 
    ax.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%') 
    ax.set_title("Expense Distribution") 
    fig.patch.set_facecolor('#1e1e2e') 
 
    canvas = FigureCanvasTkAgg(fig, master=chart_frame) 
    canvas.draw() 
    canvas.get_tk_widget().pack() 
root = tk.Tk() 
root.title("FinTrack - Smart Personal Expense Tracker") 
root.geometry("980x680") 
root.configure(bg="#1e1e2e") 
style = ttk.Style() 
style.theme_use('clam') 
style.configure("TLabel", background="#1e1e2e", foreground="white", font=("Segoe 
UI", 12)) 
style.configure("TButton", font=("Segoe UI", 10)) 
style.configure("TEntry", font=("Segoe UI", 10)) 
style.configure("TCombobox", font=("Segoe UI", 10)) 
title_frame = tk.Frame(root, bg="#1e1e2e") 
title_frame.pack(pady=10) 
title = tk.Label(title_frame, text="FinTrack\nSmart Personal Expense Tracker", 
font=("Segoe UI", 22, "bold"), fg="#f0a500", bg="#1e1e2e") 
title.pack(anchor="center") 
summary_frame = tk.Frame(root, bg="#1e1e2e") 
summary_frame.pack(pady=10) 
FinTrack:Smart Personal Expense Tracker 
PAGE 20 
 
 
summary_labels = [ 
    ("Total Expense", "₹0.00"), 
    ("Average Expense", "₹0.00"), 
    ("Highest Expense", "₹0.00"), 
    ("Entries Expense", "0") 
] 
 
summary_values = [] 
 
for i, (label_text, value_text) in enumerate(summary_labels): 
    frame = tk.Frame(summary_frame, bg="#2e2e3e", padx=15, pady=10) 
    frame.grid(row=0, column=i, padx=10) 
    tk.Label(frame, text=label_text, bg="#2e2e3e", fg="white", font=("Segoe UI", 
11)).pack() 
    value_label = tk.Label(frame, text=value_text, bg="#2e2e3e", fg="#00ff99", 
font=("Segoe UI", 13, "bold")) 
    value_label.pack() 
    summary_values.append(value_label) 
 
total_label, avg_label, high_label, entries_label = summary_values 
 
category_var = tk.StringVar() 
 
 
add_frame = tk.LabelFrame(root, text="Add New Expense", bg="#1e1e2e", 
fg="white", font=("Segoe UI", 13, "bold")) 
add_frame.pack(padx=20, pady=10, fill="x") 
 
left_form = tk.Frame(add_frame, bg="#1e1e2e") 
left_form.grid(row=0, column=0, padx=20, pady=10, sticky="w") 
 
form_items = [ 
    ("Date:", tk.Entry), 
    ("Category:", ttk.Combobox), 
    ("Amount (₹):", tk.Entry), 
    ("Description:", tk.Entry) 
] 
 
widgets = {} 
 
for i, (label_text, widget_type) in enumerate(form_items): 
    tk.Label(left_form, text=label_text, bg="#1e1e2e", fg="white").grid(row=i, 
column=0, sticky="w", pady=6) 
    if widget_type == tk.Entry: 
        entry = ttk.Entry(left_form, width=30) 
    elif widget_type == ttk.Combobox: 
        entry = ttk.Combobox(left_form, textvariable=category_var, values=categories, 
state="readonly", width=28) 
entry.grid(row=i, column=1, pady=6) 
widgets[label_text] = entry 
widgets["Date:"].insert(0, datetime.now().strftime("%d/%m/%Y")) 
date_entry = widgets["Date:"] 
amount_entry = widgets["Amount (₹):"] 
description_entry = widgets["Description:"] 
add_btn = ttk.Button(left_form, text="Add Expense", command=add_expense) 
add_btn.grid(row=4, column=1, pady=10, sticky="e") 
overview_frame = tk.LabelFrame(root, text="Expense Overview", bg="#1e1e2e", 
fg="white", font=("Segoe UI", 13, "bold")) 
overview_frame.pack(padx=20, pady=10, fill="both", expand=True) 
export_btn = ttk.Button(overview_frame, text="Export Data", command=export_data) 
export_btn.pack(pady=5) 
chart_frame = tk.Frame(overview_frame, bg="#1e1e2e") 
chart_frame.pack(pady=10) 
root.mainloop() 
