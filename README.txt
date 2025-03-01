
Secure File Vault
=================

Overview
--------
Secure File Vault is a Python application that allows users to securely store, view, and manage their files. The application uses Tkinter for the GUI and MySQL for the database. Files are encrypted before storage and decrypted when viewed.

Features
--------
- User Authentication:
  - Sign Up
  - Log In
  - Password Reset
- File Management:
  - Upload Files
  - View Files
  - Delete Files
  - Delete All Files
- Search Functionality
- Encryption and Decryption of Files

Setup
-----
1. **Database Setup**:
   - Ensure MySQL server is running.
   - Run the SQL script `database_setup.sql` to set up the database and tables.
   - Open phpMyAdmin, click on the SQL tab, copy and paste the contents of `database_setup.sql`, and click Go/Execute.

2. **Install Dependencies**:
   - Install the required Python packages using pip:
     ```
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   - Execute `main.py` to start the application:
     ```
     python main.py
     ```

Usage
-----
1. **Sign Up**:
   - Open the application and click on "Sign Up".
   - Fill in the required details and click "Submit".
   - If successful, you will be redirected to the login page.

2. **Log In**:
   - Enter your email and password and click "Log In".
   - If the credentials are valid, you will be redirected to the home page.

3. **Forgot Password**:
   - Click on "Forgot Password?" on the login page.
   - Enter your email, phone number, and new password.
   - Click "Reset Password" to update your password.

4. **Upload Files**:
   - Click on "Upload File" on the home page.
   - Browse and select a text file to upload.
   - The file will be encrypted and stored.

5. **View Files**:
   - Click on a file name to view its contents.
   - The file will be decrypted and displayed in a new window.

6. **Delete Files**:
   - Click on "Delete" next to a file name to delete the file.
   - Click on "Delete All Files" to delete all files.

7. **Search Files**:
   - Enter a search term in the search box and click "Search".
   - The search results will be displayed in a new window.

8. **Logout**:
   - Click on "Logout" to log out and return to the login page.

Testing
-------
- Run `test_app.py` to execute the unit tests:
  ```
  python -m unittest test_app.py -v
  ```

Files
-----
- `main.py`: Main application logic and GUI setup.
- `enc.py`: File encryption logic.
- `dec.py`: File decryption logic.
- `test_app.py`: Unit tests for basic functionality.
- `database_setup.sql`: SQL script to set up the database and tables.
- `requirements.txt`: List of required Python packages.
- `README.txt`: This readme file.

License
-------
This project is licensed under the MIT License.
