from haystack import indexes

from .models import Page


class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Page

    def should_update(self, instance, **kwargs):
        if instance.deleted:
            self.remove_object(instance, **kwargs)
            return False
        else:
            return True
