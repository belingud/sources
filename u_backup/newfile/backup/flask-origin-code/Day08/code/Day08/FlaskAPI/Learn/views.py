from flask import request
from flask_restful import Resource, reqparse, marshal_with, fields

from Learn.models import Student

parse = reqparse.RequestParser()

parse.add_argument("hobby", dest="aihao",action="append")
parse.add_argument("csrftoken", location=["cookies", "args"], action="append")

student_fields = {
    "name": fields.String(attribute="s_name"),
    "s_age": fields.Integer,
    "hehe": fields.String(default=""),
    "hehe_time": fields.Integer(default=3)
}

return_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    # "data": fields.Nested(student_fields)
    "data": fields.List(fields.Nested(student_fields))
}


class LearnResource(Resource):

    # @marshal_with(student_fields)
    @marshal_with(return_fields)
    def get(self):

        # hobby = request.args.getlist("hobby")
        #
        # print(hobby)

        # args = parse.parse_args()
        #
        # hobby = args.get("aihao")
        #
        # print(hobby)
        #
        # csrf = args.get("csrftoken")
        #
        # print(csrf)

        # return {"msg": "ok"}

        students = []

        for i in range(8):
            students.append(Student())

        #
        # return student

        data = {
            "msg": "ok",
            "status": 200,
            "data": students
        }

        return data