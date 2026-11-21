# LIBRARY MANAGEMENT SYSTEM
## Full Project README Documentation

**Project type:** Web Application  
**Backend:** Python + Flask  
**Frontend:** HTML5, CSS3, JavaScript  
**Database:** SQLite  
**IDE:** Visual Studio Code

---

## 1. Project Overview

The Library Management System is a web-based application for managing library books, student accounts, book searches, borrowing and returns, overdue fines, reservations, notifications, and reports.

The application is organized into eight modules. Each module has a separate Python file, and all modules use a common SQLite database connection.

### Objectives

- Store and manage library book details.
- Register and manage students and library staff.
- Search books by title, author, ISBN, or category.
- Record book issue and return transactions.
- Calculate overdue fines.
- Record book reservations.
- Store in-app notifications.
- Display library statistics and recent activity.

### Project scope

This is an educational starter application intended for local development and academic demonstration. It includes administrator login and basic library operations. Complete role-based permissions, email/SMS delivery, online payment processing, and automatic reservation queue fulfillment are not implemented in this version.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Flask | Web application framework |
| HTML5 | Web page structure |
| CSS3 | Page styling and responsive layout |
| JavaScript | Client-side interactions |
| SQLite | Relational database |
| Werkzeug | Password hashing |
| VS Code | Code editor |
| Web browser | Application interface |

---

## 3. System Requirements

### Hardware
- Desktop computer or laptop
- 4 GB RAM recommended
- At least 200 MB free disk space for the project and Python environment

### Software
- Windows 10/11, macOS, or Linux
- Python 3.10 or later recommended
- Visual Studio Code
- A modern web browser such as Chrome, Edge, or Firefox

---

## 4. Project Folder Structure

```text
library_management_system/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
│
├── auth.py
├── books.py
├── users.py
├── catalog.py
├── circulation.py
├── fines.py
├── reservations.py
├── reports.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── books.html
│   ├── users.html
│   ├── catalog.html
│   ├── circulation.html
│   ├── fines.html
│   └── reservations.html
│
└── static/
    ├── style.css
    └── app.js
```

The `library.db` database file is created automatically when the application is initialized. The `.venv` folder is created when you set up the virtual environment.

### Main files

- `app.py`: Creates the Flask app, registers the modules, protects application pages, and starts the local server.
- `database.py`: Creates database tables, opens SQLite connections, and inserts the initial administrator account.
- `requirements.txt`: Lists the Python packages required by the application.
- `templates/`: Contains the HTML pages.
- `static/`: Contains CSS and JavaScript files.

---

## 5. Installation and Setup in VS Code

### Step 1: Install Python

1. Visit https://www.python.org/downloads/
2. Download a stable Python release for your operating system.
3. Run the installer.
4. On Windows, select **Add Python to PATH** before installing.
5. Complete the installation.

Check the installation in a new terminal:

```powershell
python --version
```

If the `python` command is not recognized on Windows, try:

```powershell
py --version
```

If neither command works, reinstall Python and enable the PATH option.

### Step 2: Install VS Code

1. Visit https://code.visualstudio.com/
2. Download and install Visual Studio Code.
3. Open VS Code.
4. Open Extensions and install the Microsoft Python extension.

### Step 3: Extract and open the project

1. Download and extract the project ZIP.
2. Open VS Code.
3. Select **File → Open Folder**.
4. Select the extracted `library_management_system` folder.
5. Confirm that `app.py` is visible in the VS Code Explorer.

### Step 4: Open the terminal

Select **Terminal → New Terminal**.

### Step 5: Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

If only the Python Launcher works:

```powershell
py -m venv .venv
```

macOS/Linux:

```bash
python3 -m venv .venv
```

