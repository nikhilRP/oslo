## Recommendation engine for a marketplace


Taking a knock at the publication mentioned below:

#### Recommending Similar Items in Large-scale Online Marketplaces (https://pdfs.semanticscholar.org/e107/0c60d926e69298263e9ca36c698b69a21914.pdf)

What is the problem this publication is trying to solve?
* Recommendation engine for a large-scale marketplace
* Recommending similar products to consumer based on behavior (bid page redirect vs item landing from search page)

Key ideas:
* Personalization of recommendation based on the user search behavior
* Clustering of items
* Configurable ranking function (similarity and quality) based on the user behavior. Recommendations for user after a bid out come (higher weight for item similarity) vs landing on a item page based on the search (higher weight to quality compared to the previous scenario)

Comments on the mission:
* I really like the what this paper is aiming to solve but I am not sure if it is the solution for every situation.
* WHY? Selecting user queries and clustering the items is very dependent on the search engine metrics (maturity, quality and effectiveness). In other words every time there is a change to search engine results and personalization there will be a need to generate clusters based on the new search engine output. Might also result in the cold-start problem or forced to use recommendation engine that still uses results from old search engine. As I say that eBay's search engine might be very stable and there is very little room for drastic changes to the search engine itself. And on top of that it is the assumption that authors make in the publication and do not talk about search engine in detail.

Improvements I would be making:
* Cluster items based on Online K-means clustering and keep them updated using continuous ingestion rather than having an offline cluster generation mechanism. Eliminates the need for having bisecting K-means mentioned in the paper in the terms of parallelization and also cold-start problem for new items.
* Find a way to group users based on the search queries and behavior and boost the retrieved items using ranking function.
