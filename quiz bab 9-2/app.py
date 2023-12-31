from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://adrian:adrian@cluster0.b5hahmz.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient (connection_string)
db = client.dbdiary
app = Flask (__name__) 

@app.route('/')
def home(): 
    return render_template('index.html')


# request handler FLASK
@app.route('/diary', methods=['GET'])
def show_diary (): 
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles' : articles})
 
@app.route ('/diary', methods=['POST'])
def save_diary ():
    # sample_receive = request.form.get('sample_give')
    # print (sample_receive)

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')


    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    #variabel baru untuk files serta menggunakan datetime module
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1] 
    filename = f'file-{mytime}.{extension}'
    save_to =f'static/{filename}'
    file.save(save_to)

    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1] 
    profilename = f'profile-{mytime}.{extension}'
    save_to =f'static/{profilename}'
    profile.save(save_to)
    
    doc = {
        'file' : filename,
        'profile' : profilename,
        'title' : title_receive,
        'content' : content_receive
    }  
    db.diary.insert_one(doc)    
    return jsonify({'message' : 'the memory has kept in the diary'})


if __name__ =='__main__':
    app.run ('0.0.0.0' , port=5000, debug=True)