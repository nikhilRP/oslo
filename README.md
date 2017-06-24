## OSLO

[![Build Status](https://travis-ci.org/nikhilRP/recommendation_engine.svg?branch=master)](https://travis-ci.org/nikhilRP/recommendation_engine)

What is OSLO?
* POC implementation of a recommendation engine for a large-scale marketplace. Named after the coffeeshop where it was built, they do have great coffee :)
* Based tentatively on the paper - Recommending Similar Items in Large-scale Online Marketplaces
* My view on the publication - [click here](https://github.com/nikhilRP/recommendation_engine/blob/master/Review.md)

#### NOTE: It is just a POC and is hacked over the weekend most likely with excess coffee and beer intake. So please do not use it for any serious purposes.

### Implementation

**What is been implemented in this code repo?**

1. Create search engine for items available. This is done using elasticsearch and indexing all listing titles in it.
2. Use top queries provided and get the results.
    * Construct query (might be multiple words) including fuzziness and then get the desired results for top 100 search terms
3. Cluster the results using K-Means clustering
    * Removed duplicate results
    * Vectorize the results using TF-IDF
    * Reduce dimensions using SVD
    * Select K (number of clusters) by maximizing silhouette score
    * Index listings and keywords for a given clusters
4. Use seed item to construct the query and query the top 5 clusters
5. Use ranking function (simple boosting in elasticsearch) to order the recommendations
6. Display top 10 recommendations

##### NOTE: Since no quality metrics are provided work is still not completed

### Requirements

    docker
    docker-compose

### Tests

  Running tests without docker

    py.test web/

  Running tests in the docker container

    docker-compose build && docker-compose run --rm web py.test

### Run the web app

    docker-compose stop && docker-compose up --force-recreate --build


### Endpoints

1. Index page - http://{docker-ip}/
    - Should have details about search terms used to generate clusters and associated clusters.
2.  Elasticsearch index creation -  http://{docker-ip}/cluster-data?index=true
    - Triggers indexing of all the listings and then does clustering
    - NOTE: Takes a while to finish (20 to 25 mins)
    - Not using flag "index=true" uses existing index to cluster the search term results http://{docker-ip}/cluster-data
3. Search page - http://{docker-ip}/search?seed={item}
    - Use seed item to get top n recommendations

### Improvements

1. Write tests
2. Make infrastructure scalable
3. Use online clustering preferably Online agglomerative clustering to update the clusters on the fly (would be really useful for short lived items and avoids cold-start problem)
4. Make clustering independent of search personalization
5. Remove duplicate clusters
6. Fine tune ranking function
