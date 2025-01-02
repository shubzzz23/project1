from flask import Flask, request, redirect, render_template, flash, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'
client = MongoClient('mongodb://localhost:27017/')
db = client.mytododb

@app.route('/')
def index():
    todos = db.todos.find()  # Fetch all todos from the database
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    description = request.form.get('desc')

    # Ensure fields are not empty
    if not title or not description:
        flash("Title and Description are required!", "danger")
        return redirect('/')

    # Insert the new todo in the database
    db.todos.insert_one({'title': title, 'description': description})
    flash("Todo added successfully!", "success")
    return redirect('/')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('desc')

        # Ensure fields are not empty
        if not title or not description:
            flash("Title and Description are required!", "danger")
            return redirect(url_for('edit', id=id))

        # Update the selected todo in the database
        db.todos.update_one({'_id': ObjectId(id)}, {'$set': {'title': title, 'description': description}})
        flash("Todo updated successfully!", "success")
        return redirect('/')

    todo = db.todos.find_one({'_id': ObjectId(id)})
    return render_template('edit.html', todo=todo)

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    db.todos.delete_one({'_id': ObjectId(id)})  # Delete the selected todo
    flash("Todo deleted successfully!", "success")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5002)
