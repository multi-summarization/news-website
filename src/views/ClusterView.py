from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ClusterModel import ClusterModel, ClusterSchema

cluster_api = Blueprint('cluster_api', __name__)
cluster_schema = ClusterSchema()


@cluster_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Cluster Function
  """
  req_data = request.get_json()
  data, error = cluster_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  cluster = ClusterModel(data)
  cluster.save()
  data = cluster_schema.dump(cluster).data
  return custom_response(data, 201)

"""
@cluster_api.route('/<int:cluster_id>', methods=['DELETE'])
@Auth.auth_required
def delete(cluster_id):
  post = ClusterModel.get_one_article(Cluster_id)
  if not post:
    return custom_response({'error': ' not found'}, 404)
  data = cluster_schema.dump(post).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  post.delete()
  return custom_response({'message': 'deleted'}, 204)
"""



def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
