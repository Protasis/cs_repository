from django.db import models
from django.db.models import permalink
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


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


class Project(models.Model):
    """ this class represents a paper (i.e. syssec, protasis)
    it will act as a container for any materia (papers, whitepapers,
    wiki with material...) """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    description = models.TextField()


class WhitePaper(models.Model):
    """ this class similarly to Paper represent
    a whitepaper, or dissemination material """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    abstract = models.TextField()
    code = models.URLField(null=True, blank=True)
    data = models.FileField(null=True, blank=True, upload_to=settings.DATA_FOLDER)

    data_protected = models.BooleanField(default=False)

    paper = models.FileField(null=True, blank=True, upload_to=settings.PAPER_FOLDER)
    url = models.URLField(null=True, blank=True)
    corresponding = models.ForeignKey(
        InstitutionAuthor, null=True, blank=True,
        related_name="+", on_delete=models.SET_NULL)
    authors = models.ManyToManyField(InstitutionAuthor)

    wp_paper_access = models.ManyToManyField(User, related_name="can_access_paper_wp", blank=True)
    wp_data_access = models.ManyToManyField(User, related_name="can_access_data_wp", blank=True)
    wp_code_access = models.ManyToManyField(User, related_name="can_access_code_wp", blank=True)

    bibtex = models.TextField(null=True, blank=True)

    venue = models.ForeignKey(Venue, null=True)

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


class Data(models.Model):
    """ this class represent data associated
    to a paper, or a project """
    pass


class Code(models.Model):
    """ this class represent data associated
    to a paper, or a project """
    pass


class Paper(models.Model):
    """ this class represent a paper
    it contains title, authors ref, conference,
    dataset, code and bibtex ref"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    abstract = models.TextField()
    code = models.URLField(null=True, blank=True)
    data = models.FileField(null=True, blank=True, upload_to=settings.DATA_FOLDER)

    data_protected = models.BooleanField(default=False)

    paper = models.FileField(null=True, blank=True, upload_to=settings.PAPER_FOLDER)
    url = models.URLField(null=True, blank=True)
    corresponding = models.ForeignKey(
        InstitutionAuthor, null=True, blank=True,
        related_name="+", on_delete=models.SET_NULL)
    authors = models.ManyToManyField(InstitutionAuthor)

    pa_paper_access = models.ManyToManyField(User, related_name="can_access_paper", blank=True)
    pa_data_access = models.ManyToManyField(User, related_name="can_access_data", blank=True)
    pa_code_access = models.ManyToManyField(User, related_name="can_access_code", blank=True)

    bibtex = models.TextField(null=True, blank=True)

    venue = models.ForeignKey(Venue, null=True)

    @permalink
    def get_absolute_url(self):
        return reverse('views.paper', args=[str(self.id), str(self.slug)])

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


class UserPerms(models.Model):
    user = models.OneToOneField(User)
    usr_project_access = models.ManyToManyField(Project, related_name="can_access_paper", blank=True)
    usr_paper_access = models.ManyToManyField(Paper, related_name="can_access_paper", blank=True)
    usr_data_access = models.ManyToManyField(Data, related_name="can_access_paper", blank=True)
    usr_code_access = models.ManyToManyField(Code, related_name="can_access_paper", blank=True)
