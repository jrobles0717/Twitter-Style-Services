from flask import jsonify
from model.Posts import PostsDAO

class BasePosts:

    def build_map_dict(self,row):
        result = {}
        result['message_id'] = row[0]
        result['user_id'] = row[1]
        result['message_likes'] = row[2]
        result['message_reads'] = row[3]
        result['message_shares'] = row[4]
        result['message_replies'] = row[5]
        result['message_content'] = row[6]
        return result

    def build_attr_map(self, mid, uid, cont, rid):
        result = {}
        result["message_id"] = mid
        result["user_id"] = uid
        result["message_likes"] = 0
        result["message_reads"] = 0
        result["message_shares"] = 0
        result["message_replies"] = 0
        result["message_content"] = cont
        if rid > 0:
            result["replying_to"] = rid
        return result

    def newPost(self, json):
        uid = json['RegisteredUser']
        cont = json['Text']
        dao = PostsDAO()
        mid = dao.newPost(uid,cont)
        result = self.build_attr_map(mid, uid, cont, 0)
        return jsonify(result), 201

    def getMsg(self):
        dao = PostsDAO()
        post_list = dao.getMsg()
        result_list = []
        for row in post_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getMsgId(self, mid):
        dao = PostsDAO()
        msg = dao.getMsgId(mid)
        if not msg:
            return jsonify("Message not found"), 404
        else:
            result = self.build_map_dict(msg)
            return jsonify(result)

    def reply(self, json):
        uid = json['RegisteredUser']
        mid = json["replyingto"]
        cont = json["Text"]
        dao = PostsDAO()
        rid = dao.reply(uid,mid,cont)
        result = self.build_attr_map(rid, uid, cont, mid)
        return jsonify(result), 201

    def share(self, json):
        uid = json['RegisteredUser']
        mid = json['sharing']
        dao = PostsDAO()
        cont = dao.share(uid,mid)
        result = self.build_attr_map(mid, uid, cont, 0)
        return jsonify(result)

    def getLiked(self, mid):
        dao = PostsDAO()
        user_list = dao.getLiked(mid)
        result_list = []
        for row in user_list:
            result_list.append(row)
        return jsonify(result_list)

    def getLike(self, json, mid):
        dao = PostsDAO()
        uid = json['RegisteredUser']
        result = dao.getLike(mid, uid)
        if result:
            return jsonify("Like Message"), 200
        else:
            return jsonify("Something went wrong"), 404

    def getLikeRemoved(self, json, mid):
        dao = PostsDAO()
        uid = json['RegisteredUser']
        result = dao.getLikeRemoved(mid, uid)
        if result:
            return jsonify("Like Removed from Message"), 200
        else:
            return jsonify("Something went wrong"), 404

    def getUnlike(self, json, mid):
        dao = PostsDAO()
        uid = json['RegisteredUser']
        result = dao.getUnlike(mid, uid)
        if result:
            return jsonify("Unlike Message"), 200
        else:
            return jsonify("Something went wrong"), 404

    def getUnliked(self, mid):
        dao = PostsDAO()
        user_list = dao.getUnliked(mid)
        result_list = []
        for row in user_list:
            result_list.append(row)
        return jsonify(result_list)

    def getUnlikeRemoved(self, json, mid):
        dao = PostsDAO()
        uid = json['RegisteredUser']
        result = dao.getUnlikeRemoved(mid, uid)
        if result:
            return jsonify("Unlike Removed from Message"), 200
        else:
            return jsonify("Something went wrong"), 404

