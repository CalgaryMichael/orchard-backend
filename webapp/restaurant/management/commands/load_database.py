import io
import requests
import time
from django.core.management.base import BaseCommand
from django.db import transaction
from webapp.restaurant import etl


class Command(BaseCommand):
    help = "Runs ETL on a given file or URL"

    def add_arguments(self, parser):
        parser.add_argument("--file", default=None, type=str)
        parser.add_argument("--url", default=None, type=str)

    def handle(self, *args, **options):
        start = time.time()
        file_ = options.get("file")
        url = options.get("url")
        assert file_ or url, "Please specify a file location or a URL"
        assert not (file_ and url), "Please only specify a file location or a URL"

        if file_:
            print("Opening file from provided location...")
            with io.open(file_, "r", encoding="ISO-8859-1") as csv_buffer:
                print("Running ETL...")
                with transaction.atomic():
                    etl.etl(csv_buffer)
        else:
            print("Retrieving file from provided URL...")
            response = requests.get(url)
            print("Running ETL...")
            with transaction.atomic():
                etl.etl(io.BytesIO(response.content))
        print("Done in '{}'".format(time.time() - start))
