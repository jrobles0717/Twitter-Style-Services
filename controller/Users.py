from flask import jsonify
from model.Users import UsersDAO

class BaseUsers:

    def build_map_dict(self,row):
        result = {}
        result['user_id'] = row[0]
        result['user_name'] = row[1]
        result['user_lastname'] = row[2]
        result['user_username'] = row[3]
        result['user_email'] = row[4]
        result['user_password'] = row[5]
        result['user_follows'] = row[6]
        result['user_followers'] = row[7]
        result['user_notification'] = row[8]
        result['user_block'] = row[9]
        result['user_posts'] = row[10]
        return result

    def build_attr_dict(self, uid, user_name, user_lastname, user_username, user_email, user_password):
        result = {}
        result['user_id'] = uid
        result['user_name'] = user_name
        result['user_lastname'] = user_lastname
        result['user_username'] = user_username
        result['user_email'] = user_email
        result['user_password'] = user_password
        result['user_follows'] = 0
        result['user_followers'] = 0
        result['user_notification'] = 0
        result['user_block'] = 0
        result['user_posts'] = 0
        return result

    def newUser(self, json):
        user_name = json['user_name']
        user_lastname = json['user_lastname']
        user_username = json['user_username']
        user_email = json['user_email']
        user_password = json['user_password']
        dao = UsersDAO()
        uid = dao.newUser(user_name, user_lastname, user_username, user_email, user_password)
        result = self.build_attr_dict(uid, user_name, user_lastname, user_username, user_email, user_password)
        return jsonify(result), 201

    def updateUser(self, json, uid):
        user_name = json['user_name']
        user_lastname = json['user_lastname']
        user_username = json['user_username']
        user_email = json['user_email']
        user_password = json['user_password']
        dao = UsersDAO()
        updated = dao.updateUser(uid, user_name, user_lastname, user_username, user_email, user_password)
        result = self.build_attr_dict(uid, user_name, user_lastname, user_username, user_email, user_password)
        return jsonify(result), 200

    def getAllUsers(self):
        dao = UsersDAO()
        user_list = dao.getAllUsers()
        result_list = []
        for row in user_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getUserId(self, uid):
        dao = UsersDAO()
        user = dao.getUserId(uid)
        if not user:
            return jsonify("User not found"), 404
        else:
            result = self.build_map_dict(user)
            return jsonify(result)

    def deleteUser(self, uid):
        dao = UsersDAO()
        result = dao.deleteUser(uid)
        if result:
            return jsonify("User Deleted"), 200
        else:
            return jsonify("User not found"), 404

    def follow(self, json, uid):
        dao = UsersDAO()
        follower = json['RegisteredUser']
        result = dao.follow(follower, uid)
        if result:
            return jsonify("User Followed"), 200
        else:
            return jsonify("Something went wrong"), 404

    def block(self, json, uid):
        dao = UsersDAO()
        blocker = json['RegisteredUser']
        result = dao.block(blocker, uid)
        if result:
            return jsonify("User Blocked"), 200
        else:
            return jsonify("Something went wrong"), 404

    def getFollowedBy(self, uid):
        dao = UsersDAO()
        user_list = dao.getFollowedBy(uid)
        result_list = []
        for row in user_list:
            result_list.append(row)
        return jsonify(result_list)

    def getFollows(self, uid):
        dao = UsersDAO()
        user_list = dao.getFollows(uid)
        result_list = []
        for row in user_list:
            result_list.append(row)
        return jsonify(result_list)

    def blockedBy(self, uid):
        dao = UsersDAO()
        user_list = dao.blockedBy(uid)
        result_list = []
        for row in user_list:
            result_list.append(row)
        return jsonify(result_list)

    def blocking(self, uid):
        dao = UsersDAO()
        user_list = dao.blocking(uid)
        result_list = []
        for row in user_list:
            result_list.append(row)
        return jsonify(result_list)

    def unfollow(self, json, uid):
        dao = UsersDAO()
        follower = json['RegisteredUser']
        result = dao.unfollow(follower, uid)
        if result:
            return jsonify("User Unfollowed"), 200
        else:
            return jsonify("Something went wrong"), 404

    def unblock(self, json, uid):
        dao = UsersDAO()
        blocker = json['RegisteredUser']
        result = dao.unblock(blocker, uid)
        if result:
            return jsonify("User Unblocked"), 200
        else:
            return jsonify("Something went wrong"), 404
