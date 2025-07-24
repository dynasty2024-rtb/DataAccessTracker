# **Data Access Tracker**


## **Project Overview**

The Data Access Tracker is an internal web application built with Flask designed to enhance data governance and accountability within an organization. It provides a centralized system for team members to log and track who accessed which dataset, when, and for what specific purpose. This tool is crucial for audits, compliance, and maintaining a clear historical record of data interactions.


## **Features**



* **User Login:** Secure authentication system to ensure only authorized personnel can access the application.
* **Dataset Selection:** A predefined list of datasets that users can select when logging an access event.
* **Access Log Entry:** A simple form to record details of data access, including the dataset, purpose, and automatic timestamping.
* **Access History View:** A comprehensive view of all logged data accesses, filterable by user and date range for easy auditing and reporting.


## **Setup Instructions**

Follow these steps to get the Data Access Tracker up and running on your local machine.


### **1. Prerequisites**



* Python 3.7+
* pip (Python package installer)


### **2. Project Structure**

Ensure your project directory is set up as follows:

data-access-tracker/ \
├── app.py \
└── templates/ \
    ├── base.html \
    ├── index.html \
    ├── login.html \
    └── history.html \



### **3. Installation**



1. **Clone the repository (if applicable) or create the project directory.**
2. **Navigate into your project directory:** \
cd data-access-tracker \

3. **Create a virtual environment (recommended):** \
python -m venv venv \

4. **Activate the virtual environment:**
    * **On Windows:** \
.\venv\Scripts\activate \

    * **On macOS/Linux:** \
source venv/bin/activate \

5. **Install the required Python packages:** \
pip install Flask Flask-SQLAlchemy Flask-Login Werkzeug \



### **4. Running the Application**



1. **Ensure your virtual environment is activated.**
2. **Run the Flask application:** \
python app.py \

3. The application will start on http://127.0.0.1:5000/ (or a similar address). Open this URL in your web browser.


## **Usage**


### **Default Credentials**

Upon the first run of app.py, a default administrator user will be created if one doesn't already exist.



* **Username:** admin
* **Password:** adminpass

**IMPORTANT:** Change this password immediately in a production environment!


### **Logging In**



1. Access the application in your browser (e.g., http://127.0.0.1:5000/).
2. You will be redirected to the login page.
3. Enter the default credentials (admin/adminpass) or any other user credentials you might create.


### **Logging Data Access**



1. After logging in, you will be on the Dashboard (/).
2. Select a dataset from the "Select Dataset" dropdown.
3. Enter a clear and concise "Purpose of Access" (e.g., "Auditing Q2 sales figures for quarterly report").
4. Click the "Log Access" button.
5. A success message will be displayed, and the log will be recorded.


### **Viewing Access History**



1. Click on the "Access History" link in the navigation bar.
2. On the history page, you can:
    * View all access logs in reverse chronological order.
    * **Filter by User:** Select a specific user from the "Filter by User" dropdown to see only their access logs.
    * **Filter by Date Range:** Use the "Start Date" and "End Date" fields to narrow down logs to a specific period.
3. Click "Apply Filters" to update the history view.


### **Logging Out**

Click the "Logout" button in the navigation bar to end your session.


## **Technologies Used**



* **Flask:** Python web framework
* **Flask-SQLAlchemy:** ORM for database interaction (SQLite by default)
* **Flask-Login:** User session management
* **Werkzeug:** Security utilities for password hashing
* **HTML5:** Structure of web pages
* **Tailwind CSS:** Utility-first CSS framework for styling
* **Jinja2:** Templating engine (integrated with Flask)


## **Future Improvements**



* **User Management:** Add features for creating, editing, and deleting users (beyond the initial admin).
* **Dataset Management:** Allow administrators to add, edit, and remove datasets via a web interface.
* **User Roles:** Implement different user roles (e.g., "Auditor" who can only view logs, "Data Steward" who can manage datasets).
* **Improved Validation:** More robust server-side and client-side form validation.
* **Pagination:** For large datasets, implement pagination on the history page.
* **Search Functionality:** Add a search bar to filter logs by keywords in the purpose or dataset name.
* **Export Functionality:** Allow exporting access logs (e.g., to CSV).
* **Enhanced UI/UX:** Further refine the user interface for better usability and aesthetics.
* **Database Migration Tool:** Use Flask-Migrate for managing database schema changes.
* **Deployment Ready:** Configure for production deployment (e.g., Gunicorn, Nginx, PostgreSQL).