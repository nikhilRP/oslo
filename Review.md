### Recommending Similar Items in Large-scale Online Marketplaces

[Link for the publication](https://pdfs.semanticscholar.org/e107/0c60d926e69298263e9ca36c698b69a21914.pdf)

**What is the problem this publication is trying to solve?**
* Recommendation engine for a large-scale marketplace
* Recommending similar products to consumer based on behavior (bid page redirect vs item landing from search page)

**Key ideas:**
* Personalization of recommendations by using weighting of similarity of the item and quality
* Offline clustering of items
* Including user behavior by using top search queries to cluster the items (to get a view on how users group items)
* Configurable ranking function (similarity and quality) based on the user behavior. Recommendations for user after a bid out come (higher weight for item similarity) vs landing on a item page based on the search (higher weight to quality compared to the previous scenario)

**Improvements I would be making:**
* Cluster items based on Online clustering (preferably hierarchical) and keep them updated using continuous ingestion rather than having an offline cluster generation mechanism. Eliminates the need for having bisecting K-means mentioned in the paper in the terms of parallelization and also cold-start problem for new items.
    - One time  batch processing and then streaming updates (insertion or deletion) of new elements
* Would dynamically optimize clustering algorithm using silhouette, homogeneity and completeness scores. (selction of K wasn't mentioned in paper at all)
* Decouple search and clustering. (really depends on the maturity of search engine and specific use case)
    - WHY? Selecting user queries and clustering the items is very dependent on the search engine metrics (maturity, quality and effectiveness). In other words every time there is a change to search engine results and personalization there will be a need to generate clusters based on the new search engine output. Might also result in the cold-start problem or forced to use recommendation engine that still uses results from old search engine. As I say that eBay's search engine might be very stable and there is very little room for drastic changes to the search engine itself. And on top of that it is the assumption that authors make in the publication and do not talk about search engine in detail.
* Would be great to include a specific user behavior as part of ranking function (weight or boost items specific to user based on search logs) apart from similarity and quality.
