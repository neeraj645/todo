from flask import Flask, redirect, render_template, request
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# client = MongoClient('mongodb+srv://ssk9144794940:29oqRtlBfEWk6Dxn@cluster0.ag59kmf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
# db = client['project2']
# collection = db['todo_project']



# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://ssk9144794940:29oqRtlBfEWk6Dxn@cluster0.ag59kmf.mongodb.net/?retryWrites=true&w=majority")
db = client['todo']  # Replace 'your_database_name' with your actual database name
collection = db['todo_project'] 


@app.route('/', methods=['GET', 'POST'])
def default():
   
    message= 'none'
    try:
        if request.method == 'POST':
            topics = request.form['topic']
            descs = request.form['desc']
            collection.insert_one({'topic': topics, 'desc': descs, 'date': datetime.now()})
            message = 'true'
    except:
        message = 'false'
    return render_template('index.html',message = message)
        

@app.route('/show')
def show():
        data1  = collection.find()
        val = collection.count_documents({})
        return render_template('show.html',data = data1,val = val)


@app.route('/delete/<sno>')
def delete(sno):
    result = collection.delete_one({"_id": ObjectId(sno)})
    return redirect('/show')


@app.route('/update/<sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['topic']
        desc = request.form['desc']
        doc_id = ObjectId(sno)
        print("Title:", title)
        print("Description:", desc)
        print("Document ID:", doc_id)
        collection.update_one({"_id": doc_id}, {"$set": {"topic": title, "desc": desc}})
        return redirect("/show")
    todo = collection.find_one({"_id": ObjectId(sno)})  
    return render_template('update.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)
