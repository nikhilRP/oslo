import csv
import json

from es import get_es

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

__index_name__ = 'engine'
__doc_type__ = 'listing'
__c_doc_type__ = 'cluster'


class Cluster(object):
    """ Primarily used to query ES index and then cluster the results using
    tf-idf and k-means, number of clusters is selected by bootstraping
    silhouette_score

    NOTE: Due to infrastructure limitations clustering is limited to top 100
    search queries
    """
    def __init__(self, file_name):
        self.es = get_es()
        self.file_name = file_name

    def _parse_queries(self):
        queries = list()
        with open(self.file_name, "rt") as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # skip the headers
            for row in reader:
                queries.append(row[1])
        return queries

    def _get_search_results_for_query(self, query):
        """ Query ES for results and return then as list of sentences
        Return list of matching titles
        """
        data = self.es.search(
            index=__index_name__, doc_type=__doc_type__, body={
                "query": {
                    "match": {
                        "title": {
                            "query": query,
                            "fuzziness": "AUTO",
                            "operator":  "and"
                        },
                    },
                },
                "size": 10000
            })
        results = list()
        for result in data['hits']['hits']:
            results.append(result['_source']['title'])
        return results

    def _vectorize_data(self, data):
        """ vectorize data using tf-idf vectorizer

        TODO: Tune the params and extend similarity metric
        """
        vectorizer = TfidfVectorizer(stop_words='english')
        data = vectorizer.fit_transform(data)
        return data, vectorizer

    def _reduce_dimensions(self, data):
        """ Dimensionality reduction if required

        TODO: Tune number of dimensions, really depends on the search results
        """
        svd = TruncatedSVD(10)
        normalizer = Normalizer(copy=False)
        lsa = make_pipeline(svd, normalizer)
        X = lsa.fit_transform(data)
        return X, svd

    def _cluster(self, search_results):
        """ Cluster search results and tune then using max silhouette_score
        """
        clusters, max_score = dict(), 0

        # TODO: Very hacky probably should use grid search to maximize
        # silhouette_score or even randomized search
        for n_clusters in range(10, 1000, 10):
            X, vectorizer = self._vectorize_data(search_results)
            X, svd = self._reduce_dimensions(X)
            km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100)
            cluster_labels = km.fit_predict(X)
            score = metrics.silhouette_score(X, cluster_labels)
            if n_clusters == 0:
                max_score = score
            if max_score > score:
                break
            max_score = score

        clusters['score'] = max_score
        labels = dict(zip(search_results, cluster_labels.tolist()))
        for key, value in sorted(labels.items()):
            clusters.setdefault(str(value), []).append(key)
        centroids = svd.inverse_transform(km.cluster_centers_)
        order_centroids = centroids.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        for i in range(n_clusters):
            clusters[str(i) + ':keywords'] = list()
            for ind in order_centroids[i, :10]:
                clusters[str(i) + ':keywords'].append(terms[ind])
        return clusters

    def start_clustering(self):
        # clustering only top 100 queries
        queries = self._parse_queries()[:100]
        all_clusters = dict()
        for query in queries:
            search_results = self._get_search_results_for_query(query)
            all_clusters[query] = self._cluster(list(set(search_results)))

        with open('data/clusters.json', 'w') as fp:
            json.dump(all_clusters, fp)
        index_clusters()
        return {'status': 'Done clustering items'}


class LoadClusters(object):
    """ Parse clusters.json file and retrieve term clusters
    """

    def __init__(self):
        with open('data/clusters.json') as data_file:
            self.clusters = json.load(data_file)

    def get_queries(self):
        return {'queries': list(self.clusters.keys())}

    def get_clusters(self, query):
        clusters = self.clusters.get(query, None)
        results = {'name': query, 'children': list()}
        for cluster in clusters:
            if cluster.endswith('keywords') or cluster == 'score':
                continue
            for c in clusters:
                if cluster + ':keywords' == c:
                    keywords = clusters[c]
            results['children'].append({
                'name': cluster,
                'children': [{'name': key} for key in clusters[cluster]],
                'keywords': keywords
            })
        results['queries'] = self.get_queries()['queries']
        return results


def index_clusters():
    """ Index clusters in elasticsearch
    """
    es = get_es()
    es.indices.put_mapping(
        index=__index_name__, doc_type=__c_doc_type__, body={
            __c_doc_type__: {
                'properties': {
                    'keywords': {
                        "type": "string",
                        "position_increment_gap": 100
                    },
                    'items': {
                        "type": "string",
                        "position_increment_gap": 100
                    }
                }
            }
        })
    clusters = LoadClusters()
    for query in clusters.get_queries()['queries']:
        results = clusters.get_clusters(query)['children']
        for result in results:
            listings = list()
            for child in result['children']:
                listings.append(child['name'])
            doc = {
                'name': '{query}-{cluster}'.format(
                    query=query, cluster=result['name']),
                'keywords': result['keywords'],
                'items': listings
            }
            es.index(index=__index_name__, doc_type=__c_doc_type__, body=doc)
