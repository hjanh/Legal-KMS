# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from vote.models import VoteModel
from vote.managers import VotableManager
from neomodel import StructuredNode, StructuredRel, StringProperty, UniqueIdProperty, IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom


class Abbreviations(models.Model):
    language_id = models.IntegerField()
    abbr = models.CharField(max_length=16)
    abbreviation = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'abbreviations'


class Datasources(models.Model):
    name = models.CharField(max_length=120)
    datasources_type = models.IntegerField()
    baseurl = models.CharField(max_length=120)
    targeturl = models.CharField(max_length=120)
    primarylanguage = models.IntegerField()
    timestamp = models.DateTimeField()
    active = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'datasources'


class DatasourcesType(models.Model):
    datasource_type = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'datasources_type'


class Documentstorage(VoteModel, models.Model):
    hash = models.CharField(max_length=255, blank=True, null=True)
    datasource = models.IntegerField()
    datasources_type = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=320)
    title = models.TextField()
    date = models.DateTimeField()
    author = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    language = models.IntegerField(blank=True, null=True, default=None)
    filepath = models.CharField(max_length=320)
    slug = models.CharField(max_length=320)
    votes = VotableManager()

    class Meta:
        managed = True
        db_table = 'documentstorage'

    def get_total_votes(self):
        total = self.votes.count()
        return int(total)

    def generate_absolute_url(self):
        url = "/document/" + self.slug
        return url


class Languages(models.Model):
    language = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'languages'


class Metadata(models.Model):
    lastactivity = models.IntegerField()
    databasesize = models.IntegerField()
    graphdatabaselink = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'metadata'


