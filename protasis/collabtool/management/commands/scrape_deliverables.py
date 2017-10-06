from BeautifulSoup import BeautifulSoup, NavigableString
from collabtool.models import Deliverable, Group, GroupAccess
from django.core.management.base import BaseCommand, CommandError
import os
import urlparse
from rfc3987 import parse as rfc3987_parse
from dateutil.parser import parse as dateutil_parse
import re

SYSSEC_URL = 'http://www.syssec-project.eu'
DEBUG = True


def scrape_deliv(fname):
    b = BeautifulSoup(open(fname, 'r').read())

    n = b.findAll('h2')[0]

    syssec_group = Group.objects.filter(name='syssec').first()
    group_access = GroupAccess.objects.filter(group=syssec_group).first()

    while True:
        n = n.nextSibling

        # stop parsing at next section
        if n.name == 'h2':
            break

        # parse the deliverables list
        if n.name == 'ul':
            for li in n.childGenerator():
                dt = li.contents[0].strip()

                if dt != 'SysSec Deliverable':
                    continue
                url = dict(li.find('a').attrs)['href']
                # ensure validity of url
                try:
                    rfc3987_parse(url, rule='IRI')
                except ValueError:
                    url = SYSSEC_URL+url
                    rfc3987_parse(url, rule='IRI')

                title = li.contents[1].text.strip()

                donext = True
                for c in li.contents[2:]:
                    ctext = str(c)
                    if isinstance(c, NavigableString) and ctext:
                        for d in re.findall("[\w\s]+", ctext):
                            try:
                                date = dateutil_parse(d)
                                donext = False
                                break
                            except ValueError:
                                donext = True
                    if not donext:
                        break
                    try:
                        title = "%s %s" % (title, c.contents[0].strip())
                    except AttributeError:
                        pass
                    if isinstance(c, NavigableString) and str(c):
                        title = "%s %s" % (title, str(c))
                        title = title.strip()

                d = Deliverable(title=title, url=url, date=date)
                if not DEBUG:
                    d.save()
                    d.group_access.add(group_access)
                    d.save()
                else:
                    print "%s (%s), %s" % (d.title, d.date, d.url)


class Command(BaseCommand):

    help = 'Scrape syssec deliverables'

    def add_arguments(self, parser):
        parser.add_argument(
            "-f", "--file", dest="filename", action="store",
            type=str, help="specify import file", metavar="FILE")

    def handle(self, *args, **options):
        if options['filename'] is None:
            raise CommandError("Option `--file=...` must be specified.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']):
            raise CommandError("File does not exist at the specified path.")
        scrape_deliv(options['filename'])
