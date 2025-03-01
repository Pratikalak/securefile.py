# --------------------------------------- Required Lib --------------------------------------- #
# ---------------------------------------              --------------------------------------- #
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import mysql.connector
import re
import hashlib
import random
from mysql.connector import Error
from tkinter import filedialog
import os
import datetime
import base64
import requests

# Color scheme constants
MAIN_BG = "#FF69B4"  # Hot pink
BUTTON_BG = "#FF1493"  # Deep pink
BUTTON_ACTIVE_BG = "#DB7093"  # Pale violet red
TEXT_COLOR = "white"

ONLINE_FILE_DIR = os.path.join(os.path.dirname(__file__), "online_file")
if not os.path.exists(ONLINE_FILE_DIR):
    os.makedirs(ONLINE_FILE_DIR)

def show_forgot_password():
    """Switches to forgot password frame"""
    log_in_frame.grid_forget()
    forgot_password_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)

def reset_password():
    """Handle password reset"""
    email = forgot_email_entry.get()
    phone = forgot_phone_entry.get()
    new_password = new_password_entry.get()
    confirm_new_password = confirm_new_password_entry.get()
    
    if not email or not phone or not new_password or not confirm_new_password:
        messagebox.showerror("Error", "All fields are required")
        return
        
    if new_password != confirm_new_password:
        messagebox.showerror("Error", "Passwords do not match")
        return
        
    password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,24}$')
    if not password_pattern.match(new_password):
        messagebox.showerror("Error", "Password must be \n # at least 8 characters \n # no longer than 24 characters \n # at least one number \n # one special character")
        return
    
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="securefile"
        )
        cursor = mydb.cursor()
        
        check_query = "SELECT * FROM userdata WHERE email_address=%s AND phone_number=%s"
        cursor.execute(check_query, (email, phone))
        result = cursor.fetchone()
        
        if result:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            update_query = "UPDATE userdata SET password=%s WHERE email_address=%s AND phone_number=%s"
            cursor.execute(update_query, (hashed_password, email, phone))
            mydb.commit()
            messagebox.showinfo("Success", "Password reset successful!")
            
            forgot_email_entry.delete(0, 'end')
            forgot_phone_entry.delete(0, 'end')
            new_password_entry.delete(0, 'end')
            confirm_new_password_entry.delete(0, 'end')
            
            show_log_in()
        else:
            messagebox.showerror("Error", "Email and Phone number do not match our records")
            
    except Error as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def show_log_in_from_forgot():
    """Switch from forgot password to login frame"""
    forgot_password_frame.grid_forget()
    log_in_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)

# --------------------------------------- Getting Input (sign_up_frame) --------------------------------------- #

"""
    This code accesses the values of several 'Entry' widgets in a GUI from (sign_up_frame).
"""

def submit_sign_up():
    # Access the values of the Entry widgets
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password= confirm_password_entry.get()
    
# --------------------------------------- Checking Email Pattern (sign_up_frame) --------------------------------------- #

    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_pattern.match(email):
        messagebox.showerror("Error", "Invalid Email")
        return
    
# --------------------------------------- Checking First Name Length (sign_up_frame) --------------------------------------- #

    if len(first_name) > 12 or len(first_name) < 3:
        messagebox.showerror("Error", "First Name must be at least 3 characters and no longer than 12 characters")
        return

# --------------------------------------- Checking Last Name Length (sign_up_frame) --------------------------------------- #

    if len(last_name) > 12 or len(last_name) < 3:
        messagebox.showerror("Error", "Last Name must be at least 3 characters and no longer than 12 characters")
        return

# --------------------------------------- Checking Phone Number (sign_up_frame) --------------------------------------- #

    if not phone_number.isdigit() or len(phone_number) != 10:
        messagebox.showerror("Error", "Phone Number must only contain numbers and be 10 digits long")
        return
    if password != confirm_password:
        messagebox.showerror("Error", "Password and Confirm Password do not match")
        return
    
# --------------------------------------- Checking strength of Password (sign_up_frame) --------------------------------------- #

    password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,24}$')
    if not password_pattern.match(password):
        messagebox.showerror("Error", "Password must be \n # at least 8 characters \n # no longer than 24 characters \n # at lest one number \n # one special character")
        return
    
# --------------------------------------- Hashing Password (sign_up_frame) --------------------------------------- #
    
    password =password.encode()
    password = hashlib.sha256(password).hexdigest()
    
# --------------------------------------- Connecting To Database (sign_up_frame) --------------------------------------- #

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="securefile"
    )

# --------------------------------------- Chicking Availability Of Email and Phone Number (sign_up_frame) --------------------------------------- #

    cursor = mydb.cursor()
    check_user_query = "SELECT * FROM userdata WHERE email_address =%s OR phone_number=%s"
    cursor.execute(check_user_query, (email, phone_number))
    result = cursor.fetchone()
    if result:
        messagebox.showerror("Error", "Email or Phone number already in use")
    else:
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="securefile"
            )
            mycursor = mydb.cursor()
            sql = "INSERT INTO userdata (first_name, last_name, email_address, phone_number, password) VALUES (%s, %s, %s, %s, %s)"
            val = (first_name, last_name, email, phone_number, password)
            mycursor.execute(sql, val)
            mydb.commit()
            mydb.close()
            
            if messagebox.showinfo("Success", "Account Created Successfully!") == "ok":
                show_log_in()  # Redirect to login page
                first_name_entry.delete(0, "end")
                last_name_entry.delete(0, "end")
                phone_number_entry.delete(0, "end")
                email_entry.delete(0, "end")
                password_entry.delete(0, "end")
                confirm_password_entry.delete(0, "end")
        except Error:
            messagebox.showerror("Error", "Failed to create account. Please try again later.")

# --------------------------------------- Getting Input (log_in_frame) --------------------------------------- #

