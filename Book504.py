import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["booksDB"]   # Database name
collection = db["books"] # Collection name

# Insert Data
def insert_data():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    price = entry_price.get()

    if title and author and year and price:
        book = {"title": title, "author": author, "year": year, "price": price}
        collection.insert_one(book)
        messagebox.showinfo("Success", "Book Added Successfully!")
        fetch_data()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Fetch Data
def fetch_data():
    listbox.delete(0, tk.END)
    for book in collection.find():
        listbox.insert(tk.END, f"{book['_id']} | {book['title']} | {book['author']} | {book['year']} | ₹{book['price']}")

# Delete Data
def delete_data():
    selected = listbox.get(tk.ACTIVE)
    if selected:
        book_id = selected.split(" | ")[0]
        collection.delete_one({"_id": ObjectId(book_id)})
        messagebox.showinfo("Deleted", "Book Deleted Successfully!")
        fetch_data()
    else:
        messagebox.showwarning("Selection Error", "Please select a book to delete")

# Update Data
def update_data():
    selected = listbox.get(tk.ACTIVE)
    if selected:
        book_id = selected.split(" | ")[0]
        new_title = entry_title.get()
        new_author = entry_author.get()
        new_year = entry_year.get()
        new_price = entry_price.get()

        if new_title and new_author and new_year and new_price:
            collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": {"title": new_title, "author": new_author, "year": new_year, "price": new_price}}
            )
            messagebox.showinfo("Updated", "Book Updated Successfully!")
            fetch_data()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")
    else:
        messagebox.showwarning("Selection Error", "Please select a book to update")

# GUI Setup
root = tk.Tk()
root.title("📚 Books Management System")
root.geometry("650x500")

# Labels and Entries
tk.Label(root, text="Book Title").pack()
entry_title = tk.Entry(root)
entry_title.pack()

tk.Label(root, text="Author").pack()
entry_author = tk.Entry(root)
entry_author.pack()

tk.Label(root, text="Year").pack()
entry_year = tk.Entry(root)
entry_year.pack()

tk.Label(root, text="Price").pack()
entry_price = tk.Entry(root)
entry_price.pack()

# Buttons
tk.Button(root, text="Add Book", command=insert_data).pack(pady=5)
tk.Button(root, text="Update Book", command=update_data).pack(pady=5)
tk.Button(root, text="Delete Book", command=delete_data).pack(pady=5)
tk.Button(root, text="Refresh", command=fetch_data).pack(pady=5)

# Listbox
listbox = tk.Listbox(root, width=80, height=15)
listbox.pack(pady=10)

fetch_data()
root.mainloop()