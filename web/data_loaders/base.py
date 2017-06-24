import csv

from es import get_es

__index_name__ = 'engine'
__doc_type__ = 'listing'


class Loader(object):
    """ Load data from files and get rid of the unwanted information for now
    and indexes the titles in elasticsearch
    """
    def __init__(self, file_name):
        self.es = get_es()
        self.file_name = file_name

    def _parse_file(self):
        """ Parse the CSV file and yield row
        TODO: very hacky, make it robust and yield chunks and do bulk indexing
        limited memory for now.
        """
        with open(self.file_name, "rt") as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # skip the headers
            for row in reader:
                yield row

    def _configure_index(self):
        """ Create index and doctype
        """
        self.es.indices.create(index=__index_name__)
        self.es.indices.put_mapping(
            index=__index_name__,
            doc_type=__doc_type__,
            ignore_conflicts='true',
            body={
                'listings': {
                    'properties': {
                        'item_id': {
                            "type": "integer", "store": "true"
                        },
                        'title': {
                            "type": "string", "store": "true"
                        }
                    }
                }
            })

    def index_items(self):
        """ Index titles in elasticsearch
        """
        for row in self._parse_file():
            try:
                self.es.index(
                    index=__index_name__, doc_type=__doc_type__,
                    body={'item_id': row[1], 'title': row[3]}
                )
            except:
                continue
        return self.es.count(index=__index_name__, doc_type=__doc_type__)
