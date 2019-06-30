import json
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from .forms import CustomSearchForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from .models import Documentstorage, View, Document, User, Entity, Paragraph
from datetime import date

# added neo4j operations simply into existing actions

def upvote(request):
    user_id = request.user.id
    doc_hash = request.POST.get('hash')
    document = get_object_or_404(Documentstorage, hash=doc_hash)
    print(document.get_total_votes)
    document.votes.up(user_id)

    #neo4j operations
    user_node = User.nodes.get(handle = user_id)

    #pruning path and file extensions for maximum of 2 file extensions
    node_title = os.path.splitext(os.path.basename(document.filepath))[0]
    node_title = os.path.splitext(os.path.basename(node_title))[0]
    doc_node = Document.nodes.get(title=node_title)

    if user_node.dislike.is_connected(doc_node):
            user_node.dislike.disconnect(doc_node)

    user_node.like.connect(doc_node)

    message = 'You liked this'

    ctx = {'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def downvote(request):
    user_id = request.user.id
    doc_hash = request.POST.get('hash')
    document = get_object_or_404(Documentstorage, hash=doc_hash)
    document.votes.down(user_id)

    #neo4j operations
    user_node = User.nodes.get(handle = user_id)

    #pruning path and file extensions for maximum of 2 file extensions
    node_title = os.path.splitext(os.path.basename(document.filepath))[0]
    node_title = os.path.splitext(os.path.basename(node_title))[0]
    doc_node = Document.nodes.get(title=node_title)

    if user_node.like.is_connected(doc_node):
            user_node.like.disconnect(doc_node)

    user_node.dislike.connect(doc_node)

    message = 'You disliked this'

    ctx = {'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def delete(request):
    user_id = request.user.id
    doc_hash = request.POST.get('hash')
    document = get_object_or_404(Documentstorage, hash=doc_hash)
    document.votes.delete(user_id)

    #neo4j operations
    user_node = User.nodes.get(handle = user_id)

    #pruning path and file extensions for maximum of 2 file extensions
    node_title = os.path.splitext(os.path.basename(document.filepath))[0]
    node_title = os.path.splitext(os.path.basename(node_title))[0]
    doc_node = Document.nodes.get(title=node_title)

    if user_node.like.is_connected(doc_node):
            user_node.like.disconnect(doc_node)

    if user_node.dislike.is_connected(doc_node):
            user_node.dislike.disconnect(doc_node)

    message = 'You deleted your vote'

    ctx = {'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def get_user_profile(request):
    user = request.user
    votes_up = Documentstorage.votes.all(user.id, 0)
    votes_down = Documentstorage.votes.all(user.id, 1)
    return render(request, 'document_manager/user_profile.html', {"user": user, "votes_up": votes_up, "votes_down": votes_down})

def recommendations(request):
    user_id = request.user.id

    #neo4j operations
    user_node = User.nodes.get(handle = user_id)
    entity_scores = user_node.like_connections_over_entity()
    paragraph_connections = user_node.paragraph_connections()
    view_scores = user_node.view_connections_over_entity()

    #doc from relational db
    for rec in entity_scores:
        startdocs = []
        for sdoc in rec['startdoc']:
            startdocs.append(Documentstorage.objects.filter(filepath__icontains=sdoc)[0])

        # strings to ent objects
        ents = []
        for ent in rec['entities']:
            ents.append(Entity.nodes.filter(text__exact = ent)[0])
            #print(Entity.nodes.filter(text__exact = ent)[0])

        rec['entity_objects'] = ents
        rec['startdoc_objects'] = startdocs
        rec['recdoc_object'] = Documentstorage.objects.filter(filepath__icontains=rec['recdoc'])[0]

    for rec in paragraph_connections:
        rec['startdoc_object'] = Documentstorage.objects.filter(filepath__icontains=rec['startdoc'])[0]
        rec['recdoc_object'] = Documentstorage.objects.filter(filepath__icontains=rec['recdoc'])[0]
        rec['par_object'] = Paragraph.nodes.get(name=rec['par'])

    for rec in view_scores:
        # strings to ent objects
        ents = []
        for ent in rec['entities']:
            ents.append(Entity.nodes.filter(text__exact = ent)[0])
            #print(Entity.nodes.filter(text__exact = ent)[0])

        rec['entity_objects'] = ents
        rec['startdoc_object'] = Documentstorage.objects.filter(filepath__icontains=rec['startdoc'])[0]
        rec['recdoc_object'] = Documentstorage.objects.filter(filepath__icontains=rec['recdoc'])[0]


    return render(request, 'document_manager/recommendations.html', {"entity_scores": entity_scores, "paragraph_connections": paragraph_connections, "view_scores": view_scores})

def entity_search(request, entityslug):
    entity_node = Entity.nodes.filter(text__exact = entityslug.replace('-', ' '))[0]
    docs = entity_node.get_connected_documents()
    print(docs)
    frequency = entity_node.get_total()
    #print(frequency)
    #entity = slugify(entity)

    for doc in docs:
        doc['startdoc_object'] = Documentstorage.objects.filter(filepath__icontains=doc['startdoc'])[0]

    return render(request, 'document_manager/entity_search.html', {"docs": docs, "ent": entity_node, "freq":frequency})

def paragraph_search(request, paragraphslug):
    paragraph_node = Paragraph.nodes.filter(name__exact = paragraphslug.replace('-', ' '))[0]
    docs = paragraph_node.get_connected_documents()
    print(docs)
    frequency = paragraph_node.get_total()
    #entity = slugify(entity)

    for doc in docs:
        doc['startdoc_object'] = Documentstorage.objects.filter(filepath__icontains=doc['startdoc'])[0]

    return render(request, 'document_manager/paragraph_search.html', {"docs": docs, "par": paragraph_node, "freq":frequency})

def document_list(request):
    docs_from_3 = Documentstorage.objects.filter(datasource=3)
    return render(request, 'document_manager/document_list.html')


class DocumentDetailView(generic.DetailView):
    model = Documentstorage
    template_name = "document_manager/document_detail.html"

    # overwrite due to duplicate db entries (slug)
    def get_object(self):
        doc = Documentstorage.objects.filter(slug__iexact=self.kwargs['slug'])[:1]
        return doc[0]

    def get_context_data(self, **kwargs):
        user = self.request.user
        doc = self.object
        View(document_id=doc, user_id=user, view_date=timezone.now()).save()

        #neo4j operations
        user_node = User.nodes.get(handle = user.id)

        #pruning path and file extensions for maximum of 2 file extensions
        node_title = os.path.splitext(os.path.basename(doc.filepath))[0]
        node_title = os.path.splitext(os.path.basename(node_title))[0]
        doc_node = Document.nodes.get(title=node_title)

        user_node.view.connect(doc_node)

        print(user_node.view.is_connected(doc_node))

        if user_node.view.is_connected(doc_node):
            print("You are the truth")

        # getting connected entity nodes
        ents = []
        for ent in doc_node.get_connected_entitys():
            ents.append(Entity.nodes.filter(text__exact = ent['entity'])[0])
            #print(Entity.nodes.filter(text__exact = ent)[0])

        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['user'] = user
        context['likes'] = doc.votes.user_ids()
        context['views'] = View.objects.filter(document_id=doc)
        context['entities'] = ents
        return context

