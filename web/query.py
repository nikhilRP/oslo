from es import get_es


class Query(object):
    """ Construct query based on the seed item and then recommend items
    """
    def __init__(self, seed_title, quality=False):
        self.seed = seed_title
        self.quality = quality
        self.es = get_es()

    def _select_clusters(self):
        self.es.search(index='engine', doc_type='cluster')

    def _ranking_function(self):
        pass

    def _construct_query(self, boost_fields):
        pass

    def get_recommendations(self):
        pass