### Step 6: Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source .venv/bin/activate
```

The terminal should show `(.venv)` when the environment is active.

### Step 7: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 8: Run the application

Make sure the terminal is in the folder containing `app.py`, then execute:

```bash
python app.py
```

Open this address in your browser:

**http://127.0.0.1:5000**

Keep the terminal open while using the application. Press `Ctrl + C` in the terminal to stop the Flask server.

---

## 6. Default Administrator Login

During the first database initialization, the application creates an administrator account if the configured email does not already exist.

| Field | Default value |
|---|---|
| Email | `admin@library.local` |
| Password | `admin123` |
| Role | `admin` |

**Important:** This is a demonstration account. Change the default password before using the application with real data. Do not publish the default credentials.

---

## 7. Description of the Eight Modules

### Module 1: Login and Authentication

**Python file:** `auth.py`  
**HTML file:** `templates/login.html`

Functions:
- Login using email or name.
- Verify passwords using Werkzeug password hashing.
- Create a Flask session after successful login.
- Display an error for invalid credentials.
- Log out and clear the session.

Process:
1. The user enters their email/name and password.
2. The application searches for the user record.
3. The entered password is checked against the stored password hash.
4. If valid, a session is created and the user is redirected to the dashboard.
5. If invalid, an error message is displayed.

### Module 2: Book Management

**Python file:** `books.py`  
**HTML file:** `templates/books.html`

Functions:
- Add books.
- Store ISBN, title, author, category, publisher, and copy count.
- View the inventory.
- Delete books that have no linked borrowing or reservation records.

Book fields:

| Field | Description |
|---|---|
| ISBN | Unique book identifier; optional |
| Title | Name of the book |
| Author | Book author |
| Category | Subject or genre |
| Publisher | Publishing company |
| Total copies | Number of copies owned |
| Available copies | Number of copies currently available |

### Module 3: Student/User Management

**Python file:** `users.py`  
**HTML file:** `templates/users.html`

Functions:
- Create student accounts.
- Create librarian accounts.
- Create administrator accounts.
- Store name, email, phone, role, and password hash.
- Display registered users.
- Delete users who do not have linked library records.

Passwords are stored as hashes rather than plain text.

### Module 4: Book Search and Catalog

**Python file:** `catalog.py`  
**HTML file:** `templates/catalog.html`

Functions:
- Search by title.
- Search by author.
- Search by ISBN.
- Search by category.
- Display total and available copies.

The search uses SQL `LIKE` conditions to find partial matches.

### Module 5: Book Borrowing and Return

**Python file:** `circulation.py`  
**HTML file:** `templates/circulation.html`

Functions:
- Select an available book.
- Select a registered student.
- Set the borrowing period.
- Record issue and due dates.
- Decrease available stock when a book is issued.
- Record the return date.
- Increase available stock when a book is returned.
- Calculate overdue days and the applicable fine.

The default borrowing period is 14 days. The form accepts a period from 1 to 60 days.

### Module 6: Fine Management

**Python file:** `fines.py`  
**HTML file:** `templates/fines.html`

Functions:
- Display fine records.
- Show the student and related book.
- Show the fine amount.
- Mark an unpaid fine as paid.
- Display payment status.

The fine rate is configured in `database.py`:

```python
FINE_PER_DAY = 5.0
```

Calculation:

```text
Fine = Number of overdue days × Fine per day
```

Example:

```text
Overdue days = 3
Fine per day = ₹5
Total fine = 3 × ₹5 = ₹15
```

The current application records payment status manually. It does not process online payments.

### Module 7: Reservation and Notification

**Python file:** `reservations.py`  
**HTML file:** `templates/reservations.html`

Functions:
- Create a book reservation.
- Store the selected book and student.
- Display reservations.
- Cancel a waiting reservation.
- Create in-app notifications.
- Mark notifications as read.

Notifications are stored in SQLite. This version does not send email or SMS messages.

### Module 8: Dashboard and Reports

**Python file:** `reports.py`  
**HTML file:** `templates/dashboard.html`

Functions:
- Count book titles.
- Count total copies.
- Count students.
- Count currently borrowed books.
- Count overdue loans.
- Calculate unpaid fine totals.
- Display recent borrowing activity.
- Display book counts by category.

The dashboard retrieves its information from SQLite using SQL queries.

---

## 8. Database Design

The system uses SQLite, a lightweight relational database.

### Table: users

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | User name |
| email | TEXT | Unique email |
| phone | TEXT | Phone number |
| role | TEXT | admin, librarian, or student |
| password_hash | TEXT | Hashed password |

### Table: books

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| isbn | TEXT | Unique ISBN |
| title | TEXT | Book title |
| author | TEXT | Author |
| category | TEXT | Book category |
| publisher | TEXT | Publisher |
| total_copies | INTEGER | Total stock |
| available_copies | INTEGER | Available stock |

### Table: loans

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| book_id | INTEGER | Reference to books |
| user_id | INTEGER | Reference to users |
| issue_date | TEXT | Issue date |
| due_date | TEXT | Expected return date |
| return_date | TEXT | Actual return date |
| status | TEXT | borrowed or returned |

### Table: fines

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| loan_id | INTEGER | Related loan |
| user_id | INTEGER | Student reference |
| amount | REAL | Fine amount |
| paid | INTEGER | 0 = unpaid, 1 = paid |

### Table: reservations

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| book_id | INTEGER | Reserved book |
| user_id | INTEGER | Student reference |
| reserved_at | TEXT | Reservation date |
| status | TEXT | waiting, fulfilled, or cancelled |

### Table: notifications

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| user_id | INTEGER | Notification recipient |
| message | TEXT | Notification message |
| is_read | INTEGER | 0 = unread, 1 = read |
| created_at | TEXT | Creation timestamp |

### Database relationships

- One user can have multiple loan records.
- One book can have multiple loan records over time.
- Each fine is linked to a loan and a user.
- A user can create multiple reservations.
- A book can have multiple reservations.
- A user can receive multiple notifications.

---

## 9. Application Workflow

1. The administrator opens the website.
2. The administrator logs in.
3. The dashboard displays library statistics.
4. Books are added to the inventory.
5. Student accounts are created.
6. Books are searched through the catalog.
7. A book is issued to a student.
8. The system records the issue date and due date.
9. The book is returned and stock is updated.
10. An overdue fine is recorded when applicable.
11. A reservation can be created.
12. The dashboard displays updated library information.

---

## 10. Testing and Validation

| Test ID | Test case | Expected result |
|---|---|---|
| TC01 | Login with valid credentials | Dashboard opens |
| TC02 | Login with invalid credentials | Error message appears |
| TC03 | Add a book | Book appears in inventory |
| TC04 | Add a duplicate ISBN | Book insertion is rejected |
| TC05 | Register a student | User appears in user list |
| TC06 | Search by book title | Matching books appear |
| TC07 | Issue an available book | Loan is created and stock decreases |
| TC08 | Issue an unavailable book | Issue is rejected |
| TC09 | Return a borrowed book | Loan is marked returned and stock increases |
| TC10 | Return a book late | Fine is calculated |
| TC11 | Mark a fine as paid | Fine status changes to paid |
| TC12 | Create a reservation | Reservation and notification are created |
| TC13 | Cancel a waiting reservation | Status changes to cancelled |
| TC14 | Open dashboard | Statistics are displayed |

### Suggested testing procedure

1. Start the application.
2. Log in using the administrator account.
3. Add at least two books.
4. Register at least one student.
5. Search for a book.
6. Issue an available book.
7. Test a return.
8. In a development database, set a test loan's due date to a past date to test overdue fine calculation.
9. Check the fine record.
10. Create a reservation.
11. Verify the dashboard.

Do not change dates or records in a production library database for testing.

---

## 11. Troubleshooting

### Error: `py` is not recognized

Try:

```powershell
python --version
```

If Python is also not recognized, install Python and enable **Add Python to PATH**. Restart VS Code after installation.

### Error: `No module named flask`

Activate the virtual environment and run:

```bash
pip install -r requirements.txt
```

### Error: Template not found

Check that the `templates` folder is in the same project directory as `app.py`. Verify the HTML filename and spelling.

### CSS is not loading

Check that `style.css` is inside the `static` folder and that the base template links to it using Flask's `url_for('static', filename='style.css')`.

### Port 5000 is already in use

Stop the other application using port 5000, or change the final line of `app.py`:

```python
app.run(debug=True, port=5001)
```

Then open:

http://127.0.0.1:5001

### Database is locked

Close other programs or database viewers using the SQLite file. Stop and restart the Flask application.

### Forgot the administrator password

For a local development project, reset the administrator password using a Python script with `generate_password_hash`. Do not delete the database unless you are prepared to lose its records.

---

## 12. Security Considerations and Current Limitations

This project is an educational starter implementation, not a production-ready library platform.

Before public deployment, implement:

- Role-based access control on every protected route.
- CSRF protection for forms.
- Server-side validation for all inputs.
- A strong randomly generated Flask secret key stored outside source code.
- Login rate limiting and secure session cookie settings.
- HTTPS and a production WSGI server.
- Database backups and recovery procedures.
- Audit logs for book issues, returns, and fine payments.
- Transaction-safe stock and reservation handling.
- Tests for authorization and concurrent borrowing.

### Current implementation limitations

- All authenticated users can currently access the registered module routes; role permissions are not enforced.
- Reservations can be recorded and cancelled, but a queue is not automatically fulfilled when a book becomes available.
- Notifications are in-app database records only.
- Fine payments are manually marked as paid.
- Book and user edit forms are not included.
- PDF and Excel report exports are not included.
- Flask's development server with `debug=True` is intended only for local development.

---

## 13. Future Enhancements

1. Separate administrator, librarian, and student dashboards.
2. Student self-registration.
3. Edit and update operations for books and users.
4. Automatic reservation queue processing.
5. Email and SMS reminders.
6. PDF and Excel report generation.
7. Printable borrowing receipts.
8. Barcode or QR code scanning.
9. Online fine payment integration.
10. Advanced analytics and charts.
11. Password reset functionality.
12. Secure deployment to a hosting platform.

---

## 14. Conclusion

The Library Management System provides a modular approach to managing common library activities. It combines Python, Flask, HTML, CSS, JavaScript, and SQLite to provide a web-based application.

The eight modules organize the main operations: authentication, book management, user management, catalog search, borrowing and returns, fine management, reservations and notifications, and dashboard reporting.

The project demonstrates how a web application connects its frontend, backend, and database to manage information in a structured way. It can be used as a foundation for further development and academic project demonstrations.

---

## 15. Quick Reference: Commands

### Windows PowerShell

```powershell
# Create virtual environment
python -m venv .venv

# Activate environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Local website

http://127.0.0.1:5000

### Default local administrator

```text
Email: admin@library.local
Password: admin123
```

**End of Documentation**

