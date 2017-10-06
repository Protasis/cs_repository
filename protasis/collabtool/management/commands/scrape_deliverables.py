from BeautifulSoup import BeautifulSoup
from collabtool.models import Deliverable, Group
from django.core.management.base import BaseCommand, CommandError
import os
import urlparse
from rfc3987 import parse

SYSSEC_URL = 'http://www.syssec-project.eu'


def save_deliv(g, d):
    pass


def scrape_deliv(fname):
    b = BeautifulSoup(open(fname, 'r').read())

    n = b.findAll('h2')[0]

    syssec_group = Group.objects.filter(name='syssec').first()

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
                title = li.contents[1].text.strip()
                url = dict(li.find('a').attrs)['href']
                # ensure validity of url
                try:
                    parse(url)
                except ValueError:
                    url = SYSSEC_URL+url
                    parse(url)

                d = Deliverable(title=title, url=url)
                save_deliv(syssec_group, d)


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
