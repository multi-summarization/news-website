from . import db
import datetime
from marshmallow import fields, Schema

class ClusterModel(db.Model):

    __tablename__ = 'cluster'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    cluster_no = db.Column(db.Integer, nullable=False)
    source_title = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.Text, nullable=False)

    def __init__(self, data):
        self.cluster_no = data.get('cluster_no')
        self.article_id = data.get('article_id')
        self.source_title = data.get('source_title')
        self.source_url = data.get('source_url')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    @staticmethod
    def get_all_clusters():
        return ClusterModel.query.all()

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ClusterSchema(Schema):
  """
  Cluster Schema
  """
  id = fields.Int(dump_only=True)
  source_title = fields.Str(required=True)
  source_url = fields.Str(required=True)
  article_id = fields.Int(required=True)
  cluster_no = fields.Int(required=True)

    