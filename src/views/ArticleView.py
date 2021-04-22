from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ArticleModel import ArticleModel, ArticleSchema

article_api = Blueprint('article_api', __name__)
article_schema = ArticleSchema()


@article_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Article Function
  """
  req_data = request.get_json()
  req_data['owner_id'] = g.user.get('id')
  data, error = article_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  post = ArticleModel(data)
  post.save()
  data = article_schema.dump(post).data
  return custom_response(data, 201)

@article_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Articles
  """
  posts = ArticleModel.get_all_articles()
  data = article_schema.dump(posts, many=True).data
  return custom_response(data, 200)

@article_api.route('/<int:article_id>', methods=['GET'])
def get_one(article_id):
  """
  Get A Article
  """
  post = ArticleModel.get_one_article(article_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = article_schema.dump(post).data
  return custom_response(data, 200)

@article_api.route('/<int:article_id>', methods=['PUT'])
@Auth.auth_required
def update(article_id):
  """
  Update A Article
  """
  req_data = request.get_json()
  post = ArticleModel.get_one_article(article_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = article_schema.dump(post).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)
  
  data, error = article_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = article_schema.dump(post).data
  return custom_response(data, 200)

@article_api.route('/<int:article_id>', methods=['DELETE'])
@Auth.auth_required
def delete(article_id):
  """
  Delete A Article
  """
  post = ArticleModel.get_one_article(article_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = article_schema.dump(post).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  post.delete()
  return custom_response({'message': 'deleted'}, 204)
  

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
