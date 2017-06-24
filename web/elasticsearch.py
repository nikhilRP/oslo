from elasticsearch import Elasticsearch


def get_es():
    return Elasticsearch(['192.168.99.100'], port=9200)
