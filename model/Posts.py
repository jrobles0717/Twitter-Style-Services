from config.dbconfig import pg_config
import psycopg2

class PostsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'], pg_config['user'],
                                                                            pg_config['password'], pg_config['dbport'],
                                                                            pg_config['dbhost'])
        self.conn = psycopg2.connect(connection_url)

    def newPost(self, uid, cont):
        cursor = self.conn.cursor()
        query = "insert into message (user_id, message_content) values (%s, %s) returning message_id;"
        cursor.execute(query, (uid,cont,))
        mid = cursor.fetchone()[0]
        self.conn.commit()
        self.userPosted(uid)
        return mid

    def getMsg(self):
        cursor = self.conn.cursor()
        query = "select * from message;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMsgId(self, mid):
        cursor = self.conn.cursor()
        query = "select * from message where message_id=%s;"
        cursor.execute(query, (mid,))
        result = cursor.fetchone()
        return result

    def reply(self, uid, mid, cont):
        cursor = self.conn.cursor()
        query = "insert into message (user_id, message_content, is_reply) values (%s, %s, %s) returning message_id;"
        cursor.execute(query,(uid, cont, mid,))
        rid = cursor.fetchone()[0]
        query = "update message set message_replies = message_replies + 1 where message_id = %s;"
        cursor.execute(query,(mid,))
        self.conn.commit()
        self.userPosted(uid)
        return rid

    def share(self, uid, mid):
        cursor = self.conn.cursor()
        query = "update message set message_shares = message_shares + 1 where message_id = %s returning message_content;"
        cursor.execute(query, (mid,))
        cont = cursor.fetchone()[0]
        query = "insert into share (user_id, message_id) values (%s, %s)"
        cursor.execute(query, (uid, mid,))
        self.conn.commit()
        return cont


    def getLiked(self, mid):
        cursor = self.conn.cursor()
        query = "select liker_id from likes where message_id=%s;"
        cursor.execute(query, (mid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getLike(self, mid, likerid):
        cursor = self.conn.cursor()
        query = "insert into likes (message_id, liker_id) select %s, %s where not exists (select like_id from likes where " \
                "message_id = %s and liker_id = %s) returning like_id;"
        cursor.execute(query, ( mid, likerid, mid, likerid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0

    def getLikeRemoved(self, mid, likerid):
        cursor = self.conn.cursor()
        query = "delete from likes where message_id = %s and liker_id = %s;"
        cursor.execute(query, ( mid, likerid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0

    def getUnlike(self, mid, unlikerid):
        cursor = self.conn.cursor()
        query = "insert into unlikes (message_id, unliker_id) select %s, %s where not exists (select unlike_id from unlikes where " \
                "message_id = %s and unliker_id = %s) returning unlike_id;"
        cursor.execute(query, ( mid, unlikerid, mid, unlikerid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0

    def getUnliked(self, mid):
        cursor = self.conn.cursor()
        query = "select unliker_id from unlikes where message_id=%s;"
        cursor.execute(query, (mid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUnlikeRemoved(self, mid, unlikerid):
        cursor = self.conn.cursor()
        query = "delete from unlikes where message_id = %s and unliker_id = %s;"
        cursor.execute(query, ( mid, unlikerid,))
        affected = cursor.rowcount
        self.conn.commit()
        return affected != 0

    def userPosted(self, uid):
        cursor = self.conn.cursor()
        query = "update users set user_posts = user_posts + 1 where user_id = %s;"
        cursor.execute(query,(uid,))
        self.conn.commit()