def validate_log_in_credentials():
    
    log_email = log_email_entry.get()
    log_password = log_password_entry.get()
    # log_email = "pratikalakarki@gmail.com"
    # log_password = "Prats123@"
    
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_pattern.match(log_email):
        messagebox.showerror("Error", "Invalid Email")
        return
    
    log_password =log_password.encode()
    log_password = hashlib.sha256(log_password).hexdigest()
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securefile"
    )
    cursor = mydb.cursor()
    query = "SELECT email_address, password, id FROM userdata WHERE email_address=%s and password=%s"
    cursor.execute(query, (log_email, log_password))
    result = cursor.fetchone()
    if result:
        current_user_id = result[2]
        show_home_page(current_user_id)
        return 
    else:
        messagebox.showerror("Error", "Invalid Credentials")
        return False


# --------------------------------------- Switching to (sign_up_frame) --------------------------------------- #

""" 
        This code defines a function show_sign_up that switches the displayed frame 
    from main_frame to sign_up_frame.
    """

def show_sign_up():
    main_frame.grid_forget()
    sign_up_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)

# --------------------------------------- Switching to (log_in_frame) --------------------------------------- #

"""
        This code defines a function show_log_in that switches the displayed frame 
    from main_frame to log_in_frame.
    """
    
def show_log_in():
    main_frame.grid_forget()
    log_in_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)
        
# --------------------------------------- Switching Back to (main_frame) --------------------------------------- #

"""
        This code defines a function back_to_main that switches the displayed frame 
    from either the sign_up_frame or the log_in_frame back to the main_frame.
    """
    
def back_to_main():
    sign_up_frame.grid_forget()
    log_in_frame.grid_forget()
    main_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)
        
# --------------------------------------- Switching to (home_page_frame) --------------------------------------- #

"""
        This code defines a function show_log_in that switches the displayed frame 
    from main_frame to log_in_frame.
    """        

# Add this new logout function
def logout():
    if messagebox.showinfo("Logout", "Successfully logged out!") == "ok":
        # Clear any user data
        home_page_frame.grid_forget()
        for widget in home_page_frame.winfo_children():
            widget.destroy()
        show_log_in()

# Add this new function to view file contents
def view_file_contents(file_path, file_name):
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create new window to display content
        view_window = tk.Toplevel()
        view_window.title(f"Viewing: {file_name}")
        
        # Set window size and position
        window_width = 600
        window_height = 400
        screen_width = view_window.winfo_screenwidth()
        screen_height = view_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        view_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Add text widget with scrollbar
        text_frame = tk.Frame(view_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap="word", font=("Helvetica", 12))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Insert content and make read-only
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        
        # Close button
        close_button = tk.Button(view_window, 
                               text="Close",
                               command=view_window.destroy,
                               font=("Helvetica", 12),
                               background=BUTTON_BG,
                               foreground=TEXT_COLOR)
        close_button.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file: {str(e)}")

# Add this new function to handle file deletion
def delete_file(file_path, file_name, current_user_id):
    try:
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {file_name}?"):
            # Delete from database
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="securefile"
            )
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM filestorage WHERE user_id = %s AND file_name = %s", 
                         (current_user_id, file_name))
            mydb.commit()
            mydb.close()

            # Delete physical file
            if os.path.exists(file_path):
                os.remove(file_path)

            messagebox.showinfo("Success", "File deleted successfully!")
            show_home_page(current_user_id)  # Refresh the page
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete file: {str(e)}")

# Modify the show_home_page function
def show_home_page(current_user_id):
    # Clear existing widgets
    for widget in home_page_frame.winfo_children():
        widget.destroy()
    
    main_frame.grid_forget()
    home_page_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")

    # Create main container
    main_container = tk.Frame(home_page_frame, bg=MAIN_BG)
    main_container.grid(row=0, column=0, sticky="nsew")  # Changed from pack to grid
    
    # Configure grid weights for expansion
    home_page_frame.grid_rowconfigure(0, weight=1)
    home_page_frame.grid_columnconfigure(0, weight=1)

    # Welcome header
    welcome_frame = tk.Frame(main_container, bg=MAIN_BG)
    welcome_frame.pack(fill="x")
    
    # Get user name from database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="securefile"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT first_name, last_name FROM userdata WHERE id = %s", (current_user_id,))
    user = cursor.fetchone()
    full_name = f"{user[0]} {user[1]}" if user else "User"
    
    welcome_label = ttk.Label(welcome_frame, 
                            text=f"Welcome, {full_name}",
                            font=("Helvetica", 16, "bold"),
                            background=MAIN_BG,
                            foreground=TEXT_COLOR)
    welcome_label.pack(pady=10)

    # Buttons frame
    buttons_frame = tk.Frame(main_container, bg=MAIN_BG)
    buttons_frame.pack(fill="x", pady=20)

    # Upload button
    upload_btn = tk.Button(buttons_frame,
                          text="Upload File",
                          command=lambda: browse_and_upload_file(current_user_id),
                          font=("Helvetica", 12),
                          background=BUTTON_BG,
                          foreground=TEXT_COLOR)
    upload_btn.pack(side="left", padx=10)

    # Files section
    files_frame = tk.LabelFrame(main_container, text="Your Files", bg=MAIN_BG, fg=TEXT_COLOR)
    files_frame.pack(fill="both", expand=True, pady=20)

    # Get files from database
    cursor.execute("SELECT file_name FROM filestorage WHERE user_id = %s ORDER BY time DESC", (current_user_id,))
    files = cursor.fetchall()

    if files:
        for file in files:
            file_name = file[0]
            file_path = os.path.join(ONLINE_FILE_DIR, file_name)
            
            # Create frame for each file row
            file_row = tk.Frame(files_frame, bg=MAIN_BG)
            file_row.pack(fill="x", pady=2)
            
            # File button
            file_btn = tk.Button(file_row,
                               text=file_name,
                               command=lambda f=file_path, n=file_name: view_file_contents(f, n),
                               bg=MAIN_BG,
                               fg=TEXT_COLOR)
            file_btn.pack(side="left", expand=True, fill="x", padx=(10, 5))
            
            # Delete button for each file
            delete_btn = tk.Button(file_row,
                                 text="Delete",  # Changed from × to "Delete"
                                 command=lambda f=file_path, n=file_name: delete_file(f, n, current_user_id),
                                 bg=BUTTON_BG,
                                 fg="red",
                                 width=6)
            delete_btn.pack(side="right", padx=5)
    else:
        no_files_label = ttk.Label(files_frame,
                                  text="No files uploaded yet",
                                  background=MAIN_BG,
                                  foreground=TEXT_COLOR)
        no_files_label.pack(pady=20)

    # Add bottom frame for buttons
    bottom_frame = tk.Frame(main_container, bg=MAIN_BG)
    bottom_frame.pack(side="bottom", fill="x", pady=10)

    # Delete All Files button (left)
    delete_all_btn = tk.Button(bottom_frame,
                            text="Delete All Files",
                            command=lambda: delete_all_files(current_user_id),
                            font=("Helvetica", 12),
                            background=BUTTON_BG,
                            foreground="red",
                            relief="raised",
                            bd=3)
    delete_all_btn.pack(side="left", padx=20)

    # Logout button (right)
    logout_btn = tk.Button(bottom_frame,
                          text="Logout",
                          command=logout,
                          font=("Helvetica", 12),
                          background=BUTTON_BG,
                          foreground=TEXT_COLOR,
                          relief="raised",
                          bd=3)
    logout_btn.pack(side="right", padx=20)

    # After the files section and before the menu frame, add the logout button
    logout_container = tk.Frame(main_container, bg=MAIN_BG)
    logout_container.pack(fill="x", pady=(10, 20))  # Reduced bottom padding

    logout_btn = tk.Button(logout_container,
                          text="Logout",
                          command=logout,
                          font=("Helvetica", 12, "bold"),
                          background="white",  # White background
                          foreground="black",  # Black text
                          relief="raised",
                          bd=2,
                          width=10,
                          height=1)
    logout_btn.pack(side="left", padx=20)

    mydb.close()

