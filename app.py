from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.n5dbos3.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page2')
def index2():
    return render_template('index2.html')

@app.route('/page3')
def index3():
    return render_template('index3.html')

@app.route('/page4')
def index4():
    return render_template('index4.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = list(db.bucket.find({}, {'_id': False}))
    num = len(count)+1

    doc = {'num': num,
           'bucket': bucket_receive,
           'done': 0}
    db.bucket.insert_one(doc)

    return jsonify({'msg': '등록 완료'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)},{'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료'})

@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)},{'$set': {'done': 0}})
    return jsonify({'msg': '버킷 취소'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets':bucket_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)