from django.db import models
from django.db.models import permalink
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User, Group
from django.conf import settings
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


class Data(models.Model):
    """ this class represent data associated
    to a paper, or a project """

    title = models.CharField(max_length=255, null=False, default='')
    slug = models.SlugField(max_length=255, unique=True, default='')
    url = models.URLField(null=True, blank=True)
    data = models.FileField(null=True, blank=True, upload_to=settings.DATA_FOLDER)
    protected = models.BooleanField(default=False)
    group_access = models.ManyToManyField(GroupAccess)

    class Meta:
        verbose_name_plural = "data"

    def short_description(self):
        return self.__class__.__name__
        return 'data: ' + self.title

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()


class Code(models.Model):
    """ this class represent data associated
    to a paper, or a project """
    title = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=255, unique=True, default='')
    url = models.URLField(null=True, blank=True)
    code = models.FileField(null=True, blank=True, upload_to=settings.PAPER_FOLDER)
    protected = models.BooleanField(default=False)
    group_access = models.ManyToManyField(GroupAccess)

    class Meta:
        verbose_name_plural = "code"

    def short_description(self):
        return 'code: ' + self.title

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()


class Publication(models.Model):

    @permalink
    def get_absolute_url(self):
        return reverse('views.' + self.__class__.__name__.lower(), args=[str(self.id), str(self.slug)])

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

    group_access = models.ManyToManyField(GroupAccess)

    class Meta:
        abstract = True


class Paper(Publication):
    """ this class represent a paper
    it contains title, authors ref, conference,
    dataset, code and bibtex ref"""

    def save(self, *args, **kwargs):

        for x in [self.code, self.url, self.bibtex, self.corresponding]:
            if not x:
                x = None

        self.slug = slugify(self.title)
        print(self.slug)

        super(Paper, self).save(*args, **kwargs)

    def short_description(self):
        return self.title

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()


class WhitePaper(Publication):
    """ this class similarly to Paper represent
    a whitepaper, or dissemination material """

    @permalink
    def get_absolute_url(self):
        return reverse('views.whitepaper', args=[str(self.id), str(self.slug)])

    def save(self, *args, **kwargs):

        for x in [self.code, self.url, self.bibtex, self.corresponding]:
            if not x:
                x = None

        self.slug = slugify(self.title)
        print(self.slug)

        super(WhitePaper, self).save(*args, **kwargs)

    def short_description(self):
        return self.title

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()


class Project(models.Model):
    """ this class represents a paper (i.e. syssec, protasis)
    it will act as a container for any materia (papers, whitepapers,
    wiki with material...) """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    data = models.ManyToManyField(Data, blank=True)
    code = models.ManyToManyField(Code, blank=True)
    paper = models.ManyToManyField(Paper, blank=True)
    whitepaper = models.ManyToManyField(WhitePaper, blank=True)
    institutions = models.ManyToManyField(Institution, blank=True)
    wiki = models.URLField(default='/collabtool/wiki/')
    # here we keep the "links" between a project and a paper/whitepaper and so on
    # when "saving a paper we need a link to the project and the associated datas?
    # if project<-paper<-(data+code) I can get the list of associated data/code having
    # only some more stuff there
    # permission side we just need to check access for the user to the single resource!

    group_access = models.ManyToManyField(GroupAccess, blank=True)

    @permalink
    def get_absolute_url(self):
        print self.name
        return reverse('views.project', args=[str(self.id), str(self.slug)])

    def save(self, *args, **kwargs):

        for x in [self.code, self.url, self.bibtex, self.corresponding]:
            if not x:
                x = None

        self.slug = slugify(self.title)
        print(self.slug)

        super(Project, self).save(*args, **kwargs)

    def short_description(self):
        return self.title

    def __str__(self):
        return self.short_description()

    def __unicode__(self):
        return self.short_description()
