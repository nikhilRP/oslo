import csv
import logging

from elasticsearch import Elasticsearch

__index_name__ = 'engine'
__doc_type__ = 'listing'

logger = logging.getLogger('web_1')


class Loader(object):
    """ Load data from files and get rid of the unwanted information for now
    """

    def __init__(self, file_name):
        self.es = Elasticsearch(['192.168.99.100'], port=9200)
        self.file_name = file_name

    def _parse_file(self):
        """ Parse the CSV file and yield row
        TODO: very hacky, make it robust and yield chunks
        """
        with open(self.file_name, "rt") as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # skip the headers
            for row in reader:
                yield row

    def _configure_index(self):
        """ Create index and doctype
        """
        try:
            self.es.indices.create(index=__index_name__)
            self.es.indices.put_mapping(
                index=__index_name__,
                doc_type=__doc_type__,
                ignore_conflicts='true',
                body={
                    'listings': {
                        'properties': {
                            'item_id': {
                                "type": 'integer', "store": "true"
                            },
                            'title': {
                                "type": "string", "store": "true"
                            }
                        }
                    }
                })
        except Exception as e:
            logger.info(e)
            return False
        return True

    def index_items(self):
        """ Index titles in elasticsearch
        """
        for row in self._parse_file():
            logger.info(row)
            self.es.index(
                index=__index_name__, doc_type=__doc_type__,
                body={'item_id': row[1], 'title': row[3]}
            )
        return self.es.count(index=__index_name__, doc_type=__doc_type__)
