from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.Users import BaseUsers
from controller.Posts import BasePosts

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/bdbge/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        return BaseUsers().newUser(request.json)
    else:
        return BaseUsers().getAllUsers()

@app.route('/bdbge/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def spec_user(uid):
    if request.method == 'PUT':
        return BaseUsers().updateUser(request.json, uid)
    elif request.method == 'DELETE':
        return BaseUsers().deleteUser(uid)
    else:
        return BaseUsers().getUserId(uid)

@app.route('/bdbge/follow/<int:uid>', methods=['POST'])
def follow(uid):
    if request.method == 'POST':
        return BaseUsers().follow(request.json,uid)
    else:
        return "An error has occurred"

@app.route('/bdbge/block/<int:uid>', methods=['POST'])
def block(uid):
    return BaseUsers().block(request.json,uid)

@app.route('/bdbge/followedby/<int:uid>', methods=['GET'])
def followedBy(uid):
    if request.method == 'GET':
        return BaseUsers().getFollowedBy(uid)
    else:
        return "An error has occurred"

@app.route('/bdbge/follows/<int:uid>', methods=['GET'])
def getFollows(uid):
    if request.method == 'GET':
        return BaseUsers().getFollows(uid)
    else:
        return "An error has occurred"

@app.route('/bdbge/unfollow/<int:uid>', methods=['POST'])
def unfollow(uid):
    if request.method == 'POST':
        return BaseUsers().unfollow(request.json,uid)
    else:
        return "An error has occurred"

@app.route('/bdbge/blockedby/<int:uid>', methods=['GET'])
def blockedBy(uid):
    return BaseUsers().blockedBy(uid)

@app.route('/bdbge/blocking/<int:uid>', methods=['GET'])
def blocked(uid):
    return BaseUsers().blocking(uid)

@app.route('/bdbge/unblock/<int:uid>', methods=['POST'])
def unblock(uid):
    if request.method == 'POST':
        return BaseUsers().unblock(request.json,uid)
    else:
        return "An error has occurred"

@app.route('/bdbge/posts', methods=['POST'])
def posts():
    if request.method == 'POST':
        return BasePosts().newPost(request.json)
    else:
        return "An error has occurred"

@app.route('/bdbge/msg', methods=['GET'])
def msg():
    if request.method == 'GET':
        return BasePosts().getMsg()
    else:
        return "An error has occurred"

@app.route('/bdbge/msg/<int:mid>', methods=['GET'])
def msgId(mid):
    if request.method == 'GET':
        return BasePosts().getMsgId(mid)
    else:
        return "An error has occurred"

@app.route('/bdbge/reply', methods=['POST'])
def reply():
    if request.method == 'POST':
        return BasePosts().reply(request.json)
    else:
        return "An error has occurred"

@app.route('/bdbge/share', methods=['POST'])
def share():
    if request.method == 'POST':
        return BasePosts().share(request.json)
    else:
        return "An error has occurred"

@app.route('/bdbge/liked/<int:mid>', methods=['GET'])
def liked(mid):
    if request.method == 'GET':
        return BasePosts().getLiked(mid)
    else:
        return "An error has occurred"

@app.route('/bdbge/like/<int:mid>', methods=['POST'])
def like(mid):
    if request.method == 'POST':
        return BasePosts().getLike(request.json, mid)
    else:
        return "An error has occurred"

@app.route('/bdbge/like/remove/<int:mid>', methods=['POST'])
def likeRemoved(mid):
    if request.method == 'POST':
        return BasePosts().getLikeRemoved(request.json, mid)
    else:
        return "An error has occurred"

@app.route('/bdbge/unlike/<int:mid>', methods=['POST'])
def unlike(mid):
    if request.method == 'POST':
        return BasePosts().getUnlike(request.json, mid)
    else:
        return "An error has occurred"

@app.route('/bdbge/unliked/<int:mid>', methods=['GET'])
def unliked(mid):
    if request.method == 'GET':
        return BasePosts().getUnliked(mid)
    else:
        return "An error has occurred"

@app.route('/bdbge/unlike/remove/<int:mid>', methods=['POST'])
def unlikeRemoved(mid):
    if request.method == 'POST':
        return BasePosts().getUnlikeRemoved(request.json, mid)
    else:
        return "An error has occurred"

if __name__ == '__main__':
    app.run()