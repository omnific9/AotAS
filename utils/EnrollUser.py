__author__ = 'Langxuan'

import MySQLdb

class Dbclass:
    def __init__(self):

        self.conn = MySQLdb.connect (host = "127.0.0.1",
                               user = "root",
                               passwd = "root",
                               db = "james")
        self.cursor = self.conn.cursor()

    def setuser(self, userid, condition, email):
        self.cursor.execute("INSERT INTO users (user_id,start_date,study_condition,email,interaction_day,last_login) VALUES (\'"+userid+"\',DATE(NOW()),\'"+condition+"\',\'"+email+"\',0,\'2014-01-01\')")
        self.conn.commit()

    def setusersoc(self, userid, soc):
        self.cursor.execute("INSERT INTO globalvars (user_id,study_day,varkey,varvalue) VALUES (\'"+userid+"\',0,\'soc\',\'"+soc+"\')")
        self.conn.commit()

    def closeDB(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":

    db = Dbclass()

    username = raw_input("Please type in the user name: ")
    while len(username) > 16:
        print "Please limit the user name within 16 characters."
        username = raw_input("Please type in the user name: ")
    db.cursor.execute("SELECT * FROM users where user_id LIKE \'"+username+"____\'")
    row = db.cursor.fetchone()
    while row:
        username = raw_input("The user name already exists. Please type in another name: ")
        while len(username) > 16:
            print "Please limit the user name within 16 characters."
            username = raw_input("Please type in the user name: ")
        db.cursor.execute("SELECT * FROM users where user_id LIKE \'"+username+"____\'")
        row = db.cursor.fetchone()
    pin = raw_input("Please type in the user\'s chosen PIN: ")
    while len(pin) != 4:
        print "Please choose a PIN with exactly four digits"
        pin = raw_input("Please type in the user\'s chosen PIN: ")
    soc = raw_input("Please type in the user\'s stage of change (pc, c, p, a, or m): ")
    while soc != 'pc' and soc!='c' and soc!='p' and soc!= 'a' and soc!='m':
        print "Please type in the user\'s stage of change in abbreviated form: pc for Precontemplation, c for Contemplation, p for Preparation, a for Action, and m for Maintenance."
        soc = raw_input("Please type in the user\'s stage of change (pc, c, p, a, or m): ")
    cond = raw_input("Please type in the user\'s study condition (HWNL, NONC, CONT, or FULL): ")
    while cond != 'HWNL' and cond != 'NONC' and cond != 'CONT' and cond != 'FULL':
        print "Please type in the user\'s study condition in abbreviated form: HWNL for Homework-Only, NONC for Non-Contingency, CONT for Contingency, and FULL for Full-Interaction."
        cond = raw_input("Please type in the user\'s study condition (HWNL, NONC, CONT, or FULL): ")
    email = raw_input("Please type in the user\'s email: ")
    email2 = raw_input("Please type in the user\'s email again: ")
    while email != email2:
        print "The two email addresses do not match. Please retype the email."
        email = raw_input("Please type in the user\'s email: ")
        email2 = raw_input("Please type in the user\'s email again: ")

    db.setuser(username+pin, cond, email)
    db.setusersoc(username+pin, soc)
    db.closeDB()

    d = raw_input("User data set successfully. Press Enter to exit.")