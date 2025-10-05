from tkinter import *
from tkinter import ttk, messagebox
import json

# ----------------- MAIN WINDOW -----------------
top = Tk()
top.geometry("700x500")
top.title("Sales Management")

# ----------------- VARIABLES -----------------
name_var = StringVar()
qty_var = StringVar()
price_var = StringVar()
search_var = StringVar()

# ----------------- FUNCTIONS -----------------
def add_item():
    name = name_var.get().strip()
    qty = qty_var.get().strip()
    price = price_var.get().strip()

    if not name or not qty or not price:
        messagebox.showwarning("Warning", "Please fill all fields before adding!")
        return

    tree.insert("", "end", values=(name, qty, price))
    name_var.set("")
    qty_var.set("")
    price_var.set("")

def delete_item():
    selected = tree.selection()
    if selected:
        tree.delete(selected)   # ❌ Original: you tried to use tree.item() instead of tree.delete()
    else:
        messagebox.showwarning("Warning", "Select item to delete")

def update_item():
    selected = tree.selection()
    if selected:
        if not name_var.get() or not qty_var.get() or not price_var.get():
            messagebox.showwarning("Warning", "Fill all fields to update!")
            return
        tree.item(selected, values=(name_var.get(), qty_var.get(), price_var.get()))
    else:
        messagebox.showwarning("Warning", "Select item to update")

def show_item(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected, "values")
        name_var.set(values[0])
        qty_var.set(values[1])
        price_var.set(values[2])

def save_data():
    data = [tree.item(i, "values") for i in tree.get_children()]
    with open("products.json", "w") as f:
        json.dump(data, f)
    messagebox.showinfo("Saved", "Data saved successfully!")

def load_data():
    try:
        with open("products.json", "r") as f:
            data = json.load(f)
        tree.delete(*tree.get_children())
        for item in data:
            tree.insert("", "end", values=item)
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved file found")
def search_item():
    search_text = search_var.get().strip().lower()
    tree.delete(*tree.get_children())  # Clear current display

    try:
        with open("products.json", "r") as f:
            data = json.load(f)
        for item in data:
            # Check if product name contains the search text
            if search_text in item[0].lower():
                tree.insert("", "end", values=item)
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved file found")

# ----------------- LABELS & ENTRY -----------------
Label(top, text="Product Name:", font=("Arial", 10, "bold")).place(x=50, y=50)
Entry(top, width=50, bd=5, textvariable=name_var).place(x=200, y=50)

Label(top, text="Quantity:", font=("Arial", 10, "bold")).place(x=50, y=100)
Entry(top, width=50, bd=5, textvariable=qty_var).place(x=200, y=100)

Label(top, text="Price:", font=("Arial", 10, "bold")).place(x=50, y=150)
Entry(top, width=50, bd=5, textvariable=price_var).place(x=200, y=150)
Label(top, text="Search:", font=("Arial", 10, "bold")).place(x=50, y=270)
Entry(top, width=50, font=("Arial", 10, "bold"), bd=5, textvariable=search_var).place(x=120, y=270)

# ----------------- BUTTONS -----------------
Button(top, text="Add Item", width=15, bg="green", fg="white", command=add_item).place(x=10, y=200)
Button(top, text="Update Item", width=15, bg="blue", fg="white", command=update_item).place(x=160, y=200)
Button(top, text="Delete Item", width=15, bg="red", fg="white", command=delete_item).place(x=310, y=200)
Button(top, text="Save", width=15, bg="lightgreen", fg="black", command=save_data).place(x=460, y=200)
Button(top, text="Load", width=15, bg="lightblue", fg="black", command=load_data).place(x=10, y=230)
Button(top, text="Search", width=15, bg="yellow", fg="black", command=search_item).place(x=500, y=270)

# ----------------- TREEVIEW -----------------
tree = ttk.Treeview(top, columns=("Name", "Quantity", "Price"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Quantity", text="Quantity")
tree.heading("Price", text="Price")

tree.column("Name", width=200)
tree.column("Quantity", width=100)
tree.column("Price", width=100)

tree.place(x=30, y=300, width=650, height=150)

# ----------------- BIND -----------------
tree.bind("<ButtonRelease-1>", show_item)

top.mainloop()