def browse_and_upload_file(current_user_id):
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")],
        title="Choose a file to upload"
    )
    
    if file_path:
        try:
            # Read the content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate filename with timestamp
            original_filename = os.path.basename(file_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}.txt"
            
            # Store in database
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="securefile"
            )
            cursor = mydb.cursor()
            
            query = "INSERT INTO filestorage (user_id, time, file_name) VALUES (%s, %s, %s)"
            values = (current_user_id, datetime.datetime.now(), new_filename)
            cursor.execute(query, values)
            mydb.commit()
            
            # Save encrypted file
            new_file_path = os.path.join(ONLINE_FILE_DIR, new_filename)
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo("Success", "File uploaded successfully!")
            
            # Refresh the page after successful upload
            for widget in home_page_frame.winfo_children():
                widget.destroy()
            show_home_page(current_user_id)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {str(e)}")
        finally:
            if 'mydb' in locals() and mydb.is_connected():
                mydb.close()

# Add function to delete all files
def delete_all_files(current_user_id):
    if messagebox.askyesno("Confirm Delete All", "Are you sure you want to delete all files?"):
        try:
            # Delete from database
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="securefile"
            )
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM filestorage WHERE user_id = %s", (current_user_id,))
            mydb.commit()
            mydb.close()

            # Delete all physical files for this user
            cursor.execute("SELECT file_name FROM filestorage WHERE user_id = %s", (current_user_id,))
            files = cursor.fetchall()
            for file in files:
                file_path = os.path.join(ONLINE_FILE_DIR, file[0])
                if os.path.exists(file_path):
                    os.remove(file_path)

            messagebox.showinfo("Success", "All files deleted successfully!")
            show_home_page(current_user_id)  # Refresh the page
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete files: {str(e)}")

# --------------------------------------- Connect to the database and retrieve the user data --------------------------------------- #

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securefile"
    )
    cursor = mydb.cursor()
    query = "SELECT first_name, last_name FROM userdata WHERE id = %s"
    cursor.execute(query, (current_user_id,))
    result = cursor.fetchone()
    if result:
        full_name = str(result[0]) + " " + str(result[1])
        home_text = ttk.Label(home_page_frame, text=f"Welcome, {full_name}", font=("Helvetica", 15), foreground=TEXT_COLOR, background=MAIN_BG)
        home_text.grid(row=0, column=1, pady=20, padx=10)
        # Connect to the database and retrieve the file names
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="securefile"
        )
        cursor = mydb.cursor()
        query = "SELECT file_name FROM filestorage WHERE user_id = %s"
        cursor.execute(query, (current_user_id,))
        file_names = cursor.fetchall()

        if file_names:
            row = 3
            column = 0
            files_text = ttk.Label(home_page_frame, text="Files:", font=("Helvetica", 15), foreground=TEXT_COLOR, background=MAIN_BG)
            files_text.grid(row=2, column=0, pady=10, padx=20,sticky="w")
            
# --------------------------------------- Arranging the Files in Alphabaticl Order --------------------------------------- #

            for i in range(len(file_names)):
                for j in range(len(file_names) - i - 1):
                    if file_names[j] > file_names[j + 1]:
                        file_names[j], file_names[j + 1] = file_names[j + 1]
            for i, file_name in enumerate(file_names):
                file_path = os.path.join(os.path.dirname(__file__), "online_file", str(file_name[0]))
                
# --------------------------------------- Decrypt the Users File --------------------------------------- #

                def ceaser_cipher(ciphertext, term, total_chars):
                    plaintext = ""
                    for i, char in enumerate(ciphertext):
                        shift = term[i % len(term)]
                        if char.isalpha():
                            if char.isupper():
                                shift_char = chr((ord(char) - shift - 65 + 26) % 26 + 65)
                                plaintext += shift_char
                            else:
                                shift_char = chr((ord(char) - shift - 97 + 26) % 26 + 97)
                                plaintext += shift_char
                        elif char.isdigit():
                            shift_char = chr((ord(char) - shift - 48 + 10) % 10 + 48)
                            plaintext += shift_char
                        else:
                            plaintext += char
                    return plaintext
                
