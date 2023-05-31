from flask import Flask, request, jsonify

app = Flask(__name__)

"""{“topic”: ”topic_name”,
“source”:[{“id”: “id”, 
“source_content”:“source_content”, 
“source_video_path”:“source_video_path”, 
“video_name”: “video_name”}, ...]}
"""

"""
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)  # TODO subtopic reference
    topic_queue = db.Column(db.Integer, nullable=False)
    subtopics = db.relationship('Subtopic', cascade="all,delete", backref='topic', lazy='dynamic')
    source_of_learning = db.relationship('SourceOfLearningTextContent', cascade="all,delete", backref='topic',
                                         lazy='dynamic')
    source_of_learning_video_content = db.relationship('SourceOfLearningVideoContent', cascade="all,delete",
                                                       backref='topic', lazy='dynamic')
                                                       
                                                       
class SourceOfLearningTextContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_content_header = db.Column(db.String(255), nullable=False)
    source_content_plain_text = db.Column(db.Text, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True)
    subtopic_id = db.Column(db.Integer, db.ForeignKey('subtopic.id'), nullable=True)"""

# @app.route('/get_source_by_topic')
# def get_source_by_topic(topic):
#     if request.method == 'GET':
#         topic = Topic.query.filter_by(topic_name=topic).first()
#         if not topic:
#             return jsonify({'error': 'This topic not found'})
#
#         sources = []
#         for source in topic.source_of_learning_video_content:
#             response = {
#                 'source_id' : source.id
#                 'source_content' :
#             }
#
#


"""/add_topic/<course>
request POST
{“topic”:”topic_name”}
response 200
"""

@app.route('/add_topic', methods=['POST'])
def add_topic():
    new_topic_name = request.form.args('new_topic_name')
    course_id = request.form.args('course_id')
    topic_queue = request.form.args('topic_queue')
    subtopics = request.form.args('subtopics')
    source_of_learning = request.form.args('source_of_learning')
    source_of_learning_video_content = request.form.args('source_of_learning_video_content')
    if request.method == 'POST':
        new_topic = Topic(topic_name=new_topic_name,
                          course_id=course_id,
                          topic_queue=topic_queue,
                          subtopics=subtopics,
                          source_of_learning=source_of_learning,
                          source_of_learning_video_content=source_of_learning_video_content)
        db.session.add(new_topic)
        db.session.commit()

    response = {}
    response['topic'] = new_topic_name
    return response, 200

"""/add_subtopic/<course>
request POST
{“topic”:”topic_name”,
“subtopic”: “subtopoic_name”}
responce 200"""


@app.route('/add_subtopic/course', methods=['POST'])
def add_subtopic(course):
    new_subtopic_name = request.form.get('new_subtopic_name')
    topic_id = request.form.get('topic_id')
    subtopic_queue = request.form.get('subtopic_queue')
    questions = request.form.get('questions')
    exercises = request.form.get('exercises')
    subtopicgroups = request.form.get('subtopicgroups')
    source_of_learning = request.form.get('source_of_learning')
    source_of_learning_video_content = request.form.get('source_of_learning_video_content')
    if request.method == 'POST':
        new_subtopic = Subtopic(subtopic_name=new_subtopic_name,
                                topic_id=topic_id,
                                subtopic_queue=subtopic_queue,
                                questions=questions,
                                exercises=exercises,
                                subtopicgroups=subtopicgroups,
                                source_of_learning=source_of_learning,
                                source_of_learning_video_content=source_of_learning_video_content)

        db.session.add(new_subtopic)
        db.session.commit()

    response = {}
    topic = Topic.query.filter_by(id=topic_id).first()
    if topic:
        response['topic'] = topic.topic_name
        response['subtopic'] = new_subtopic_name

    return response, 200

"""
/edit_topic/<cource>/<id>
request PUT
{“new_name”:”new_name”}
response 200"""

@app.route('/edit_topic/course/id', methods=['PUT'])
def edit_topic(course, id):
    new_name = request.json.get('new_name')
    if request.method == 'PUT':
        topic = Topic.query.filter_by(id=id).first()

        topic.topic_name = new_name
        db.session.commit()

        return 'Updated!', 200


"""/delete_topic/<course>/<id>
request DELETE
response 200"""

@app.route('delete_topic/course/id', methods=['DELETE'])
def delete_topic(course, id):
    if request.method == 'DELETE':
        our_topic = Topic.query.filter_by(id=id).first()

        db.session.delete(our_topic)
        db.session.commit()

        return 200

