from flask import render_template, request, redirect
from group import app
from group.models import *

@app.route('/')
def index():
    groups = Group.get_all_groups()
    return render_template('groups.html', groups = groups)

@app.route('/group/add', methods=['GET', 'POST'])
def create_group():

    if request.method == 'GET':
        return render_template('add_group.html')

    uid = 1 #TODO integrate with account

    title = request.form.get('name')
    description = request.form.get('description')

    Group.insert_group(uid, title, description)

    return redirect('/')
