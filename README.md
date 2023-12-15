### Running

Used the first docker image version. Though my Mac is an apple chip, creating a container by: 

`docker run --platform linux/amd64 -ti karmaresearch/wdps2`

### To be discussed:

1. Entity recognition

   The requirement on Canvas: "You can use libraries that do the entity **recognition** but not the **disambiguation.**" 

   Using spacy is feasible but so far we haven't reached disambiguation.

2. Extract answer

   Done, need to upload the code and adjust the details

3. Fact-checking

   If dont use Google we need to check facts in certain databases. 

   

   In Wikidata:

   `*from* SPARQLWrapper *import* SPARQLWrapper, JSON`

   `sparql = SPARQLWrapper("https://query.wikidata.org/sparql")`

   `*# this query checks Amsterdam(Q727) is in which country(P17)*`

   `*# the result shows "Netherlands"*`

   `sparql.setQuery("""`

   `SELECT ?countryLabel WHERE {`

     `wd:Q727 wdt:P17 ?country .`

     `SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }`

   `}`

   `""")`

   `sparql.setReturnFormat(JSON)`

   `results = sparql.query().convert()`

   `*for* result *in* results["results"]["bindings"]:`

   ​    `print(result["countryLabel"]["value"])`

   This could be run in Python after installing SPARQLWrapper. If we want to use this, we also need to **extract the relation** to construct a query. 

   

   Each entity in Wikidata has a unique identifier, called Q number. And each attribute of the data also has a P number. Knowing the **Q number and P number** of the entities and attributes is a must to build a query.

   

​	