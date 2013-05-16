from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import QuerySet


from .utils import get_obj_id, generate_unique_slug


class SlugQuerySet(QuerySet):
    def filter_by_obj(self, obj, **kwargs):
        content_type = kwargs.pop('content_type',
                                  ContentType.objects.get_for_model(obj))

        return self.filter_by_obj_id(obj.pk,
                                     content_type=content_type,
                                     **kwargs)

    def filter_by_obj_id(self, obj_id, content_type, **kwargs):
        _filter = self.filter

        if kwargs.pop('exclude', False):
            _filter = self.exclude

        return _filter(content_type_id=get_obj_id(content_type),
                       object_id=obj_id,
                       **kwargs)

    def filter_by_model(self, klass, **kwargs):
        content_type = kwargs.pop('content_type',
                                  ContentType.objects.get_for_model(klass))

        return self.filter(content_type_id=get_obj_id(content_type),
                           **kwargs)


class SlugManager(models.Manager):
    def get_query_set(self):
        return SlugQuerySet(self.model)

    def filter_by_obj(self, *args, **kwargs):
        return self.get_query_set().filter_by_obj(*args, **kwargs)

    def filter_by_model(self, *args, **kwargs):
        return self.get_query_set().filter_by_model(*args, **kwargs)

    def get_current(self, obj, content_type=None):
        if isinstance(obj, models.Model):
            obj_id = obj.pk

            if not content_type:
                content_type = ContentType.objects.get_for_model(obj)

        obj_id = obj

        try:
            return self.filter_by_obj_id(obj_id,
                                         redirect=False,
                                         content_type=content_type).get()
        except self.model.DoesNotExist:
            return None

    def is_slug_available(self, slug, obj=None):
        if slug in self.get_forbidden_slugs():
            return False

        qs = self.filter(slug=slug)

        if not obj is None:
            qs = qs.filter_by_obj(obj, exclude=True)

        if qs.exists():
            return False

        return True

    def generate_unique_slug(self, instance, slug, max_length,
                             field_name, index_sep):

        qs = self.filter_by_obj(instance, exclude=True)

        return generate_unique_slug(qs, instance, slug, max_length,
                                    field_name, index_sep)

    def update_slug(self, instance, slug, erase_redirects=False):
        content_type = ContentType.objects.get_for_model(instance)

        pk = instance.pk

        try:
            filters = {
                'content_type': content_type,
                'object_id': pk,
                'redirect': False,
            }
            current = self.get(**filters)
            new = False
            update = current.slug != slug
        except self.model.DoesNotExist:
            new = True
            update = True

        if update:
            filters = {
                'content_type': content_type,
                'object_id': pk,
            }

            qs = self.filter(**filters).exclude(slug=slug)

            if not new and erase_redirects:
                qs.delete()
            else:
                qs.update(redirect=True)

            filters['slug'] = slug

            affected = self.filter(**filters).update(redirect=False)

            if not affected:
                slug = self.model(**dict({'redirect': False}, **filters))
                slug.save()


class Slug(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    slug = models.CharField(max_length=255,
                            verbose_name=_('URL'),
                            db_index=True,
                            unique=True)
    redirect = models.BooleanField(default=False,
                                   verbose_name=_('Redirection'))

    objects = SlugManager()

    class Meta:
        abstract = True

    def get_forbidden_slugs(self):
        return []

    def get_current(self):
        if self.redirect:
            return self

        return Slug.objects.get_current_for_obj(self.object_id,
                                                content_type=self.content_type_id)
