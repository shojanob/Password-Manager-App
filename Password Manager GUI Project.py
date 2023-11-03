from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ------------------------------------------ SEARCH DATA ------------------------------------------------------- #
def find_password():
    user_website = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Data file not found", message="Sorry, the data file you're looking for was not found.")
    else:
        if user_website in data:
            email = data[user_website]["email"]
            password = data[user_website]["password"]
            messagebox.showinfo(title=f"Your information from {user_website}", message=f"Website: {user_website}\n"
                                                                                       f"Email: {email}\n "
                                                                                       f"Password: {password}")
        else:
            messagebox.showerror(title="Details Not Found", message="No details for the website exists.")
    finally:
        website_input.delete(0,END)

# ----------------------------------------- PASSWORD GENERATOR ------------------------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------------------- SAVE PASSWORD --------------------------------------------------------- #
def save():
    website = website_input.get()
    email_user = email_user_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email_user,
            "password": password,
                }
    }

    if len(website) == 0 or len(password) == 0 or len(email_user) == 0:
        messagebox.showwarning(title="Error", message="You must fill in the empty fields to save onto password manager!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading JSON data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Saving updated data
            data.update(new_data)

            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            email_user_input.delete(0,END)
            password_input.delete(0,END)


# --------------------------------------------- UI SETUP ---------------------------------------------------------- #


window = Tk()
window.title("Shoh's Password Manager")
window.config(padx=30, pady=50)
window.minsize(width=600, height=600)

canvas = Canvas(width=300, height=300, highlightthickness=0)
lock_image = PhotoImage(file="blue_lock.png")
canvas.create_image(150, 150, image=lock_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=("Arial", 14, "normal"), pady=10)
email_user_label = Label(text="Email/Username:", font=("Arial", 14, "normal"),pady=10)
password_label = Label(text="Password:", font=("Arial", 14, "normal"), pady=10)

website_label.grid(column=0, row=2)
email_user_label.grid(column=0, row=3)
password_label.grid(column=0,row=4)

# Entries
website_input = Entry(width=35)
email_user_input = Entry(width=35)
password_input = Entry(width=21)

website_input.grid(column=1,row=2, columnspan=2)
website_input.focus()
email_user_input.grid(column=1, row=3, columnspan=2)
password_input.grid(column=1,row=4)

# Buttons
generate_pass_button = Button(text="Generate Password", highlightthickness=0, command=generate_password)
add_button = Button(text="Add", highlightthickness=0, width=36, command=save)
search_button = Button(text="Search", highlightthickness=0, command=find_password)

generate_pass_button.grid(column=3,row=4)
add_button.grid(column=1,row=5, columnspan=2)
search_button.grid(column=2,row=2)


window.mainloop()