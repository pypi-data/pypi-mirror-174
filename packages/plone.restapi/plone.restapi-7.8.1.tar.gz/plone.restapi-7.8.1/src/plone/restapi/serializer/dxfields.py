# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from plone.app.textfield.interfaces import IRichText
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.interfaces import INamedFileField
from plone.namedfile.interfaces import INamedImageField
from plone.restapi.imaging import get_original_image_url
from plone.restapi.imaging import get_scales
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import IPrimaryFieldTarget
from plone.restapi.serializer.converters import json_compatible
from zope.component import getMultiAdapter
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IField
from zope.schema.interfaces import ITextLine
from zope.schema.interfaces import IVocabularyTokenized

import logging

try:
    from plone.app.contenttypes.interfaces import ILink
    from plone.app.contenttypes.utils import replace_link_variables_by_paths
except ImportError:
    # Probably Plone 4.3 with dexterity but without plone.app.contenttypes.
    ILink = None

log = logging.getLogger(__name__)


@adapter(IField, IDexterityContent, Interface)
@implementer(IFieldSerializer)
class DefaultFieldSerializer(object):
    def __init__(self, field, context, request):
        self.context = context
        self.request = request
        self.field = field

    def __call__(self):
        return json_compatible(self.get_value())

    def get_value(self, default=None):
        return getattr(self.field.interface(self.context), self.field.__name__, default)


@adapter(IChoice, IDexterityContent, Interface)
@implementer(IFieldSerializer)
class ChoiceFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        # Binding is necessary for named vocabularies
        if IField.providedBy(self.field):
            self.field = self.field.bind(self.context)
        value = self.get_value()
        if value is not None and IVocabularyTokenized.providedBy(self.field.vocabulary):
            try:
                term = self.field.vocabulary.getTerm(value)
                value = {"token": term.token, "title": term.title}
            # Some fields (e.g. language) have a default value that is not in
            # vocabulary
            except LookupError:
                pass
        return json_compatible(value)


@adapter(ICollection, IDexterityContent, Interface)
@implementer(IFieldSerializer)
class CollectionFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        # Binding is necessary for named vocabularies
        if IField.providedBy(self.field):
            self.field = self.field.bind(self.context)
        value = self.get_value()
        value_type = self.field.value_type
        if (
            value is not None
            and IChoice.providedBy(value_type)
            and IVocabularyTokenized.providedBy(value_type.vocabulary)
        ):
            values = []
            for v in value:
                try:
                    term = value_type.vocabulary.getTerm(v)
                    values.append({u"token": term.token, u"title": term.title})
                except LookupError:
                    log.warning("Term lookup error: %r" % v)
            value = values
        return json_compatible(value)


@adapter(INamedImageField, IDexterityContent, Interface)
class ImageFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        image = self.field.get(self.context)
        if not image:
            return None

        width, height = image.getImageSize()

        url = get_original_image_url(self.context, self.field.__name__, width, height)

        scales = get_scales(self.context, self.field, width, height)
        result = {
            "filename": image.filename,
            "content-type": image.contentType,
            "size": image.getSize(),
            "download": url,
            "width": width,
            "height": height,
            "scales": scales,
        }
        return json_compatible(result)


@adapter(INamedFileField, IDexterityContent, Interface)
class FileFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        namedfile = self.field.get(self.context)
        if namedfile is None:
            return None

        url = "/".join((self.context.absolute_url(), "@@download", self.field.__name__))
        result = {
            "filename": namedfile.filename,
            "content-type": namedfile.contentType,
            "size": namedfile.getSize(),
            "download": url,
        }
        return json_compatible(result)


@adapter(IRichText, IDexterityContent, Interface)
class RichttextFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        value = self.get_value()
        return json_compatible(value, self.context)


if ILink is not None:

    @adapter(ITextLine, ILink, Interface)
    class TextLineFieldSerializer(DefaultFieldSerializer):
        def __call__(self):
            if self.field.getName() != "remoteUrl":
                return super(TextLineFieldSerializer, self).__call__()
            value = self.get_value()
            path = replace_link_variables_by_paths(context=self.context, url=value)
            portal = getMultiAdapter(
                (self.context, self.context.REQUEST), name="plone_portal_state"
            ).portal()
            ref_obj = portal.restrictedTraverse(path, None)
            if ref_obj:
                value = ref_obj.absolute_url()
            return json_compatible(value)


@adapter(IField, IDexterityContent, Interface)
@implementer(IPrimaryFieldTarget)
class DefaultPrimaryFieldTarget(object):
    def __init__(self, field, context, request):
        self.context = context
        self.request = request
        self.field = field

    def use_primary_field_target(self):
        sm = getSecurityManager()
        perm = bool(sm.checkPermission(ModifyPortalContent, self.context))
        if perm:
            return False
        return True

    def __call__(self):
        return


@adapter(INamedFileField, IDexterityContent, Interface)
class PrimaryFileFieldTarget(DefaultPrimaryFieldTarget):
    def __call__(self):
        if not self.use_primary_field_target():
            return

        namedfile = self.field.get(self.context)
        if namedfile is None:
            return

        return "/".join(
            (self.context.absolute_url(), "@@download", self.field.__name__)
        )
