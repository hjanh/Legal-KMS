"""import datetime"""
from haystack import indexes
from document_manager.models import Documentstorage


class DocumentstorageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, model_attr='title')
    text2 = indexes.CharField(model_attr='text', null=True)
    language = indexes.IntegerField(model_attr='language', null=True)
    datasource = indexes.IntegerField(model_attr='datasource')

    def get_model(self):
        return Documentstorage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        """return self.get_model().objects.filter(date=datetime.datetime.now())"""
        """HACKAROUND TO TWEAK BAD TIME DATA"""
        return self.get_model().objects.all()