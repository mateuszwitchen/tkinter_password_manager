import tkinter as tk
import random
import json
from PIL import Image, ImageTk
import hashlib
import requests

# Functions
# ---------------------------------------------------------------------

def read_password():
    def close(window):
        window.destroy()

    def read_action():
        def read_json(website_name):
            try:
                with open('passwords.json', 'r') as file:
                    data = json.load(file)
                    for item in data:
                        if item.get('website') == website_name:
                            password = item.get('password')
                            return password if password else None
            except FileNotFoundError:
                print("File not found!")
            except json.JSONDecodeError:
                print("JSON decoding error!")

        website = str(website_field.get("1.0", "end-1c")).strip()
        result_window = tk.Tk()
        result_window.title(f"Password for: {website}")
        result_window.geometry("400x150")

        password_label = tk.Label(result_window, text=str(read_json(website)), font=("Arial", 30))
        password_label.pack()

        close_button = tk.Button(result_window, text="Close", command=lambda: close(result_window))
        close_button.place(x=150, y=50)

    window = tk.Tk()
    window.title("Read Password")
    window.geometry("400x200")

    prompt = tk.Label(window, text="Website:", font=("Arial", 25))
    prompt.place(x=10, y=50)

    website_field = tk.Text(window, font=("Arial", 20))
    website_field.place(x=200, y=55, width=200, height=30)

    read_button = tk.Button(window, text="Check", command=read_action)
    read_button.place(x=150, y=100)

    close_button = tk.Button(window, text="Close", command=lambda: close(window))
    close_button.place(x=150, y=130)

def save_password():
    def close():
        window.destroy()

    def save_json(password, website):
        try:
            with open("passwords.json", "r") as json_file:
                all_passwords = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_passwords = []

        all_passwords.append({"website": website, "password": password})

        with open("passwords.json", "w") as json_file:
            json.dump(all_passwords, json_file, indent=4)

    window = tk.Tk()
    window.geometry("400x300")

    label1 = tk.Label(window, text="Website", font=('Arial', 24))
    label1.place(x=80, y=50)

    website_field = tk.Text(window, font=('Arial', 24))
    website_field.place(x=180, y=50, width=200, height=35)

    label2 = tk.Label(window, text="Password", font=('Arial', 24))
    label2.place(x=80, y=100)

    password_field = tk.Text(window, font=('Arial', 24))
    password_field.place(x=180, y=100, width=200, height=35)

    def save_and_close():
        website = str(website_field.get("1.0", "end-1c")).strip()
        password = str(password_field.get("1.0", "end-1c")).strip()

        if website and password:
            save_json(password, website)
            close()
        else:
            print("Please fill in both fields")

    save_button = tk.Button(window, text="Save", command=save_and_close)
    save_button.place(x=200, y=150)

    window.mainloop()

def password_checker():
    def check_online(password):
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        url = "https://api.pwnedpasswords.com/range/" + sha1_hash[:5]

        try:
            response = requests.get(url)
            response.raise_for_status()
            hashes = response.text.splitlines()

            remaining_hash = sha1_hash[5:]

            for line in hashes:
                if line.split(":")[0] == remaining_hash:
                    return True
            return False
        except requests.RequestException:
            print("Connection error")
            return False

    def generate_password():
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        symbols = "!@#$%^&*"
        password = ''.join(random.choices(chars + symbols + "0123456789", k=15))
        return password

    def save_extended(password):
        def close():
            window.destroy()

        def save_json(password, website):
            try:
                with open("passwords.json", "r") as json_file:
                    all_passwords = json.load(json_file)
            except (FileNotFoundError, json.JSONDecodeError):
                all_passwords = []

            all_passwords.append({"website": website, "password": password})

            with open("passwords.json", "w") as json_file:
                json.dump(all_passwords, json_file, indent=4)

        def save_and_close():
            website = website_field.get("1.0", "end-1c").strip()
            if website:
                save_json(password, website)
                close()
            else:
                print("Please enter a website")

        window = tk.Tk()
        window.geometry("400x300")
        window.title("Save Password")

        label1 = tk.Label(window, text="Website", font=('Arial', 24))
        label1.place(x=80, y=50)

        website_field = tk.Text(window, font=('Arial', 24))
        website_field.place(x=180, y=50, width=200, height=35)

        label2 = tk.Label(window, text="Password", font=('Arial', 24))
        label2.place(x=80, y=100)

        password_label = tk.Label(window, text=password, font=('Arial', 24))
        password_label.place(x=180, y=100)

        save_button = tk.Button(window, text="Save", command=save_and_close)
        save_button.place(x=200, y=150)

        window.mainloop()

    def verify():
        entered_password = password_input.get("1.0", "end-1c")
        if check_online(entered_password):
            result_label.config(text="Your password is compromised!", fg="red")
            generate_button.pack()
        else:
            result_label.config(text="Your password is safe!", fg="green")

    def generate():
        password = generate_password()
        with open("generated_password.txt", "a") as file:
            file.write(password + "\n")
        result_label.config(text=f"New password generated and saved:\n{password}")
        extended_button.config(command=lambda: save_extended(password))
        extended_button.pack()

    window = tk.Tk()
    window.geometry("400x300")
    window.title("Password Checker")

    prompt = tk.Label(window, text="Enter your password:", font=('Arial', 16))
    prompt.pack()

    password_input = tk.Text(window, font=('Arial', 16), height=1)
    password_input.pack()

    check_button = tk.Button(window, text="Check", command=verify)
    check_button.pack()

    result_label = tk.Label(window, font=('Arial', 14))
    result_label.pack()

    generate_button = tk.Button(window, text="Generate Strong Password", command=generate)
    extended_button = tk.Button(window, text="Extended Save")

    window.mainloop()

# Main Menu
# ---------------------------------------------------------------------
main = tk.Tk()
main.title("Password Manager")
main.geometry("400x600")

welcome = tk.Label(main, text="Choose an option\nto improve your password security!", font=('Arial', 20))
welcome.pack()

check_option = tk.Button(main, text="Check Password Safety", command=password_checker)
check_option.place(x=100, y=120)

save_option = tk.Button(main, text="Extended Save", command=save_password)
save_option.place(x=140, y=150)

read_option = tk.Button(main, text="Read Password", command=read_password)
read_option.place(x=150, y=180)

# image_path = "grafika1.png"
# image = Image.open(image_path)
# resized_image = image.resize((350, 300))
# photo = ImageTk.PhotoImage(resized_image)
# image_label = tk.Label(main, image=photo)
# image_label.place(x=25, y=225)

main.mainloop()
