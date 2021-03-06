from flask import Flask

from .config import app_config
from .models import db, bcrypt

from .models import ArticleModel, ClusterModel

from .views.UserView import user_api as user_blueprint
from .views.ArticleView import article_api as article_blueprint
from .views.ClusterView import cluster_api as cluster_blueprint

from flask import render_template



def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(article_blueprint, url_prefix='/api/v1/articles')
  app.register_blueprint(cluster_blueprint, url_prefix='/api/v1/clusters')

  @app.route('/', methods=['GET'])
  def index():
    articles = ArticleModel.query.all()
    return render_template('index.html', object_list=articles )

  @app.route('/article/<int:art_id>')
  def detail(art_id):
    article = ArticleModel.query.filter_by(id=art_id).one()
    cluster = ClusterModel.query.filter_by(article_id=art_id)
    return render_template('detail.html', entry=article, sources = cluster)


  return app
