import pymysql
import json
import datetime


class Db:

    def open(self):
        """Connect to database"""

        self.conn = pymysql.connect(host='fit-rds.c4saqtb91ywf.eu-west-1.rds.amazonaws.com',
            user='#########',
            password='#############',
            db='##########',
            charset='utf8',)

    # --------------------------------------------------------------------------------------------- #
    def close(self):
        """Close connection"""

        self.conn.close()

    # --------------------------------------------------------------------------------------------- #
    def get_client_exercise(self, email):
        """Get client exercise info"""

        # Get client ID
        id = self.get_client_id(email)

        # Connecting to DB.
        self.open()

        # Creating cursor.
        c = self.conn.cursor()

        # Constructing SQL query.
        query = "SELECT exercise, date, reps FROM exercise_numbers WHERE id = '" + str(id) + "' ORDER BY exercise, date;"

        # Executing SQL query.
        c.execute(query)

        # Disconnecting from DB.
        self.close()

        # Make empty list
        answer = []

        for row in c:
            answer.append([row[0], str(row[1]), row[2]])

        return answer

    # --------------------------------------------------------------------------------------------- #
    def format_exercise_for_json(self, email):
        """Get client exercise info"""

        # get un-parsed json data
        info = self.get_client_exercise(email)

        # Create empty lists for each exercise
        push_ups = []
        pull_ups = []
        squats = []
        leg_raises = []

        for i in range(len(info)):
            if info[i][0] == "push_ups":
                push_ups.append([info[i][1], info[i][2]])
            if info[i][0] == "pull_ups":
                pull_ups.append([info[i][1], info[i][2]])
            if info[i][0] == "squats":
                squats.append([info[i][1], info[i][2]])
            if info[i][0] == "legraises":
                leg_raises.append([info[i][1], info[i][2]])

        answer = {"push_ups": push_ups,
                "pull_ups": pull_ups,
                "squats": squats,
                "leg_raises": leg_raises}

        return json.dumps(answer)

    # --------------------------------------------------------------------------------------------- #
    def get_client_name(self, email):
        """Get client name info"""

        # Get ID
        id = Db().get_client_id(email)

        # Connecting to DB.
        self.open()

        # Creating cursor.
        c = self.conn.cursor()

        # Constructing SQL query to get first and last name based on ID
        query = "SELECT firstname, lastname FROM client_info WHERE id = '" + id + "';"

        # Executing SQL query.
        c.execute(query)

        # Disconnecting from DB.
        self.close()

        # Make empty list
        answer = []

        for row in c:
            answer.append([row[0], row[1]])

        return json.dumps(answer)

    # --------------------------------------------------------------------------------------------- #
    def post_info(self, fname, lname, email):
        """Post Client Information to Database"""

        # Connecting to DB.
        self.open()

        # Creating cursor.
        c = self.conn.cursor()

        # Constructing SQL query.
        query = "INSERT INTO client_info VALUES (NULL, '" + fname + "', '" + lname + "', '" + email + "')"

        try:
            # Execute the SQL command
            c.execute(query)
        except TypeError:
            self.conn.close()
            print("Error: Please use correct data types...")
        else:
            # Commit your changes in the database
            self.conn.commit()
            self.conn.close()

    # --------------------------------------------------------------------------------------------- #
    def post_workout_info(self, email, exercise, set1, set2, set3):
        """Post Client Workout Information to Database"""

        # Get the current date in string format
        now = datetime.datetime.now()
        date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

        # Get client ID
        id = Db().get_client_id(email)

        print(date, id)

        # Convert sets to one string
        reps = str(set1) + "-" + str(set2) + "-" + str(set3)

        # Connecting to DB.
        self.open()

        # Creating cursor.
        c = self.conn.cursor()

        # Constructing SQL query.
        query = "INSERT INTO exercise_numbers VALUES ('" + str(id) + "', '" + date + "', '" + exercise + "', '" + reps + "')"

        try:
            # Execute the SQL command
            c.execute(query)
        # Catch integrity and type errors
        except (pymysql.IntegrityError, TypeError) as e:
            print("MY ERROR: ",  e)
            self.conn.close()
        else:
            # Commit your changes in the database if no errors raised
            self.conn.commit()
            self.conn.close()

    # --------------------------------------------------------------------------------------------- #
    def get_client_id(self, email):
        """Return client id based on email"""

        # Connecting to DB.
        self.open()

        # Creating cursor.
        c = self.conn.cursor()

        # Constructing SQL query.
        query = "SELECT id FROM client_info WHERE email = '" + email + "';"

        # Execute the SQL command
        c.execute(query)

        # Close Connection
        self.conn.close()

        answer = []

        for item in c:
            answer.append(item)

        return answer[0][0]
