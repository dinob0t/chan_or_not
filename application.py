#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
import json

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()
credentials = 'creds.json'
creds_data = {}
chan_urls = ['1YCpe4X']
def init_creds():
    with open(credentials) as creds:
        global creds_data    
        creds_data = json.load(creds)
    print creds_data

@auth.get_password
def get_password(username):
    print creds_data 
    print ' in get password'
    print username
    if creds_data.get(username):
        print username
        print ' in username'
        return creds_data[username]
    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

# task_fields = {
#     'title': fields.String,
#     'description': fields.String,
#     'done': fields.Boolean,
#     'uri': fields.Url('task')
# }


class IsChanAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(IsChanAPI, self).__init__()

    def get(self, url_in):
        # check chan
        print url_in
        return url_in in chan_urls
        # return {'tasks': [marshal(task, task_fields) for task in tasks]}

    # def post(self):
    #     args = self.reqparse.parse_args()
    #     task = {
    #         'id': tasks[-1]['id'] + 1,
    #         'title': args['title'],
    #         'description': args['description'],
    #         'done': False
    #     }
    #     tasks.append(task)
    #     return {'task': marshal(task, task_fields)}, 201


# class TaskAPI(Resource):
#     decorators = [auth.login_required]

#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, location='json')
#         self.reqparse.add_argument('description', type=str, location='json')
#         self.reqparse.add_argument('done', type=bool, location='json')
#         super(TaskAPI, self).__init__()

#     def get(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         return {'task': marshal(task[0], task_fields)}

#     def put(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         task = task[0]
#         args = self.reqparse.parse_args()
#         for k, v in args.items():
#             if v is not None:
#                 task[k] = v
#         return {'task': marshal(task, task_fields)}

#     def delete(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         tasks.remove(task[0])
#         return {'result': True}



# api.add_resource(IsChanAPI, '/chanornot/api/v1.0/ischan/<int:id>', endpoint='url_in')
api.add_resource(IsChanAPI, '/chanornot/api/v1.0/ischan/<url_in>', endpoint='url_in')

if __name__ == '__main__':
	init_creds()
	app.run(debug=True)
