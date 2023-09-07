# Travel Order Resolved
<em>Natural Language Processing<em>
A program that processes voice and text commands to issue an appropriate itinerary.

Input will be obtained by using a speech-to-text model

We will first generate data and train the model to predict the departure and destination from the input converted from speech (speech-to-text). Based on the departure and destination locations, second prediction will be done to estimate all the possible trajectory and output the best train route itinerary.

The first prediction is done by a trained SVM model 
The second part of the solution concerns organising possible train routes and output the best route. 

## Speech-to-text module 
- Configure API key to use ASSEMBLY AI component in ``speech_to_text/api_configuration.py``
- Execute ``speech_to_text/main.py``

## Locations predictions 
- Data generation for three types of phrases by default

    To start generation, launch with ``python datagen.py``
    <br>
    *make sure the commune_2022.csv and stops.txt files are in the same directory*

    To modify phrases, change the string in the for loop. 
    Switching from cities to stops is also possible by following the instructions in the datagen.py file

- Load SVM model from ``svm_model.pkl``


## How to import data in neo4j in order to use the API :

1. Set up Neo4j
Download Neo4j desktop : https://neo4j.com/download/
Create a new project and add a new dbms
Click on the dbms and go on plugin tab to install Graph Data Science Library.


2. Load data in neo4j

Follow the instruction in station_in_area.ipynb then in sncf.ipynb.

You need to put all the csv in the import directory of your dbms. (on ubuntu "~/.config/'Neo4j Desktop'/Application/relate-data/dbmss/dbms-<dbmss id>/import")

3. Configure graph
This commands can be use in Neo4j desktop to create a graph and launch the astar algorithm on it. This is not necessary the API will do it.

```
CALL gds.graph.project(
    'travel',
    'Station',
    'TRAVEL_TO',
    {
        nodeProperties: ['latitude', 'longitude'],
        relationshipProperties: 'duration'
    }
)
```
4. A* Test request :
This is a command to run the astar algorithm just like the command above it is not necessary for the API.

```
MATCH (source:Station {name: 'Gare de Cherbourg'}), (target:Station {name: 'Gare de Dreux'})
CALL gds.shortestPath.astar.stream('travel', {
    sourceNode: source,
    targetNode: target,
    latitudeProperty: 'latitude',
    longitudeProperty: 'longitude',
    relationshipWeightProperty: 'duration'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN
    index,
    gds.util.asNode(sourceNode).name AS sourceNodeName,
    gds.util.asNode(targetNode).name AS targetNodeName,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
    costs,
    nodes(path) as path
ORDER BY index
```


### How to use the API :

In a terminal type : 
```
$ pip install virtualenv
$ virtualenv env
```
Then to activate the virtual environnement :

Windows :
```
$ env\Scripts\activate 
```
Linux :
```
$ source /bin/activate 
```

Then install django and django_neomodel:
```
$ pip install Django
$ pip install django_neomodel
```
Now to create the constrainct in neo4j (your dbms needs to be running): 
```
$ cd sncf/
$ python manage.py install_labels
$ python manage.py migrate
```
```
python3 -m spacy download fr_core_news_lg
```

Finally run the server :
```
$ python manage.py runserver
```
### Routes :

**bestPath/<str:start>/<str:dest> :** Returns the best path between two city or station. 

