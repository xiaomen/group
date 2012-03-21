from flask import render_template, request, redirect
from group import app
from group.models import *

def group_hash(group_id):
    return group_id % TOPIC_TABLE_NUMBER

@app.route('/')
def index():
    groups = Group.get_all_groups()
    return render_template('groups.html', groups = groups)

@app.route('/group/add', methods=['GET', 'POST'])
def create_group():
    if request.method == 'GET':
        return render_template('add_group.html')

    uid = 1 #TODO integrate with account

    name = request.form.get('name')
    description = request.form.get('description')

    Group.insert_group(uid, name, description)

    return redirect('/')

@app.route('/group/<group_id>')
def get_group(group_id):
    group = Group.get_group_by_id(group_id)

    _Topic = get_class(group_hash(group.id))[0]
    topics = db.session.query(_Topic).filter_by(group_id=group.id).all()

    return render_template('group.html', group=group, topics=topics)

@app.route('/topic/add', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'GET':
        return render_template('add_topic.html',
                group_id = request.args.get('group_id', ''))

    uid = 1 #TODO integrate with account

    group_id = int(request.form.get('group_id'))
    title = request.form.get('title')
    content = request.form.get('content')

    _Topic = get_class(group_hash(group_id))[0]
    topic = _Topic(group_id, uid, title, content)

    db.session.add(topic)
    db.session.commit()

    return redirect('/group/%d' % group_id)

@app.route('/topic/<topic_id>')
def get_topic(topic_id):
    group_id = topic_id.split('.')[0]
    topic_id = topic_id.split('.')[1]
    
    class_tup = get_class(group_hash(int(group_id)))
    _Topic = class_tup[0]
    _Reply = class_tup[1]

    topic = db.session.query(_Topic).filter_by(id=topic_id).first()
    replies = db.session.query(_Reply).filter_by(topic_id=topic.id).all()

    return render_template('topic.html', topic=topic,
            replies=replies, group_id=group_id)

@app.route('/reply/add', methods=['GET', 'POST'])
def create_reply():
    if request.method == 'GET':
        return render_template('add_reply.html',
                group_id = request.args.get('group_id', ''),
                topic_id = request.args.get('topic_id', ''))

    uid = 1 #TODO integrate with account

    group_id = request.form.get('group_id')
    topic_id = request.form.get('topic_id')
    content = request.form.get('content')

    _Reply = get_class(int(group_id))[1]
    reply = _Reply(int(topic_id), uid, content)

    db.session.add(reply)
    db.session.commit()

    return redirect('/topic/%s.%s' % (group_id, topic_id))

