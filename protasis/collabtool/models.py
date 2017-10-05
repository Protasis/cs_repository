from django.db import models
from django.db.models import permalink
from django.apps import apps
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import ManyToManyField
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from utils import ChoiceEnum
# Create your models here.


class GroupAccess(models.Model):

    class Meta:
        verbose_name_plural = "group accesses"

    group = models.ForeignKey(Group, null=False)
    read = models.BooleanField(default=False)

    # right now write permission is unused will need
    # further work in django admin to limit the scope
    # of how much a user can modify
    write = models.BooleanField(default=False)

    def short_description(self):

        perm_str = ""
        if self.read:
            perm_str += 'r'
        else:
            perm_str += '-'

        if self.write:
            perm_str += 'w'
        else:
            perm_str += '-'

        return "%s [%s]" % (self.group.name, perm_str)

    def __unicode__(self):
        return self.short_description()

    def __str__(self):
        return self.short_description()


class AuthMixin(models.Model):
    """ all fields/methods related to auth here """

    class Meta:
        abstract = True

    group_access = models.ManyToManyField(GroupAccess, blank=True)
    anonymous_access = models.BooleanField(default=False)

    def get_model_name(self, plural=False):
        name = self._meta.model_name.capitalize
        if plural:
            return name()+'s'
        return name()

    def get_pl_model_name(self):
        return self.get_model_name(True)

    '''@classmethod
    def all_accessible(cls, user, recursion=0, done=[], out={}):
        """ this method will return any model instance that the user can access
        if recursion>0 it will traverse all the fields of the model and if there
        is an authenticable one will return also accessible list for it"""

        out = {}

        if recursion == 0:
            done = list()

        if cls in done:
            return out

        done.append(cls)

        if recursion > 0:
            for k, v in cls.__dict__.iteritems():
                if (  # isinstance(v, ManyToManyDescriptor) and
                   issubclass(v.rel.field.related_model, AuthMixin)):
                    res = v.rel.field.related_model.get_accessible(
                                user, recursion-1, done)
                    if res:
                        out.update(res)

        return out'''

    @staticmethod
    def check_inj(s):
        import string
        tocheck = s.encode('utf-8').translate(string.maketrans("", "", ), '-_')
        if not tocheck.isalnum():
            raise SuspiciousOperation

    @classmethod
    def get_accessible(cls, user, unlinked=False):
        """ get all the accessible instances of the model """

        accessible_objs = cls.objects.filter(
            Q(group_access__group_id__in=map(lambda x: x.id,  user.groups.all())) |
            Q(anonymous_access=True))

        if accessible_objs:
            accessible_objs = list(accessible_objs)
        else:
            return []

        if not unlinked:
            return accessible_objs

        print accessible_objs
        if issubclass(cls, PublicationBase):
            # if it's a publication we need to scan Publication model too
            ct = ContentType.objects.filter(Q(app_label='collabtool') and Q(model=cls.__name__)).first()
            if ct:
                pub = Publication.objects.filter(
                        Q(content_type=ct.id) and Q(id__in=map(lambda x: x.id, accessible_objs)))
                for p in pub:
                    for mm in p._meta.related_objects:
                        if getattr(p, '%s_set' % mm.name).all().count() > 0:
                            try:
                                accessible_objs.remove(p.content_object)
                            except ValueError:
                                pass

        for i in accessible_objs:
            for mm in i._meta.related_objects:
                if getattr(i, '%s_set' % mm.name).all().count() > 0:
                    accessible_objs.remove(i)

        return accessible_objs

    def accessible_rel(self, user, m2m_field):
        from django.forms.models import model_to_dict
        """ get the accessible instances of a given model that is in a many-to-many relationship
        with the current field """
        model_name = self._meta.model_name
        model = m2m_field.related_model
        model_table = self._meta.db_table
        rel_model_table = model._meta.db_table
        mm_table = self.__class__.__dict__[m2m_field.attname].rel.field.m2m_db_table()

        self.check_inj(model_table)
        self.check_inj(rel_model_table)
        self.check_inj(mm_table)
        self.check_inj(m2m_field.attname)
        self.check_inj(model_name)

        uid = user.id
        fid = self.id
        query = '''
        SELECT * FROM
        %s as F, collabtool_groupaccess as GA, %s_group_access as FGA,
        auth_user_groups as AU, %s as MM
        WHERE  F.anonymous_access=TRUE OR (AU.group_id=GA.group_id AND
        GA.id=FGA.groupaccess_id AND
        FGA.%s_id=F.id AND
        F.id=MM.%s_id AND
        MM.%s_id = %d''' % (
            rel_model_table, rel_model_table, mm_table,
            m2m_field.attname, m2m_field.attname, model_name, fid)
        if user.is_authenticated:
            query += '''
AND AU.user_id=%d''' % (uid)
        query += ''')'''

        out = []
        for i in getattr(self, m2m_field.attname).all():
            if i.is_accessible(user):
                out.append(i)

        return out
        # res = model.objects.raw(query)
        # if res:
        #    ret = list(res)
        #    print ret
        #    return ret
        # else:
        #    return []

    def all_accessible_rel(self, user):
        """ this function will return the linked authenticable objects"""
        from collections import defaultdict, OrderedDict
        from operator import itemgetter

        out = defaultdict(list)

        # cls = self._meta.model
        done = []
        for f in self._meta.many_to_many:
            if (isinstance(f, ManyToManyField) and
               (issubclass(f.related_model, AuthMixin)
                or issubclass(f.related_model, Publication))
               and f.related_model not in done):
                res = self.accessible_rel(user, f)
                if issubclass(f.related_model, Publication):
                    for p in res:
                        out[p.content_object._meta.model].append(p)
                else:
                    out[f.related_model] = res
                done.append(f.related_model)

        return OrderedDict(sorted(dict(out).items(), key=itemgetter(0)))

    def is_accessible(self, user):
        return self.anonymous_access or bool(frozenset(user.groups.all()) and frozenset(self.group_access.all()))


