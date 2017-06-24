## OSLO

[![Build Status](https://travis-ci.org/nikhilRP/recommendation_engine.svg?branch=master)](https://travis-ci.org/nikhilRP/recommendation_engine)

What is OSLO?
* POC implementation of a recommendation engine for a large-scale marketplace. Named after the coffeeshop where it was built, they do have great coffee :)
* Based tentatively on the paper - Recommending Similar Items in Large-scale Online Marketplaces
* My view on the publication - [click here](https://github.com/nikhilRP/recommendation_engine/blob/master/Review.md)

#### NOTE: It is just a POC and is hacked over the weekend most likely with excess coffee and beer intake. So please do not use it for any serious purposes.

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
