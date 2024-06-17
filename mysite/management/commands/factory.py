from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run Factory Script from Python File'

    def add_arguments(self, parser):
        parser.add_argument('factoryFile', type=str, help='File location')

    def handle(self, *args, **options):
        factoryFile = options['factoryFile']
        self.stdout.write('[#] Begin execute...')
        with open(factoryFile) as f:
            exec(f.read())
        # print(factoryFile)
        self.stdout.write('[#] DONE!')