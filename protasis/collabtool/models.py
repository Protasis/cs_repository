from django.db import models
from django.db.models import permalink
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import ManyToManyField
from django.core.exceptions import SuspiciousOperation
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

    group_access = models.ManyToManyField(GroupAccess)
    anonymous_access = models.BooleanField(default=False)

    @classmethod
    def all_accessible(cls, user, recursion=0, done=[], out={}):
        """ this method will return any model instance that the user can access
        if recursion>0 it will traverse all the fields of the model and if there
        is an authenticable one will return also accessible list for it"""

        out = {}

        if recursion == 0:
            done = list()

        if cls in done:
            return out

        print cls
        done.append(cls)

        print done
        if recursion > 0:
            print recursion
            for k, v in cls.__dict__.iteritems():
                if (  # isinstance(v, ManyToManyDescriptor) and
                   issubclass(v.rel.field.related_model, AuthMixin)):
                    print v.rel.field.related_model
                    res = v.rel.field.related_model.get_accessible(
                                user, recursion-1, done)
                    if res:
                        out.update(res)

        return out

    def accessible_fields(self, user):
        """ this function will return recursively the linked authenticable objects"""

        out = {}

        def cls_query(user, model):
            model_name = self._meta.model.__name__.lower()
            rel_model_name = model.__name__.lower()
            if not (model_name.isalnum() and rel_model_name.isalnum()):
                raise SuspiciousOperation
            uid = user.id
            fid = self.id
            query = '''
SELECT * FROM
        collabtool_%s as F, collabtool_groupaccess as GA, collabtool_%s_group_access as FGA,
        auth_user_groups as AU, collabtool_%s_%s as MM
WHERE AU.user_id=%d AND
        AU.group_id=GA.group_id AND
        GA.id=FGA.groupaccess_id AND
        FGA.%s_id=F.id AND
        F.id=MM.%s_id AND
        MM.%s_id = %d''' % (rel_model_name,
                            rel_model_name,
                            model_name,
                            rel_model_name,
                            uid,
                            rel_model_name,
                            rel_model_name,
                            model_name,
                            fid)
            print query

            return model.objects.raw(query)

        # cls = self._meta.model
        done = []
        for f in self._meta.many_to_many:
            if (isinstance(f, ManyToManyField) and
               issubclass(f.related_model, AuthMixin) and
               f.related_model not in done):
                res = cls_query(user, f.related_model)
                if res:
                    out[f.related_model] = list(res)
                done.append(f.related_model)
        return out

    def is_accessible(self, user):
        return True


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
    author = models.ForeignKey(Author, related_name='institutions')
    institution = models.ForeignKey(Institution)
    email = models.EmailField()

    def short_description(self):
        return self.author.short_name() + " - " + self.institution.short_description()

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
    data = models.FileField(null=True, blank=True, upload_to=settings.DATA_FOLDER)
    sha512 = models.CharField(max_length=128, null=True, default='')

    def save(self):
        def sha512(f):
            import hashlib
            hash_sha512 = hashlib.sha512()
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
            f.seek(0)
            return hash_sha512.hexdigest()

        if self.data:
            self.sha512 = sha512(self.data)

        return super(File, self).save()

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()


class Data(AuthMixin, File):

    class Meta:
        verbose_name_plural = "data"

    def short_description(self):
        return 'data: ' + self.title


class Code(AuthMixin, File):
    """ this class represent code associated
    to a paper, or a project """

    class Meta:
        verbose_name_plural = "code"

    def short_description(self):
        return 'code: ' + self.title


class Publication(AuthMixin, models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):              # __unicode__ on Python 2
        return self.content_object.__str__()


class PublicationBase(AuthMixin, models.Model):

    class Meta:
        abstract = True

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    abstract = models.TextField(null=False)
    paper = models.FileField(null=True, blank=True, upload_to=settings.PAPER_FOLDER)
    url = models.URLField(null=True, blank=True)
    corresponding = models.ForeignKey(
        InstitutionAuthor, null=True, blank=True,
        related_name="+", on_delete=models.SET_NULL)
    authors = models.ManyToManyField(InstitutionAuthor)
    bibtex = models.TextField(null=True, blank=True)
    venue = models.ForeignKey(Venue, null=True)

    @classmethod
    def iter_subclasses(cls):
        for p in cls.__subclasses__():
            yield p

    def get_absolute_url(self):
        return reverse('get_check', self.__class__.__name__.lower(), args=[str(self.id), str(self.slug)])

    def short_description(self):
        return self.title

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()

    def save(self, *args, **kwargs):

        for x in [self.code, self.url, self.bibtex, self.corresponding]:
            if not x:
                x = None

        self.slug = slugify(self.title)

        super(WhitePaper, self).save(*args, **kwargs)


class Paper(PublicationBase):
    """ this class represent a paper
    it contains title, authors ref, conference,
    dataset, code and bibtex ref"""

    pass


class WhitePaper(PublicationBase):
    """ this class similarly to Paper represent
    a whitepaper, or dissemination material """

    pass


class Deliverable(PublicationBase):
    """ this class represents a deliverable publication """

    pass


class Project(AuthMixin, models.Model):
    """ this class represents a paper (i.e. syssec, protasis)
    it will act as a container for any materia (papers, whitepapers,
    wiki with material...) """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    data = models.ManyToManyField(Data, blank=True, related_name='project_data')
    code = models.ManyToManyField(Code, blank=True, related_name='project_code')
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

        print self.get_wiki_url()

        super(Project, self).save(*args, **kwargs)

    def short_description(self):
        return self.title

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()