class View(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    document_id = models.ForeignKey(Documentstorage, on_delete=models.PROTECT)
    view_date = models.DateTimeField('date viewed')

    def get_views_for_document(document):
        View.objects.filter(document_id=document)

    def get_views_for_user(user):
        View.objects.filter(user_id=user)


# definition of nodes for neo4j starts here
class Paragraph(StructuredNode):
    id = UniqueIdProperty()
    name = StringProperty()

    document = RelationshipFrom('Document', 'REFERENCES')

    def get_total(self):
        result, columns = self.cypher("MATCH (a)-[r:REFERENCES]->(b) WHERE id(b)={self} RETURN COUNT(r)")
        return result[0][0]


    def generate_absolute_url(self):
        slug = self.name.replace(' ', '-')
        url = "/paragraph_search/" + slug
        return url

    # retrieves all documents connected to this paragraph with a score for relevance
    def get_connected_documents(self):
        results, columns = self.cypher("MATCH (b)-[:REFERENCES]->(c) WHERE id(c)={self} WITH  b.title AS startdoc RETURN  startdoc LIMIT 10")

        #list of dicts
        result_list = []
        for res in results:
            res_dict = {}
            res_dict['startdoc'] = res[0]
            result_list.append(res_dict)

        return result_list


class EntityRelation(StructuredRel):
    count = IntegerProperty()
    relevance = FloatProperty()


class Entity(StructuredNode):
    id = UniqueIdProperty()

    text = StringProperty()
    type = StringProperty()

    def get_total(self):
        result, columns = self.cypher("MATCH (a)-[r:INCLUDES]->(b) WHERE id(b)={self} RETURN COUNT(r)")
        return result[0][0]

    document = RelationshipFrom('Document', 'INCLUDES', model=EntityRelation)


    def generate_absolute_url(self):
        slug = self.text.replace(' ', '-')
        url = "/entity_search/" + slug
        return url

    # retrieves all documents connected to this entity with a score for relevance
    def get_connected_documents(self):
        results, columns = self.cypher("MATCH (b)-[i1:INCLUDES]->(c) WHERE id(c)={self} WITH c.text AS entity, toFloat(i1.count) AS count1, toFloat(i1.relevance) AS rel1, b.title AS startdoc RETURN  startdoc, (count1*rel1) AS totalscore  ORDER BY totalscore DESC LIMIT 10")

        #list of dicts
        result_list = []
        for res in results:
            res_dict = {}
            res_dict['startdoc'] = res[0]
            res_dict['score'] = round(res[1],2)
            result_list.append(res_dict)

        return result_list


class Document(StructuredNode):
    id = UniqueIdProperty()

    language = StringProperty()
    title = StringProperty()

    paragraph = RelationshipTo('Paragraph', 'REFERENCES')
    entity = RelationshipTo('Entity', 'INCLUDES', model=EntityRelation)

    like = RelationshipFrom('Document', 'LIKES')
    dislike = RelationshipFrom('Document', 'DISLIKES')
    view = RelationshipFrom('Document', 'VIEWED')

    def get_connected_entitys(self):
        results, columns = self.cypher("MATCH (b) WHERE id(b)={self} MATCH (b)-[i1:INCLUDES]->(c) WHERE NOT c.text CONTAINS '.' AND NOT c.text CONTAINS '%' WITH c.text AS entity, toFloat(i1.count) AS count1, toFloat(i1.relevance) AS rel1, b.title AS startdoc RETURN  entity, (count1*rel1) AS totalscore  ORDER BY totalscore DESC LIMIT 10")

        #list of dicts
        result_list = []
        for res in results:
            res_dict = {}
            res_dict['entity'] = res[0]
            res_dict['score'] = round(res[1],2)
            result_list.append(res_dict)

        return result_list


class User(StructuredNode):
    # id from relational django db
    handle = IntegerProperty()

    like = RelationshipTo('Document', 'LIKES')
    dislike = RelationshipTo('Document', 'DISLIKES')
    view = RelationshipTo('Document', 'VIEWED')

    # retrieves a connection in the form of: user likes document has entity has document has liked by user via cypher
    def like_connections_over_entity(self):
        print(self)
        print({'test': 1})
        results, columns = self.cypher("MATCH (a) WHERE id(a)={self} MATCH (a)-[:LIKES]->(b)-[i1:INCLUDES]->(c)<-[i2:INCLUDES]-(d)<-[:LIKES]-(f) WHERE NOT (a)-[:LIKES]->(d) AND NOT (a)-[:DISLIKES]->(d) AND NOT c.text CONTAINS '.'  WITH toFloat(i1.count) AS count1, toFloat(i1.relevance) AS rel1, toFloat(i2.count) AS count2, toFloat(i2.relevance) AS rel2, d.title AS doc, c.text AS ent, f.handle AS user, b.title AS startdoc RETURN COLLECT(distinct startdoc) AS startdoc, doc, user, sum(0.5*(count1*rel1)+0.5*(count2*rel2)) AS totalscore, COLLECT(distinct ent) AS ents ORDER BY totalscore DESC LIMIT 10")

        #list of dicts
        result_list = []
        for res in results:
            res_dict = {}
            res_dict['startdoc'] = res[0]
            res_dict['recdoc'] = res[1]
            res_dict['user_id'] = res[2]
            res_dict['score'] = round(res[3],2)
            res_dict['entities'] = res[4]
            result_list.append(res_dict)

        return result_list

    def paragraph_connections(self):
        results, columns = self.cypher("MATCH (a) WHERE id(a)={self} MATCH (a)-[:LIKES]->(b)-[:REFERENCES]->(p)<-[:REFERENCES]-(dp) WITH p.name AS par, dp.title AS dp, dp.title AS doc, b.title AS startdoc RETURN startdoc, dp, par LIMIT 100")

        #list of dicts
        result_list = []
        for res in results:
            res_dict = {}
            res_dict['startdoc'] = res[0]
            res_dict['recdoc'] = res[1]
            res_dict['par'] = res[2]
            result_list.append(res_dict)

        return result_list

    def view_connections_over_entity(self):
        results, columns = self.cypher("MATCH (a) WHERE id(a)={self} MATCH (a)-[:VIEWED]->(b)-[i1:INCLUDES]->(c)<-[i2:INCLUDES]-(d) WHERE NOT (a)-[:LIKES]->(d) AND NOT (a)-[:DISLIKES]->(d) WITH toFloat(i1.count) AS count1, toFloat(i1.relevance) AS rel1, toFloat(i2.count) AS count2, toFloat(i2.relevance) AS rel2, d.title AS doc, c.text AS ent, b.title AS startdoc RETURN startdoc,  doc, sum(0.5*(count1*rel1)+0.5*(count2*rel2)) AS totalscore, COLLECT(ent) AS ents ORDER BY totalscore DESC LIMIT 10")

        #list of dicts
        result_list = []
        for res in results:
            res_dict = {}
            res_dict['startdoc'] = res[0]
            res_dict['recdoc'] = res[1]
            res_dict['score'] = round(res[2],2)
            res_dict['entities'] = res[3]
            result_list.append(res_dict)

        return result_list