# --------------------------------------- Genrate Algorythm To decrypt the text --------------------------------------- #

                def open_file(file_path):
                    with open(file_path, "r") as f:
                        # content_text.insert("0.0", f.read())
                        cipher_text=f.read()
                    
                    ciphertext = base64.b64decode(cipher_text.encode()).decode()
                    total_chars = len(ciphertext)
                    a = current_user_id
                    term = []
                    for n in range(1, total_chars):
                        if (ord(ciphertext[n]) >= 65 and ord(ciphertext[n]) <= 90) or (ord(ciphertext[n]) >= 97 and ord(ciphertext[n]) <= 122):
                            t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 50 - 25
                        else:
                            t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 18 - 9
                        term.append(t)
                    plaintext = ceaser_cipher(ciphertext, term, total_chars)
                    
                    read_file_window = tk.Toplevel(home_page_frame)
                    read_file_window.title(str(file_name))
                    screen_width = read_file_window.winfo_screenwidth()
                    screen_height = read_file_window.winfo_screenheight()

                    window_width = 400
                    window_height = 400

                    x_coordinate = (screen_width/2) - (window_width/2)
                    y_coordinate = (screen_height/2) - (window_height/2)

                    read_file_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
                    text = tk.Text(read_file_window, font=("Helvetica", 12))
                    text.pack(fill="both", expand=True)

                    text.insert("1.0", plaintext)
                    text.config(state="disabled") 
                        
                file_name = str(file_name[0]) # Convert file_name to a string
                new_file_name = ".".join(file_name.rsplit(".", 2)[:1]) + ".txt"
 
                
                # file_button = ttk.Button(home_page_frame, text=str(new_file_name), command=lambda file_path=file_path: open_file(file_path))
                # file_button.grid(row=row, column=column, pady=10, padx=50)
                browse_button = tk.Button(home_page_frame, text=str(new_file_name), command=lambda file_path=file_path: open_file(file_path), font=("Helvetica", 10), 
                background=MAIN_BG, foreground=TEXT_COLOR, relief="raised", 
                activebackground=MAIN_BG, activeforeground=TEXT_COLOR)
                browse_button.grid(row=row, column=column, padx=(15),pady=(10))
                browse_button.config(width=18)
                column += 1
                if column == 3:
                    row += 1
                    column = 0  
        else:
            files_text = ttk.Label(home_page_frame, text="No files found", font=("Helvetica", 12), foreground=TEXT_COLOR, background=MAIN_BG)
            files_text.grid(row=2, column=0, columnspan=3, pady=10, padx=(50,70)) 
            
# --------------------------------------- Search Entry code --------------------------------------- #

        search_entry = ttk.Entry(home_page_frame, width=20, font=("Helvetica", 12), 
                                    foreground=MAIN_BG, style="Round.TEntry",justify='center')
        search_entry.grid(row=1, column=1, padx=10, pady=10)

        
        search_button = tk.Button(home_page_frame, text="Search", command=lambda:search_files(), font=("Helvetica", 10), 
                          background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=1, 
                          activebackground=BUTTON_ACTIVE_BG, activeforeground=TEXT_COLOR)
        search_button.grid(row=1, column=2, padx=(65,0),pady=5,sticky="w")
        search_button.config(width=7)
        