class Venue(models.Model):
    name = models.CharField(max_length=256)
    acronym = models.CharField(max_length=256)
    date = models.DateField()
    location = models.CharField(max_length=256)

    def short_description(self):
        return self.acronym

    def __unicode__(self):
        return self.short_description()

    def __str__(self):
        return self.short_description()


class Institution(models.Model):
    name = models.CharField(max_length=256)
    website = models.URLField()

    def short_description(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    website = models.URLField(null=True, blank=True)

    def short_name(self):
        return ". ".join([x[0] + '.' for x in str(self.name).split(' ')]) + " " + str(self.surname)
    short_name.short_description = 'Name'

    def __str__(self):
        return self.short_name()

    def save(self, *args, **kwargs):
        if not self.website:
            self.website = None
        super(Author, self).save(*args, **kwargs)


class InstitutionAuthor(models.Model):
    """ since one author can have more than one affiliation
    we will need this intermediate model, probably there are better ways
    to do this with django, but I'll stick to the simplest option for now"""
    author = models.ForeignKey(Author)
    institution = models.ForeignKey(Institution, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def short_description(self):
        out = self.author.short_name()
        if self.institution:
            out += "[%s]" % self.institution.short_description()
        return out

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()


class File(models.Model):
    """ this class represent data associated
    to a paper, or a project """

    class Meta:
        abstract = True

    title = models.CharField(max_length=255, null=False, default='')
    slug = models.SlugField(max_length=255, unique=True, default='')
    url = models.URLField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to=settings.DATA_FOLDER)
    sha512 = models.CharField(max_length=128, null=True, default='')

    def save(self):
        def sha512(f):
            import hashlib
            hash_sha512 = hashlib.sha512()
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
            f.seek(0)
            return hash_sha512.hexdigest()

        if self.file:
            self.sha512 = sha512(self.file)

        self.slug = slugify(self.title)

        return super(File, self).save()

    def short_description(self):
        if self.title:
            return self.title
        else:
            return self.__class__.__name__

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()

    def get_file_url(self):
        import os
        if (self.sha512 and self.file.name):
            return reverse('get_data', args=(self.sha512, os.path.split(self.file.name)[-1]))

    def get_absolute_url(self):
        return self.get_file_url()


class Data(AuthMixin, File):

    class Meta:
        verbose_name_plural = "data"

    def get_pl_model_name(self):
        return self._meta.verbose_name_plural.capitalize()


class Code(AuthMixin, File):
    """ this class represent code associated
    to a paper, or a project """

    class Meta:
        verbose_name_plural = "code"

    def get_pl_model_name(self):
        return self._meta.verbose_name_plural.capitalize()


class Vulnerability(File):

    class Meta:
        verbose_name_plural = "vulnerabilities"

    def get_pl_model_name(self):
        return self._meta.verbose_name_plural.capitalize()


class Publication(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def is_accessible(self, user):
        return self.content_object.is_accessible(user)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def short_description(self):
        if not self.object_id:
            return self.__class__.__name__

        desc = ''
        pub = self.content_object
        c = pub.authors.count()
        if c:
            for a in pub.authors.all():
                c -= 1
                if c > 0:
                    m = ','
                else:
                    m = '. '
                desc += '%s%s' % (a.author.short_name(), m)

        desc += '%s. %s' % (pub.title, pub.date.strftime("%B, %Y"))
        return desc

    def __str__(self):              # __unicode__ on Python 2
        if self.object_id:
            return self.content_object.__str__()
        else:
            return self.__class__.__name__


class PublicationBase(AuthMixin, File, models.Model):

    class Meta:
        abstract = True

    @staticmethod
    def get_pub_related_name():
        name = '%(app_label)s_%(class)s'
        return name

    abstract = models.TextField(null=False, blank=True, default='')
    authors = models.ManyToManyField(InstitutionAuthor, blank=True, related_name=get_pub_related_name.__func__())
    corresponding = models.ForeignKey(
        InstitutionAuthor, null=True, blank=True,
        related_name="+", on_delete=models.SET_NULL)
    venue = models.ForeignKey(Venue, null=True, blank=True)
    date = models.DateField()
    data = models.ManyToManyField(Data, blank=True)
    code = models.ManyToManyField(Code, blank=True)
    bibtex = models.TextField(null=True, blank=True)

    # Status of the publication
    class EStatuses(ChoiceEnum):
        draft = 0
        submitted = 1
        accepted = 2
        published = 3

    status = models.CharField(max_length=1, choices=EStatuses.choices(), default=EStatuses.published.value)
    doi = models.CharField(max_length=128, verbose_name='DOI', blank=True, null=True, unique=True)
    isbn = models.CharField(max_length=32, verbose_name='ISBN', blank=True, null=True, unique=True,
                            help_text='Only for a book.')  # A-B-C-D

    @classmethod
    def iter_subclasses(cls):
        return iter(cls.__subclasses__())

    def get_absolute_url(self):
        return reverse('get_check', args=(self.__class__.__name__.lower(), str(self.id), str(self.slug)))

    def save(self, *args, **kwargs):

        for x in [self.venue, self.bibtex, self.corresponding, self.abstract]:
            if not x:
                x = None

        super(PublicationBase, self).save(*args, **kwargs)

    def export_bibtex(self):
        if self.bibtex:
            return self.bibtex

        # TODO: export bibtex from inserted fields if bibtex not present


class Paper(PublicationBase):
    """ this class represent a paper
    it contains title, authors ref, conference,
    dataset, code and bibtex ref"""

    @staticmethod
    def get_ticket_related_name():
                return 'papers_rel'


class Report(PublicationBase):
    """ this class similarly to Paper represent
    a whitepaper, or dissemination material """

    @staticmethod
    def get_ticket_related_name():
                return 'reports_rel'


class Deliverable(PublicationBase):
    """ this class represents a deliverable publication """

    @staticmethod
    def get_ticket_related_name():
                return 'reports_rel'


class Project(AuthMixin, models.Model):
    """ this class represents a paper (i.e. syssec, protasis)
    it will act as a container for any materia (papers, whitepapers,
    wiki with material...) """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    data = models.ManyToManyField(Data, blank=True)
    code = models.ManyToManyField(Code, blank=True)
    publication = models.ManyToManyField(Publication, blank=True)
    institutions = models.ManyToManyField(Institution, blank=True)

    def get_wiki_url(self):
        # TODO: creating programmatically entries
        # will take a while, let's do it later...

        url = reverse('wiki:get',
                      kwargs={'path': self.slug+'/'})
        return url

    def get_absolute_url(self):
        return reverse('get_check', args=['project', str(self.id), str(self.slug)])

    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)

        super(Project, self).save(*args, **kwargs)

    def short_description(self):
        return self.title

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()
