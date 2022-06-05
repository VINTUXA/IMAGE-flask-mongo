import io

from pymongo import MongoClient
import gridfs
from flask import Flask, render_template, request,send_from_directory,redirect, url_for
from werkzeug.utils import secure_filename
from flask_mongoengine import MongoEngine
import base64
import io
import os
from PIL import Image
from zipfile import ZipFile
import uuid


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'videodb',
    'host': 'localhost',
    'port': 27017
}
app.config['UPLOAD_FOLDER'] = "C:/secrets/"
db = MongoEngine()
db.init_app(app)


class Video(db.Document):
    filename = db.StringField()
    cross = db.StringField()
    animals = db.StringField()
    path = db.StringField()


@app.route('/load')
def upload():
    return render_template('load.html')


@app.route('/upload', methods=['POST'])
def upload_video():
    inputfile = request.files['inputfile']
    # print(type(inputfile))
    filename = secure_filename(inputfile.filename)
    cross = request.form['cross']
    animals = request.form['animals']
    print(animals)
    #anim = request.form['anim']
    #print(anim)

    #save file to folder
    path = app.config['UPLOAD_FOLDER']+filename
    inputfile.save(path)
    #
    # #save data to db
    videosave = Video(filename=filename, cross=cross, animals=animals, path=path)
    videosave.save()
    print("upload success")

    for objects in Video.objects:
        print(objects)


    print(Video.objects)

    return redirect('/load')


@app.route('/posts')
def posts():
    posts = Video.objects
    print(posts)
    return render_template("posts.html", posts=posts)


@app.route('/posts/one/<id>')
def posts_one(id):
    post = Video.objects(id=id)
    print(post)
    return render_template("posts.html", posts=post)


@app.route('/posts/<mode>')
def posts_mode(mode):
    if mode == "cross":
        posts_cross = Video.objects(cross="1")
        print(posts_cross)
        return render_template("posts.html", posts=posts_cross)
    if mode == "animals":
        posts_animals = Video.objects(animals="1")
        print(posts_animals)
        return render_template("posts.html", posts=posts_animals)


@app.route('/delete/<id>')
def delete(id):
    Video.objects(id=id).delete()
    print(id+" has been deleted")
    #return render_template("posts.html")
    return redirect("http://127.0.0.1:5000/posts")

@app.route('/download/<id>')
def download(id):
    for params in Video.objects(id=id):
        print(params.filename)
    #Using Video.objects(id=id) as vo:

    filename = params.filename
    uploads = app.config['UPLOAD_FOLDER']
    #print(filename)
    #path = app.config['UPLOAD_FOLDER']+ filename
    #file
    #uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    #return "d" #send_from_directory(directory=uploads, filename=filename)
    return send_from_directory(directory=uploads, path=filename, as_attachment=True)


@app.route('/download/all')
def daownload_all():
    array = []
    for file in Video.objects:
        array.append(file.filename)
        print(array)
    # creating a ZipFile object
    zipname = str(uuid.uuid4())
    print(zipname)
    zip_full_name = zipname + ".zip"
    zip_path = "C:/zip/"+zipname+".zip"
    zip_only_path = "C:/zip/"
    zipObj = ZipFile(zip_path, 'w')
    # Add multiple files to the zip
    for name in array:
        path = app.config['UPLOAD_FOLDER']+name
        #tmp_file = open(path, "wb")
        print(path)
        zipObj.write(path)
    # close the Zip File
    zipObj.close()
    print(zip_only_path+zip_full_name)



    return send_from_directory(directory=zip_only_path, path=zip_full_name, as_attachment=True)




# def mongo_conn():
#     conn = MongoClient("localhost", 27017)
#     return conn.grid_file

# db = mongo_conn()
# fs = gridfs.GridFS(db)
#
# @app.route('/load')
# def upload_form():
#     return render_template('load.html')
#
#
# @app.route('/upload_video', methods=['POST'])
# def upload_video():
#     file_data = request.files['file']
#     cross = request.form['cross']
#     #name = request.form['name']
#     #name = "qweq.jpg"
#     name = secure_filename(file_data.filename)
#     print(name)
#     data = file_data.read()
#     fs.put(data, filename=name, cross=cross)
#     print("upload complete")
#         #     filename = secure_filename(file.filename)
#         # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         # # print('upload_video filename: ' + filename)
#         # flash('Video successfully uploaded and displayed below')
#     return render_template('load.html')
#
#
# @app.route('/display/<filename>')
# def display_video(filename):
#     print(filename)
#     #return render_template('load.html')
#     data = db.fs.files.find_one({'filename': filename})
#     list1 = fs.list()
#     print(list1)
#     print(fs.all())
#     print(type(data))
#     print(data.get('cross'))
#     cross = data.get('cross')
#     params = list(data)
#     print(params[2])
#     #list(data.keys())[0][1]
#     my_id = data['_id']
#     print(my_id)
#     outputdata = fs.get(my_id).read()
#     download_location = "C:/LUXOFT/data/IMAGE/static/images/"+filename
#     print(filename)
#     print(download_location)
#     output = open(download_location, "wb")
#     output.write(outputdata)
#     output.close()
#     print("download completes")
#     #print(type(outputdata))
#     #print(outputdata.get)
#     #img = Image.open(io.BytesIO(outputdata))
#     #print(type(img))
#     #img.show()
#
#     return render_template('display.html', filename=filename, cross=cross)#, photo=outputdata)
#
#
# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     uploads = "C:/secrets/"
#     return send_from_directory(directory=uploads, path=filename)



# name = "qweq.jpg"
# file_path = r"C:/Users/Vladimir Diakonov/Desktop/"
# file_location = file_path+name
# file_data = open(file_location, 'rb')
# data = file_data.read()
# fs = gridfs.GridFS(db)
# fs.put(data, filename = name)
# print("upload complete")

# data = db.fs.files.find_one({'filename':name})
# my_id = data['_id']
# print(my_id)
# outputdata = fs.get(my_id).read()
# download_location = r"C:/Users/Vladimir Diakonov/Desktop/download/"+name
# print(download_location)
# output = open(download_location, "wb")
# output.write(outputdata)
# output.close()
# print("download completes")

if __name__ == "__main__":
    app.run()

# database = connection['dbmongocrud']
#
# #Create an object of GridFs for the above database.
# fs = gridfs.GridFS(database)
#
# #define an image object with the location.
# file_location = r"C:\Users\Vladimir Diakonov\Desktop\qweq.jpg"
#
#
# #Open the image in read-only format.
# with open(file_location, 'rb') as f:
#     contents = f.read()
#
# #Now store/put the image via GridFs object.
# fs.put(contents, filename="file")
#
# #get file
# image = fs.find()
# print(image)
# image1 = fs.find_one({'filename':'file'})
# print(image1)
# my_id = f['_id']
# print(my_id)