# --------------------------------------- Search For Files --------------------------------------- # 
                                    
        def search_files():
            search_string = search_entry.get()
            search_results = []
            for file_name in file_names:
                if search_string in str(file_name[0]):
                    search_results.append(file_name[0])
            if search_results:
                search_window = tk.Toplevel(home_page_frame)
                search_window.title("Search Results")
                screen_width = search_window.winfo_screenwidth()
                screen_height = search_window.winfo_screenheight()

                window_width = 400
                window_height = 400

                x_coordinate = (screen_width/2) - (window_width/2)
                y_coordinate = (screen_height/2) - (window_height/2)

                search_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
                search_window.config(bg=MAIN_BG)
                results_text = ttk.Label(search_window, text="Results", font=("Helvetica", 15), foreground=TEXT_COLOR, background=MAIN_BG)
                results_text.grid(row=0, column=0, pady=10, padx=50,sticky="n")


                
                result_row = 2
                result_column = 0
                for result in search_results:
                    # result_button = ttk.Button(search_window, text=result, command=lambda file_path=f"C:/Users/98218/OneDrive/Desktop/online_file/{result}": open_file(file_path))
                    # result_button.grid(row=result_row, column=result_column, pady=10, padx=50)
                    
                    result_button = tk.Button(search_window, text=result, command=lambda file_path=os.path.join(os.path.dirname(__file__), "online_file", result): open_file(file_path), font=("Helvetica", 10), 
                    background=MAIN_BG, foreground=TEXT_COLOR, relief="raised", 
                    activebackground=MAIN_BG, activeforeground=TEXT_COLOR)
                    result_button.grid(row=result_row, column=result_column, padx=(30),pady=(10))
                    result_button.config(width=40)
                    result_row += 1
            else:
                messagebox.showerror("Error", "No search results found")           
        def insert_into_database(file_path):
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="securefile"
            )
            cursor = mydb.cursor()
            query = "INSERT INTO filestorage (user_id, time, file_name) VALUES (%s, %s, %s)"
            original_file_name = os.path.basename(file_path)
            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_file_name = f"{os.path.splitext(original_file_name)[0]}.{time_stamp}{os.path.splitext(original_file_name)[1]}"
            values = (current_user_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), new_file_name)
            cursor.execute(query, values)
            mydb.commit()
                    
            def ceaser_cipher(plaintext, term, total_chars):
                ciphertext = ""
                for i, char in enumerate(plaintext):
                    shift = term[i % len(term)] # use the i-th term to shift the i-th character
                    if char.isalpha():
                        if char.isupper():
                            shift_char = chr((ord(char) + shift - 65) % 26 + 65)
                            ciphertext += shift_char
                        else:
                            shift_char = chr((ord(char) + shift - 97) % 26 + 97)
                            ciphertext += shift_char
                    elif char.isdigit():
                        shift_char = chr((ord(char) + shift - 48) % 10 + 48)
                        ciphertext += shift_char
                    else:
                        ciphertext += char
                b64_ciphertext = base64.b64encode(ciphertext.encode()).decode()
                return b64_ciphertext

            with open(file_path, "r") as f:
                file_content = f.read()
                term = []
            a=current_user_id
            total_chars = len(file_content)
            plaintext=file_content
            for n in range(1, total_chars):
                if (ord(plaintext[n]) >= 65 and ord(plaintext[n]) <= 90) or (ord(plaintext[n]) >= 97 and ord(plaintext[n]) <= 122):
                    t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 50 - 25
                else:
                    t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 18 - 9
                term.append(t)
            ciphertext = ceaser_cipher(plaintext, term, total_chars)
   
            new_file_path = os.path.join(os.path.dirname(__file__), "online_file", new_file_name)
            with open(new_file_path, "w") as f:
                f.write(ciphertext)

            messagebox.showinfo("Success", "File successfully uploaded")
                            
        def browse_file():
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if file_path:
                    insert_into_database(file_path)
            # "Browse" button 
        browse_button = tk.Button(home_page_frame, text="Browse", command=lambda:browse_file(), font=("Helvetica", 10), 
                          background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=1, 
                          activebackground=BUTTON_ACTIVE_BG, activeforeground=TEXT_COLOR)
        browse_button.grid(row=1, column=0, padx=(20,10),pady=5,sticky="nw")
        browse_button.config(width=7)
        refresh_button = tk.Button(home_page_frame, text="refresh", command=lambda:show_home_page(current_user_id), font=("Helvetica", 10), 
                    background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=1, 
                    activebackground=BUTTON_ACTIVE_BG, activeforeground=TEXT_COLOR)
        refresh_button.grid(row=2, column=2, padx=(25,10),pady=5,sticky="n")
        refresh_button.config(width=7)  
        
    else:
        return

    # Add menu buttons frame
    menu_frame = tk.Frame(home_page_frame, bg=MAIN_BG)
    menu_frame.grid(row=1, column=0, columnspan=3, pady=20)

    # Upload Files Button
    upload_button = tk.Button(menu_frame, 
                            text="Upload Files",
                            command=lambda: show_upload_section(),
                            font=("Helvetica", 12),
                            background=BUTTON_BG,
                            foreground=TEXT_COLOR,
                            relief="raised",
                            bd=3,
                            activebackground=BUTTON_ACTIVE_BG,
                            activeforeground=TEXT_COLOR)
    upload_button.grid(row=0, column=0, padx=20)
    upload_button.config(width=15)

    # View Files Button
    view_button = tk.Button(menu_frame, 
                          text="View Files",
                          command=lambda: show_files_section(),
                          font=("Helvetica", 12),
                          background=BUTTON_BG,
                          foreground=TEXT_COLOR,
                          relief="raised",
                          bd=3,
                          activebackground=BUTTON_ACTIVE_BG,
                          activeforeground=TEXT_COLOR)
    view_button.grid(row=0, column=1, padx=20)
    view_button.config(width=15)

    # Logout Button
    logout_button = tk.Button(menu_frame, 
                            text="Logout",
                            command=lambda: show_log_in(),
                            font=("Helvetica", 12),
                            background=BUTTON_BG,
                            foreground=TEXT_COLOR,
                            relief="raised",
                            bd=3,
                            activebackground=BUTTON_ACTIVE_BG,
                            activeforeground="red")
    logout_button.grid(row=0, column=2, padx=20)
    logout_button.config(width=15)

    # Create frames for different sections
    upload_section = tk.Frame(home_page_frame, bg=MAIN_BG)
    files_section = tk.Frame(home_page_frame, bg=MAIN_BG)

    def show_upload_section():
        files_section.grid_forget()
        upload_section.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=20)
        
        # Browse button
        browse_button = tk.Button(upload_section, 
                                text="Choose File", 
                                command=lambda: browse_file(),
                                font=("Helvetica", 12),
                                background=BUTTON_BG,
                                foreground=TEXT_COLOR,
                                relief="raised",
                                bd=3)
        browse_button.pack(pady=20)
        browse_button.config(width=20)

    def show_files_section():
        upload_section.grid_forget()
        files_section.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=20)

        # Add search functionality
        search_frame = tk.Frame(files_section, bg=MAIN_BG)
        search_frame.pack(fill="x", padx=20, pady=10)

        search_entry = ttk.Entry(search_frame, 
                               width=30,
                               font=("Helvetica", 12),
                               foreground=MAIN_BG,
                               style="Round.TEntry")
        search_entry.pack(side="left", padx=5)

        search_button = tk.Button(search_frame,
                                text="Search",
                                command=lambda: search_files(),
                                font=("Helvetica", 10),
                                background=BUTTON_BG,
                                foreground=TEXT_COLOR)
        search_button.pack(side="left", padx=5)

        # Display files in a scrollable frame
        files_canvas = tk.Canvas(files_section, bg=MAIN_BG)
        scrollbar = ttk.Scrollbar(files_section, orient="vertical", command=files_canvas.yview)
        scrollable_frame = tk.Frame(files_canvas, bg=MAIN_BG)

        files_canvas.configure(yscrollcommand=scrollbar.set)

        # Add files to scrollable frame
        display_files(scrollable_frame, current_user_id)

        files_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: files_canvas.configure(scrollregion=files_canvas.bbox("all")))

        files_canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

    # Initially show the files section
    show_files_section()

# --------------------------------------- Switching to (open_file_frame) --------------------------------------- # 
  
def open_file_format():
    home_page_frame.grid_forget()
    open_file_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
    for i in range(12):
        root.rowconfigure(i, minsize=50)
    for i in range(12):
        root.columnconfigure(i, minsize=50)

# --------------------------------------- Creating The Main Window --------------------------------------- #

"""
        This code creates the main window of a Tkinter GUI application and sets its 
    dimensions and location on the screen.
    """
    
root = tk.Tk()
root.title("Secure File Vault")  # Add this line
root.configure(bg=MAIN_BG)
root.geometry("600x600")
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 3
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 4.5
root.geometry("+%d+%d" % (x, y))

# --------------------------------------- Creating (main_frame) --------------------------------------- #

"""
        This code creates a Tkinter Frame widget and assigns it to the variable main_frame. 
    """
    
main_frame = tk.Frame(root, bg=MAIN_BG)

# --------------------------------------- Setting Layoput in (main_frame) --------------------------------------- #

"""
        This code sets the layout of the main_frame using the grid geometry manager.
    """
    
main_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
for i in range(12):
    root.rowconfigure(i, minsize=50)
for i in range(12):
    root.columnconfigure(i, minsize=50)
    
# --------------------------------------- Topic Text (main_frame) --------------------------------------- #

"""
       This code creates a Label widget with the text "Secure File Vault" 
    in the main_frame. 
    """
    
