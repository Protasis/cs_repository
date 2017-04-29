from django.db import models

# Create your models here.


class Institution(models.Model):
    name = models.CharField(max_length=256)
    website = models.URLField()


class Author(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    institution = models.ForeignKey(Institution)
    email = models.EmailField()


class InstitutionAuthor(models.Model):
    author = models.ForeignKey(Author)
    institution = models.ForeignKey(Institution)



class Project(models.Model):
    """ this class represent a project/paper
    it contains title, authors ref, conference,
    dataset, code and bibtex ref"""
    authorlist = models.ForeignKey(InstitutionAuthor)
    name = models.CharField(max_length=256)
    abstract = models.CharField(max_length=5*1024)
    code = models.URLField()
    data = models.URLField()
    paper = models.URLField()
    url = models.URL()
    corresponding_email = models.EmailField()
