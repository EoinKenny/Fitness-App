from flask import Flask, render_template, request
from flask_cors import CORS
from get_fit.db_main import Db


# --------------------------------------------------------------------------#
# Creating Flask App
app = Flask(__name__)
# Enable Cross Origin Resource Sharing
CORS(app)


# --------------------------------------------------------------------------#
# Index Page
@app.route('/')
def index():
    return render_template('index.html')


# --------------------------------------------------------------------------#
# For posting sensitive client information to database
@app.route('/_sign_up', methods=['POST'])
def sign_up():
    # Get Form Data From URL
    first_name_signup = request.form['firstNameSignUp']
    last_name_signup = request.form['lastNameSignUp']
    email_address_signup = request.form['emailAddressSignUp']

    # If credentials are all entered then submit to database
    if first_name_signup and last_name_signup and email_address_signup:
        Db().post_info(first_name_signup, last_name_signup, email_address_signup)
        return render_template('index.html')

    return render_template('index.html')


# --------------------------------------------------------------------------#
# For posting workout information to database
@app.route('/_log_workout', methods=['POST'])
def log_workout():

    # Get Form Data From URL
    email_log_workout = request.form['email_log_workout']
    options = request.form['options']
    set1 = request.form['set1']
    set2 = request.form['set2']
    set3 = request.form['set3']

    # Check if the data exists before submitting to database
    if email_log_workout and options and set1 and set2 and set3:
        Db().post_workout_info(email_log_workout, options, set1, set2, set3)
        return render_template('index.html')

    return render_template('index.html')


# --------------------------------------------------------------------------#
# For getting workout information for google chart
@app.route('/_get_workouts/<string:email>', methods=['GET'])
def get_chart_info(email):
    # Get Form Data From URL
    return Db().format_exercise_for_json(email)


# --------------------------------------------------------------------------#
# Setting app to run only if this file is run directly.
if __name__ == '__main__':
    app.run(debug=True)
