from django.db import models
from django.db.models import permalink
from django.urls import reverse

# Create your models here.


class Venue(models.Model):
    name = models.CharField(max_length=256)
    acronym = models.CharField(max_length=256)
    date = models.DateField()
    location = models.CharField(max_length=256)


class Institution(models.Model):
    name = models.CharField(max_length=256)
    website = models.URLField()


class Author(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    website = models.URLField()

    @property
    def short_name(self):
        return ". ".join([x for x in str(self.name).split(' ')]) + str(self.surname)


class InstitutionAuthor(models.Model):
    """ since one author can have more than one affiliation
    we will need this intermediate model, probably there are better ways
    to do this with django, but I'll stick to the simplest option for now"""
    author = models.ForeignKey(Author, related_name='institutions')
    institution = models.ForeignKey(Institution)
    email = models.EmailField()


class Project(models.Model):
    """ this class represent a project/paper
    it contains title, authors ref, conference,
    dataset, code and bibtex ref"""

    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    abstract = models.TextField()
    code = models.URLField()
    data = models.URLField()
    paper = models.URLField()
    url = models.URLField()
    corresponding = models.ForeignKey(InstitutionAuthor, related_name="+")
    authors = models.ManyToManyField(InstitutionAuthor)

    bibtex = models.TextField()
    venue = models.ForeignKey(Venue)

    @permalink
    def get_absolute_url(self):
        return reverse('views.project', args=[str(self.id), str(self.slug)])
