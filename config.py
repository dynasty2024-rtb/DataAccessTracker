app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key_that_should_be_changed')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False