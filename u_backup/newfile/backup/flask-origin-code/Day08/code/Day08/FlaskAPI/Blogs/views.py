from flask import request, g
from flask_restful import Resource, fields, marshal_with, marshal, abort, reqparse

from Blogs.models import Blog
from FlaskWork.ext import cache
from Users.models import User
from common.users_util import login_required

blog_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String
}

return_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.Nested(blog_fields)
}

parse = reqparse.RequestParser()
parse.add_argument("title", required=True, help="请填写标题")
parse.add_argument("content", required=True, help="请填写内容")


class BlogsResource(Resource):

    @marshal_with(return_fields)
    def get(self):
        blogs = Blog.query.all()

        data = {
            "msg": "ok",
            "status": 200,
            "data": blogs
        }

        return data

    @login_required
    def post(self):
        user = g.user

        args = parse.parse_args()

        title = args.get("title")

        content = args.get("content")

        blog = Blog(title=title, content=content, b_owner=user.id)

        if not blog.save():
            data = {
                "msg": "create fail",
                "status": 400
            }
            return data

        data = {
            "msg": "ok",
            "status": 200,
            "data": blog
        }

        return marshal(data, return_fields)


class BlogResource(Resource):

    def get(self, pk):
        blog = Blog.query.get(pk)

        if not blog:
            abort(404, message="blog has been deteled")

        data = {
            "msg": "ok",
            "status": 200,
            "data": blog
        }

        return marshal(data, return_fields)

    @login_required
    def patch(self, pk):

        blog = Blog.query.get(pk)

        if not blog:
            abort(404, message="blog has been deteled")

        user = g.user

        if blog.b_owner != user.id:
            abort(403, message="can't modify others")

        title = request.form.get("title")

        content = request.form.get("content")

        # if title:
        #     blog.title = title
        #
        # if content:
        #     blog.content = content

        blog.title = title or blog.title

        blog.content = content or blog.content

        if not blog.save():
            data = {
                "msg": "modify fail",
                "status": 400
            }
            return data

        data = {
            "msg": "ok",
            "status": 200,
            "data": blog
        }

        return marshal(data, return_fields)
