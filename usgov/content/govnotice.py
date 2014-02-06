# -*- coding:utf-8 -*-
from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder


from usgov.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IGovNotice(form.Schema, IImageScaleTraversable):
    """
    Gov Notice content type for usgov
    """

    #案名
    noticeTitle = schema.TextLine(
        title=_(u'Notice Title'),
        required=False,
    )

    #案號
    solicitationNumber = schema.TextLine(
        title=_(u'Solicitation Number'),
        required=False,
    )

    #標案型態
    noticeType = schema.TextLine(
        title=_(u'Notice Type'),
        required=False,
    )

    #描述
    synopsis = schema.Text(
        title=_(u'Synopsis'),
        required=False,
    )

    #承辦地址
    contractingOfficeAddress = schema.Text(
        title=_(u'Contracting Office Address'),
        required=False,
    )

    #履約地點
    placeOfPerformance = schema.Text(
        title=_(u'Place Of Formance'),
        required=False,
    )

    #承辦聯絡人
    primaryPointOfContact = schema.Text(
        title=_(u'Primary Point Of Contact'),
        required=False,
    )

    #承辦代理人
    secondaryPointOfContact = schema.Text(
        title=_(u'Secondary Point of Contact'),
        required=False,
    )

    #發佈日期
    postedDate = schema.Datetime(
        title=_(u'Posted Date'),
        required=True,
    )

    #聯聯公告
    #不需要，用noticeTitle及solicitationNumber就可以


    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/govnotice.xml to define the content type.

    # form.model("models/govnotice.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class GovNotice(Container):
    grok.implements(IGovNotice)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# govnotice_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IGovNotice)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