project_text = ttk.Label(main_frame, text="Secure File Vault", 
                         font=("Travelast", 30), foreground=TEXT_COLOR, background=MAIN_BG)
project_text.grid(row=0, column=2, columnspan=1, pady=20, padx=50)

# --------------------------------------- By Text (main_frame) --------------------------------------- #

"""
       This code creates a Label widget with the text "by" 
    in the main_frame. 
    """
    
by_text = ttk.Label(main_frame, text="by", font=("Hanging Letters", 25), foreground=TEXT_COLOR, 
                    background=MAIN_BG)
by_text.grid(row=1, column=2, columnspan=1, pady=10, padx=10)

# --------------------------------------- Name Text (main_frame) --------------------------------------- #

"""
       This code creates a Label widget with the text "Pratikala Karki" 
    in the main_frame. 
    """
    
name_text = ttk.Label(main_frame, text="Pratikala Karki", font=("3x5", 35), foreground=TEXT_COLOR, 
                      background=MAIN_BG)
name_text.grid(row=2, column=2, columnspan=1, pady=(10,80), padx=10 ,sticky='n')

# --------------------------------------- Sign Up Button (main_frame) --------------------------------------- #

"""
        This code creates a button widget with the text "Sign Up" and adds it to the main_frame.
    """
    
back_button = tk.Button(main_frame, text="Sign Up", command=show_sign_up, font=("Helvetica", 13), 
                        background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=3, 
                        activebackground=BUTTON_ACTIVE_BG,activeforeground=TEXT_COLOR)
back_button.grid(row=4, column=2,sticky="s", padx=250, pady=10)
back_button.config(width=8)

# --------------------------------------- Log In Button (main_frame) --------------------------------------- #

"""
        This code creates a button widget with the text "Log In" and adds it to the main_frame.
    """
    
back_button = tk.Button(main_frame, text="Log In", command=show_log_in, font=("Helvetica", 13), 
                        background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=3, 
                        activebackground=BUTTON_ACTIVE_BG,activeforeground=TEXT_COLOR)
back_button.grid(row=5, column=2,sticky="s", padx=250, pady=10)
back_button.config(width=8)

# --------------------------------------- Exit Button (main_frame) --------------------------------------- #

"""
        This code creates a button widget with the text "Exit" and adds it to the main_frame.
    """
    
back_button = tk.Button(main_frame, text="Exit", command=root.quit, font=("Helvetica", 13), 
                        background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=3, 
                        activebackground=BUTTON_ACTIVE_BG,activeforeground="red")
back_button.grid(row=6, column=2, sticky="s", padx=250, pady=10)
back_button.config(width=8)

# --------------------------------------- Footer Lable (main_frame) --------------------------------------- #

"""
       This code creates a Label widget with the text "Protecting your precious memories, one file at a time." 
    in the main_frame but at buttom. 
    """

work_text = ttk.Label(main_frame, text="Protecting your precious memories, one file at a time.", 
                      font=("Helvetica",10), foreground=TEXT_COLOR, background=MAIN_BG)
work_text.grid(row=8, column=2, columnspan=1, pady=(80,5), padx=50)

# --------------------------------------- Styling Entry Widget --------------------------------------- #

"""
        This code defines a style named "Round" for a Tkinter ttk entry widget.
    """
    
style = ttk.Style()
style.configure("Round.TEntry", fieldbackground="#ffffff", background="transparent", 
                 bd=5, relief="flat", padding=2, borderwidth=2,
                 highlightcolor="#597678", highlightbackground="#597678", 
                 borderradius=10)

# --------------------------------------- Creating (sign_up_frame) --------------------------------------- #

"""
        This code creates a Tkinter frame widget, with a background color of "#FF69B4".
    """
    
sign_up_frame = tk.Frame(root, bg=MAIN_BG)

# --------------------------------------- sign_up Text (sign_up_frame) --------------------------------------- #

"""
               This code creates a Label widget with the text "Sign Up" 
    in the sign_up_frame. 
    """

sign_up_text = ttk.Label(sign_up_frame, text="Sign Up", font=("Travelast", 25), foreground=TEXT_COLOR, 
                         background=MAIN_BG)
sign_up_text.grid(row=0, column=2, columnspan=1, pady=30, padx=50, sticky="nw")

# --------------------------------------- First Name (sign_up_frame) --------------------------------------- #

"""
        This code creates two Tkinter widgets, a label with text "First Name:" and an Entry widget, 
    both inside the 'sign_up_frame'. 
    """
    
first_name_label = tk.Label(sign_up_frame, text="First Name:", font=("Helvetica", 14), 
                            foreground=TEXT_COLOR, background=MAIN_BG)
first_name_entry = ttk.Entry(sign_up_frame, width=25, font=("Helvetica", 16), 
                             foreground=MAIN_BG, style="Round.TEntry", background='gray')
first_name_entry.configure(background='gray')

