from datetime import datetime
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapper

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()

def map_class_to_some_table(cls, table, entity_name, **kw):
    newcls = type(entity_name, (cls, ), {})
    mapper(newcls, table, **kw)
    return newcls

TOPIC_TABLE_NUMBER = 10
REPLY_TABLE_NUMBER = 10

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, name, description):
        self.user_id = user_id
        self.name = name
        self.description = description

    @staticmethod
    def get_all_groups():
        return Group.query.all()

    @staticmethod
    def get_group_by_id(group_id):
        return Group.query.filter_by(id=group_id).first()

    @staticmethod
    def insert_group(user_id, name, description):
        group = Group(user_id, name, description)
        db.session.add(group)
        db.session.commit()

class Topic(object):
    
    __tablename__ = 'topic'
    
    def __init__(self, group_id, user_id, title, content):
        self.group_id = group_id
        self.user_id = user_id
        self.title = title
        self.content = content

class Reply(object):

    def __init__(self, topic_id, user_id, content):
        self.topic_id = topic_id
        self.user_id = user_id
        self.content = content

registries = {}

for i in range(TOPIC_TABLE_NUMBER):
    name = "topic_%d" % i
    table = db.Table(name, db.metadata,
        db.Column('id', db.Integer, primary_key=True, autoincrement=True),
        db.Column('group_id', db.Integer, nullable=False, index=True),
        db.Column('user_id', db.Integer, nullable=False, index=True),
        db.Column('title', db.String(100), nullable=False),
        db.Column('content', db.Text),
        db.Column('create_time', db.DateTime, default=datetime.utcnow),
        db.Column('update_time', db.DateTime, default=datetime.utcnow,
                    onupdate=datetime.utcnow),
        db.Column('reply_count', db.Integer, default=0),
        db.Column('last_reply_by', db.Integer, default=0),
        db.Column('last_reply_time', db.DateTime, default=datetime.utcnow)
    )    
    registries[name] = \
            map_class_to_some_table(Topic, table, name)

for i in range(REPLY_TABLE_NUMBER):
    name = "reply_%d" % i
    table = db.Table(name, db.metadata,
        db.Column('id', db.Integer, primary_key=True, autoincrement=True),
        db.Column('topic_id', db.Integer, nullable=False, index=True),
        db.Column('user_id', db.Integer, nullable=False, index=True),
        db.Column('content', db.Text),
        db.Column('create_time', db.DateTime, default=datetime.utcnow)
    )
    registries[name] = \
            map_class_to_some_table(Reply, table, name)

def get_class(ind):
    topic = 'topic_%d' % ind
    reply = 'reply_%d' % ind
    return registries[topic], registries[reply]

