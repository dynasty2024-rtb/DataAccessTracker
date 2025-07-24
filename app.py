# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta # Import timedelta here
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config.from_pyfile('config.py')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to login page if user is not logged in

# --- Context Processor for Jinja2 Templates ---
@app.context_processor
def inject_datetime():
    """
    Injects the datetime module into all Jinja2 templates.
    This allows templates to use datetime.now() for displaying the current year, etc.
    """
    return dict(datetime=datetime)

# --- Database Models ---

class User(UserMixin, db.Model):
    """
    User model for authentication.
    - id: Primary key
    - username: Unique username for login
    - password_hash: Hashed password for security
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Dataset(db.Model):
    """
    Dataset model to store available datasets.
    - id: Primary key
    - name: Name of the dataset
    - description: Optional description of the dataset
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Dataset {self.name}>'

class AccessLog(db.Model):
    """
    AccessLog model to record data access events.
    - id: Primary key
    - user_id: Foreign key to User model (who accessed)
    - dataset_id: Foreign key to Dataset model (which dataset was accessed)
    - access_time: Timestamp of access
    - purpose: Reason for access
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    access_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    purpose = db.Column(db.Text, nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('access_logs', lazy=True))
    dataset = db.relationship('Dataset', backref=db.backref('access_logs', lazy=True))

    def __repr__(self):
        return f'<AccessLog User:{self.user_id} Dataset:{self.dataset_id} Time:{self.access_time}>'

# --- Flask-Login User Loader ---

@login_manager.user_loader
def load_user(user_id):
    """Loads a user from the database given their ID."""
    return db.session.get(User, int(user_id))

# --- Routes ---

@app.route('/')
@login_required
def index():
    """
    Dashboard/Home page. Allows users to log data access.
    Displays a form to select a dataset and enter the purpose.
    """
    datasets = Dataset.query.all()
    return render_template('index.html', datasets=datasets)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page.
    Handles both GET (display form) and POST (process login).
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/log_access', methods=['POST'])
@login_required
def log_access():
    """
    Handles the submission of a new access log entry.
    Requires dataset_id and purpose from the form.
    """
    dataset_id = request.form['dataset']
    purpose = request.form['purpose']

    if not dataset_id or not purpose:
        flash('Please select a dataset and provide a purpose.', 'danger')
        return redirect(url_for('index'))

    try:
        dataset = db.session.get(Dataset, int(dataset_id))
        if not dataset:
            flash('Selected dataset does not exist.', 'danger')
            return redirect(url_for('index'))

        new_log = AccessLog(
            user_id=current_user.id,
            dataset_id=dataset.id,
            purpose=purpose
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Access logged successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error logging access: {e}', 'danger')

    return redirect(url_for('index'))

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    """
    Displays the access history.
    Allows filtering by user and date range.
    """
    query = AccessLog.query.order_by(AccessLog.access_time.desc())
    users = User.query.all() # For filter dropdown

    filter_user_id = request.args.get('user_id')
    filter_start_date = request.args.get('start_date')
    filter_end_date = request.args.get('end_date')

    if filter_user_id and filter_user_id != 'all':
        query = query.filter(AccessLog.user_id == int(filter_user_id))

    if filter_start_date:
        try:
            start_dt = datetime.strptime(filter_start_date, '%Y-%m-%d')
            query = query.filter(AccessLog.access_time >= start_dt)
        except ValueError:
            flash('Invalid start date format. Please use YYYY-MM-DD.', 'warning')

    if filter_end_date:
        try:
            end_dt = datetime.strptime(filter_end_date, '%Y-%m-%d')
            # Add one day to include logs from the end_date itself
            query = query.filter(AccessLog.access_time < end_dt + timedelta(days=1))
        except ValueError:
            flash('Invalid end date format. Please use YYYY-MM-DD.', 'warning')

    access_logs = query.all()

    return render_template(
        'history.html',
        access_logs=access_logs,
        users=users,
        selected_user_id=filter_user_id,
        selected_start_date=filter_start_date,
        selected_end_date=filter_end_date
    )

# --- Database Initialization and Sample Data ---

# Removed @app.before_first_request as it's deprecated/removed in newer Flask versions.
# The `create_tables()` function is now called directly within the `if __name__ == '__main__':` block,
# which ensures it runs once when the script is executed.
def create_tables():
    """
    Creates database tables and adds sample data if they don't exist.
    This runs once when the app starts.
    """
    db.create_all()

    # Add a default admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin')
        admin_user.set_password('adminpass') # CHANGE THIS IN PRODUCTION!
        db.session.add(admin_user)
        db.session.commit()
        print("Added default admin user: admin/adminpass")

    # Add sample datasets if not exists
    if not Dataset.query.first():
        datasets_to_add = [
            Dataset(name='Customer_Database', description='Contains customer personal and order information.'),
            Dataset(name='Sales_Figures_Q1_2024', description='Quarterly sales data for Q1 2024.'),
            Dataset(name='Marketing_Campaign_Results', description='Performance metrics for recent marketing campaigns.'),
            Dataset(name='Product_Inventory', description='Current stock levels and product details.')
        ]
        db.session.bulk_save_objects(datasets_to_add)
        db.session.commit()
        print("Added sample datasets.")

if __name__ == '__main__':
    # Ensure the database and initial data are set up within the application context
    with app.app_context():
        create_tables()
    app.run(debug=True) # Run in debug mode for development

