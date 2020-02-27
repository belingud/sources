from flask_restful import Api

from Learn.views import LearnResource

learn_api = Api(prefix="/learn")


learn_api.add_resource(LearnResource, "/")