first_name_label.grid(row=1, column=1, padx=20, pady=10, sticky="W")
first_name_entry.grid(row=1, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Last Name (sign_up_frame) --------------------------------------- #

"""
        This code creates two Tkinter widgets, a label with text "Last Name:" and an Entry widget, 
    both inside the 'sign_up_frame'. 
    """
    
last_name_label = tk.Label(sign_up_frame, text="Last Name:", font=("Helvetica", 14), 
                           foreground=TEXT_COLOR, background=MAIN_BG)
last_name_entry = ttk.Entry(sign_up_frame, width=25, font=("Helvetica", 16), 
                            foreground=MAIN_BG, style="Round.TEntry")

last_name_label.grid(row=2, column=1, padx=20, pady=10, sticky="W")
last_name_entry.grid(row=2, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Phone Number (sign_up_frame) --------------------------------------- #

"""
        This code creates two Tkinter widgets, a label with text "Phone Number:" and an Entry widget, 
    both inside the 'sign_up_frame'. 
    """
    
phone_number_label = tk.Label(sign_up_frame, text="Phone Number:", font=("Helvetica", 14), 
                              foreground=TEXT_COLOR, background=MAIN_BG)
phone_number_entry = ttk.Entry(sign_up_frame, width=25, font=("Helvetica", 16), 
                               foreground=MAIN_BG,style="Round.TEntry")

phone_number_label.grid(row=3, column=1, padx=20, pady=10, sticky="W")
phone_number_entry.grid(row=3, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Email (sign_up_frame) --------------------------------------- #

"""
        This code creates two Tkinter widgets, a label with text "Email:" and an Entry widget, 
    both inside the 'sign_up_frame'. 
    """
    
email_label = tk.Label(sign_up_frame, text="Email:", font=("Helvetica", 14), 
                       foreground=TEXT_COLOR, background=MAIN_BG)
email_entry = ttk.Entry(sign_up_frame, width=25, font=("Helvetica", 16), 
                        foreground=MAIN_BG, style="Round.TEntry")

email_label.grid(row=4, column=1, padx=20, pady=10, sticky="W")
email_entry.grid(row=4, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Password (sign_up_frame) --------------------------------------- #

"""
        This code creates two Tkinter widgets, a label with text "Password:" and an Entry widget, 
    both inside the 'sign_up_frame'. 
    """
    
password_label = tk.Label(sign_up_frame, text="Password:", font=("Helvetica", 14), 
                          foreground=TEXT_COLOR, background=MAIN_BG)
password_entry = ttk.Entry(sign_up_frame, show="*", width=25, font=("Helvetica", 16), 
                           foreground=MAIN_BG, style="Round.TEntry")

password_label.grid(row=5, column=1, padx=20, pady=10, sticky="W")
password_entry.grid(row=5, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Confirm Password (sign_up_frame) --------------------------------------- #

"""
        This code creates two Tkinter widgets, a label with text "Confirm Password:" and an Entry widget, 
    both inside the 'sign_up_frame'. 
    """
    
confirm_password_label = tk.Label(sign_up_frame, text="Confirm Password:", font=("Helvetica", 14), 
                                  foreground=TEXT_COLOR, background=MAIN_BG)
confirm_password_entry = ttk.Entry(sign_up_frame, show="*", width=25, font=("Helvetica", 16), 
                                   foreground=MAIN_BG, style="Round.TEntry")

confirm_password_label.grid(row=6, column=1, padx=20, pady=10, sticky="W")
confirm_password_entry.grid(row=6, column=2, padx=10, pady=10, sticky="W")

def toggle_password_visibility(show_password_var):
    if show_password_var.get() == 1:
        confirm_password_entry.config(show="")
        password_entry.config(show="")
        show_password_checkbox.config(foreground="black")
    else:
        confirm_password_entry.config(show="*")
        password_entry.config(show="*")
        show_password_checkbox.config(foreground=TEXT_COLOR)

show_password_var = tk.IntVar(value=0)
show_password_checkbox = tk.Checkbutton(sign_up_frame, text="Show Password", variable=show_password_var,
                                        command=lambda: toggle_password_visibility(show_password_var),
                                        foreground="black", background=MAIN_BG)
show_password_checkbox.grid(row=7, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Submit Button (sign_up_frame) --------------------------------------- #

"""
        This code creates a "Submit" button in the sign_up_frame.
    """
    
submit_button = tk.Button(sign_up_frame, text="Submit", command=submit_sign_up, font=("Helvetica", 12), 
                          background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=3,
                          activebackground=BUTTON_ACTIVE_BG,activeforeground=TEXT_COLOR)
submit_button.grid(row=9, column=2,sticky="e",pady=10)
submit_button.config(width=8)

# --------------------------------------- Back Button (sign_up_frame) --------------------------------------- #

"""
        This code creates a "Back" button in the sign_up_frame.
    """
    
back_button = tk.Button(sign_up_frame, text="Back", command=back_to_main, font=("Helvetica", 12), 
                        background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=3, 
                        activebackground=BUTTON_ACTIVE_BG,activeforeground="red")
back_button.grid(row=11, column=1, sticky="sw",padx=10,pady=20)
back_button.config(width=8)

# ---------------------------------------  Creating (log_in_frame) --------------------------------------- #

"""
        This code creates a Tkinter frame widget, with a background color of "#FF69B4".
    """
    
log_in_frame = tk.Frame(root, bg=MAIN_BG)

# --------------------------------------- log_in text (log_in_frame) --------------------------------------- #

"""
               This code creates a Label widget with the text "Log In" 
    in the log_in_frame. 
    """
    
log_in_text = ttk.Label(log_in_frame, text="Log In", font=("Travelast", 25), 
                        foreground=TEXT_COLOR, background=MAIN_BG)
log_in_text.grid(row=0, column=2, columnspan=1, pady=30, padx=50)

# --------------------------------------- Email (log_in_frame) --------------------------------------- #

"""
        This code creates two Tkinter widgets, a label with text "Email:" and an Entry widget, 
    both inside the 'log_in_frame'. 
    """

log_email_label = tk.Label(log_in_frame, text="Email:", font=("Helvetica", 14), 
                           foreground=TEXT_COLOR, background=MAIN_BG)
log_email_entry = ttk.Entry(log_in_frame, width=25, font=("Helvetica", 16), 
                            foreground=MAIN_BG, style="Round.TEntry")

log_email_label.grid(row=2, column=1, padx=20, pady=10, sticky="W")
log_email_entry.grid(row=2, column=2, padx=10, pady=10, sticky="W")

# --------------------------------------- Password (log_in_frame) --------------------------------------- #

"""
        This code creates two Tkinter widgets, a label with text "Password:" and an Entry widget, 
    both inside the 'log_in_frame'. 
    """
    
log_password_label = tk.Label(log_in_frame, text="Password:", font=("Helvetica", 14), 
                              foreground=TEXT_COLOR, background=MAIN_BG)
log_password_entry = ttk.Entry(log_in_frame, show="*", width=25, font=("Helvetica", 16), 
                               foreground=MAIN_BG, style="Round.TEntry")

log_password_label.grid(row=3, column=1, padx=20, pady=10, sticky="W")
log_password_entry.grid(row=3, column=2, padx=10, pady=10, sticky="W")
# --------------------------------------- Toogle password visibility (log_in_frame) --------------------------------------- #
def toggle_password_visibility_log_in(show_password_var_log_in):
    if show_password_var_log_in.get() == 1:
        log_password_entry.config(show="")
        show_password_checkbox.config(foreground="black")
    else:
        log_password_entry.config(show="*")
        show_password_checkbox.config(foreground="black")

show_password_var_log_in = tk.IntVar(value=0)
show_password_checkbox_log_in = tk.Checkbutton(log_in_frame, text="Show Password", variable=show_password_var_log_in,
                                        command=lambda: toggle_password_visibility_log_in(show_password_var_log_in),
                                        foreground="black", background=MAIN_BG)
show_password_checkbox_log_in.grid(row=4, column=2, padx=10, pady=10, sticky="W")


# --------------------------------------- Log In Button (log_in_frame) --------------------------------------- #
'''log in frame ----  loin button '''
log_in_button = tk.Button(log_in_frame, text="Log In", command=validate_log_in_credentials, font=("Helvetica", 12), 
                          background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=3, 
                          activebackground=BUTTON_ACTIVE_BG, activeforeground=TEXT_COLOR)
log_in_button.grid(row=5, column=2, padx=10,pady=50)
log_in_button.config(width=8)

# --------------------------------------- Back Button (log_in_frame) --------------------------------------- #
'''sign up frame ---- back button '''
back_button = tk.Button(log_in_frame, text="Back", command=back_to_main, font=("Helvetica", 12), 
                        background=BUTTON_BG, foreground=TEXT_COLOR, relief="raised", bd=3, 
                        activebackground=BUTTON_ACTIVE_BG,activeforeground="red")
back_button.grid(row=6, column=1, sticky="w",padx=10,pady=150)
back_button.config(width=8)

# Add forgot password button
forgot_password_button = tk.Button(log_in_frame, 
                                 text="Forgot Password?", 
                                 command=show_forgot_password, 
                                 font=("Helvetica", 10),
                                 background=BUTTON_BG, 
                                 foreground=TEXT_COLOR,
                                 relief="raised", 
                                 bd=3,
                                 activebackground=BUTTON_ACTIVE_BG,
                                 activeforeground=TEXT_COLOR)
forgot_password_button.grid(row=4, column=2, padx=10, pady=5, sticky="e")

# Create forgot password frame
forgot_password_frame = tk.Frame(root, bg=MAIN_BG)

# Title
forgot_password_text = ttk.Label(forgot_password_frame, 
                               text="Reset Password", 
                               font=("Travelast", 25),
                               foreground=TEXT_COLOR, 
                               background=MAIN_BG)
forgot_password_text.grid(row=0, column=2, columnspan=1, pady=30, padx=50)

# Email field
forgot_email_label = tk.Label(forgot_password_frame, 
                            text="Email:", 
                            font=("Helvetica", 14),
                            foreground=TEXT_COLOR, 
                            background=MAIN_BG)
forgot_email_entry = ttk.Entry(forgot_password_frame, 
                             width=25,
                             font=("Helvetica", 16),
                             foreground=MAIN_BG, 
                             style="Round.TEntry")
forgot_email_label.grid(row=1, column=1, padx=20, pady=10, sticky="W")
forgot_email_entry.grid(row=1, column=2, padx=10, pady=10, sticky="W")

# Phone number field
forgot_phone_label = tk.Label(forgot_password_frame, 
                            text="Phone Number:", 
                            font=("Helvetica", 14),
                            foreground=TEXT_COLOR, 
                            background=MAIN_BG)
forgot_phone_entry = ttk.Entry(forgot_password_frame, 
                             width=25,
                             font=("Helvetica", 16),
                             foreground=MAIN_BG, 
                             style="Round.TEntry")
forgot_phone_label.grid(row=2, column=1, padx=20, pady=10, sticky="W")
forgot_phone_entry.grid(row=2, column=2, padx=10, pady=10, sticky="W")

# New password fields
new_password_label = tk.Label(forgot_password_frame, 
                            text="New Password:", 
                            font=("Helvetica", 14),
                            foreground=TEXT_COLOR, 
                            background=MAIN_BG)
new_password_entry = ttk.Entry(forgot_password_frame, 
                             show="*",
                             width=25,
                             font=("Helvetica", 16),
                             foreground=MAIN_BG, 
                             style="Round.TEntry")
new_password_label.grid(row=3, column=1, padx=20, pady=10, sticky="W")
new_password_entry.grid(row=3, column=2, padx=10, pady=10, sticky="W")

confirm_new_password_label = tk.Label(forgot_password_frame, 
                                    text="Confirm Password:", 
                                    font=("Helvetica", 14),
                                    foreground=TEXT_COLOR, 
                                    background=MAIN_BG)
confirm_new_password_entry = ttk.Entry(forgot_password_frame, 
                                     show="*",
                                     width=25,
                                     font=("Helvetica", 16),
                                     foreground=MAIN_BG, 
                                     style="Round.TEntry")
confirm_new_password_label.grid(row=4, column=1, padx=20, pady=10, sticky="W")
confirm_new_password_entry.grid(row=4, column=2, padx=10, pady=10, sticky="W")

# Reset and Back buttons
reset_button = tk.Button(forgot_password_frame, 
                        text="Reset Password",
                        command=reset_password,
                        font=("Helvetica", 12),
                        background=BUTTON_BG,
                        foreground=TEXT_COLOR,
                        relief="raised",
                        bd=3,
                        activebackground=BUTTON_ACTIVE_BG,
                        activeforeground=TEXT_COLOR)

back_to_login_button = tk.Button(forgot_password_frame, 
                               text="Back to Login", 
                               command=show_log_in_from_forgot,  # Changed this line
                               font=("Helvetica", 12),
                               background=BUTTON_BG, 
                               foreground=TEXT_COLOR,
                               relief="raised", 
                               bd=3,
                               activebackground=BUTTON_ACTIVE_BG,
                               activeforeground="red")
back_to_login_button.grid(row=6, column=1, sticky="w", padx=10, pady=20)
back_to_login_button.config(width=12)

reset_button.grid(row=5, column=2, padx=10, pady=20)
reset_button.config(width=15)

# --------------------------------------- Refresh Frame --------------------------------------- #

def refresh_frame():
    home_page_frame.after(1000, refresh_frame)

home_page_frame = tk.Frame(root, bg=MAIN_BG)
open_file_frame = tk.Frame(root, bg=MAIN_BG)

root.mainloop()


