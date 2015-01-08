__author__ = 'Langxuan'

import MySQLdb

class Dbclass:
    def __init__(self):

        self.conn = MySQLdb.connect (host = "127.0.0.1",
                               user = "root",
                               passwd = "agents",
                               db = "james")
        self.cursor = self.conn.cursor()

    def setuserid(self, userid):
        self.user_id = userid
        self.getStudyDay()
        self.setStudyDay()

    def checkuserid(self, userid):
        self.cursor.execute("select study_condition, DATEDIFF(DATE(NOW()),last_login), interaction_day from users where user_id='"+userid+"'")
        row = self.cursor.fetchone()
        if row is None:
            return 'failure'
        elif row[2] > 20:
            return 'failure'
        elif row[1] == 0:
            return 'tomorrow'
        return row[0]

    def getStudyDay(self):
        self.cursor.execute("select datediff(now(),start_date) from users where user_id='"+self.user_id+"'")
        row = self.cursor.fetchone()
        self.study_day = row[0]

    def setStudyDay(self):
        self.cursor.execute("update users set study_day="+str(self.study_day)+" where user_id='"+str(self.user_id)+"'")
        self.conn.commit()

    def setInteractionDay(self, globalvars):
        self.cursor.execute("update users set interaction_day="+str(globalvars.get('interactionday'))+" where user_id='"+str(self.user_id)+"'")
        self.conn.commit()

    def writeGlobalvars(self, globalvars):
        globalvars.pop('curmotivation',None)
        globalvars.pop('connphrase',None)
        for key in globalvars:
            query = "replace into globalvars (user_id,study_day,varkey,varvalue) values ('"+self.user_id+"',"+str(self.study_day)+",'"+key+"','"+str(globalvars.get(key))+"')"
            print query
            self.cursor.execute(query)
            self.conn.commit()

    def readGlobalvars(self):
        self.cursor.execute("select varkey,varvalue from globalvars where user_id='"+self.user_id+"' and study_day=(select max(study_day) from globalvars where user_id='"+self.user_id+"')")
        dict = {}
        for row in self.cursor.fetchall():
            newdict = {row[0]:row[1]}
            dict.update(newdict)
        return dict

    def writeMotivations(self, motivation):
        for key in motivation:
            self.cursor.execute("replace into motivation (user_id,study_day,motivation,rating) values ('"+self.user_id+"',"+str(self.study_day)+",'"+key+"','"+str(motivation.get(key))+"')")
            self.conn.commit()

    def readMotivations(self):
        self.cursor.execute("select motivation,rating from motivation where user_id='"+self.user_id+"' and study_day=(select max(study_day) from motivation where user_id='"+self.user_id+"')")
        dict = {}
        for row in self.cursor.fetchall():
            newdict = {row[0]:row[1]}
            dict.update(newdict)
        return dict

    def getUsedFiles(self):
        self.cursor.execute("select filename from usedfiles where user_id='"+self.user_id+"'")
        usedfiles=[]
        for row in self.cursor.fetchall():
            usedfiles.append(row[0])
        return usedfiles

    def updateUsedFiles(self, newusedfiles):
        for key in newusedfiles:
            self.cursor.execute("replace into usedfiles (user_id,filename,day_used) values ('"+self.user_id+"','"+key+"',"+str(self.study_day)+")")
            self.conn.commit()

    def updateLoginInfo(self):
        self.cursor.execute("update users set last_login=DATE(NOW()) where user_id='"+str(self.user_id)+"'")
        self.conn.commit()

    def setLog(self, logstring):
        logstring = logstring.replace('\'','#quot#')
        self.cursor.execute("insert into logs (user_id,log_entry,log_time) values ('"+self.user_id+"','"+logstring+"',now())")
        self.conn.commit()

    def closeDB(self):
        self.cursor.close()
        self.conn.close()
