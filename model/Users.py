from config.dbconfig import pg_config
import psycopg2

class UsersDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'], pg_config['user'],
                                                                                     pg_config['password'], pg_config['dbport'],
                                                                            pg_config['dbhost'])
        self.conn = psycopg2.connect(connection_url)

    def newUser(self, user_name, user_lastname, user_username, user_email, user_password):
        cursor = self.conn.cursor()
        query = "insert into users (user_name, user_lastname, user_username, user_email, user_password)" \
                "values (%s, %s, %s, %s, %s) returning user_id;"
        cursor.execute(query, (user_name, user_lastname, user_username, user_email, user_password,))
        uid = cursor.fetchone()[0]
        self.conn.commit()
        return uid

    def updateUser(self, uid, user_name, user_lastname, user_username, user_email, user_password):
        cursor = self.conn.cursor()
        query = "update users set user_name=%s, user_lastname=%s, user_username=%s, user_email=%s, user_password=%s where user_id=%s;"
        cursor.execute(query, (user_name, user_lastname, user_username, user_email, user_password, uid,))
        self.conn.commit()
        return True

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select * from users;"
        cursor.execute(query)
        result=[]
        for row in cursor:
            result.append(row)
        return result

    def getUserId(self, uid):
        cursor = self.conn.cursor()
        query = "select * from users where user_id = %s;"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    def deleteUser(self, uid):
        self.deleteMsg(uid)
        cursor = self.conn.cursor()
        query = "delete from users where user_id = %s;"
        cursor.execute(query, (uid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0

    def follow(self, follower, uid):
        cursor = self.conn.cursor()
        query = "insert into follow (follower, followed) select %s, %s where not exists (select fid from follow where " \
                "follower = %s and followed = %s) returning fid;"
        cursor.execute(query, (follower,uid,follower, uid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0

    def block(self, blocker, uid):
        cursor = self.conn.cursor()
        query = "insert into block (blocker, blocked) select %s, %s where not exists (select bid from block where " \
                "blocker = %s and blocked = %s) returning bid;"
        cursor.execute(query, (blocker,uid,blocker,uid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0

    def getFollowedBy(self, uid):
        cursor = self.conn.cursor()
        query = "select user_name, user_lastname, user_username from users inner join follow on user_id=followed where follower=%s;"
        cursor.execute(query, (uid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getFollows(self, uid):
        cursor = self.conn.cursor()
        query = "select user_name, user_lastname, user_username from users inner join follow on user_id=follower where followed=%s;"
        cursor.execute(query, (uid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def blockedBy(self, uid):
        cursor = self.conn.cursor()
        query = "select user_name, user_lastname, user_username from users inner join block on user_id=blocked where blocker=%s;"
        cursor.execute(query, (uid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def blocking(self, uid):
        cursor = self.conn.cursor()
        query = "select user_name, user_lastname, user_username from users inner join block on user_id=blocker where blocked=%s;"
        cursor.execute(query, (uid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def unfollow(self, follower, uid):
        cursor = self.conn.cursor()
        query = "delete from follow where follower = %s and followed = %s;"
        cursor.execute(query, (follower,uid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0
    
    def unblock(self, blocker, uid):
        cursor = self.conn.cursor()
        query = "delete from block where blocker = %s and blocked = %s;"
        cursor.execute(query, (blocker,uid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0

    def deleteMsg(self, uid): #has to be updated to fix other message values
        cursor = self.conn.cursor()
        query = "select distinct is_reply, count(is_reply) from message where user_id = %s group by is_reply;"
        cursor.execute(query,(uid,))
        result = []
        for row in cursor:
            result.append(row)
        query = "update message set message_replies = message_replies - %s where message_id = %s;"
        for x in result:
            cursor.execute(query,(x[1],x[0],))
        self.conn.commit()