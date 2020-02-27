from flask_restful import Api

from Blogs.views import BlogsResource, BlogResource

blogs_api = Api(prefix="/blogs")


blogs_api.add_resource(BlogsResource, "/")

blogs_api.add_resource(BlogResource, "/<int:pk>/")
