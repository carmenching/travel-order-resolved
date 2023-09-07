from neomodel import db
import datetime
def createGraph(name):
    if [name] not in db.cypher_query(
            '''
            CALL gds.graph.list()
            YIELD graphName
            RETURN graphName
            ORDER BY graphName ASC
            '''
            )[0]:
        
        db.cypher_query(
            '''
            CALL gds.graph.project(
                \''''+name+'''\',
                'Station',
                'TRIP_TO',
                {
                    nodeProperties: ['lat', 'lon'],
                    relationshipProperties: 'duration'
                }
            )
            '''
            )

#Not used for now
def getAvailableTrips(date):
    day=datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8])).strftime("%A").lower()
    print(day)
    response=db.cypher_query('Match(d:Day {name: "'+day+'"})-[]-(s:Service)-[]-(t:Trip) where s.start_date<"'+date+'"<s.end_date and not "'+date+'" in s.unavailability return t.id')
    return [i[0] for i in response[0]]


def astar(start,dest,graphName):
    createGraph(graphName)
    response=db.cypher_query(
            '''MATCH (source:Station {name: "'''+start+'''"}), (target:Station {name: "'''+dest+'''"})
            
            CALL gds.shortestPath.astar.stream(\''''+graphName+'''\', {
                sourceNode: source,
                targetNode: target,
                latitudeProperty: 'lat',
                longitudeProperty: 'lon',
                relationshipWeightProperty: 'duration'
            })
            YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
            RETURN
                index,
                gds.util.asNode(sourceNode).name AS sourceNodeName,
                gds.util.asNode(targetNode).name AS targetNodeName,
                totalCost,
                [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
                [nodeId IN nodeIds | gds.util.asNode(nodeId).lat] AS nodelats,
                [nodeId IN nodeIds | gds.util.asNode(nodeId).lon] AS nodelons,
                costs,
                nodes(path) as path
            ORDER BY index
            '''
            )
    result={}
    for i in range(len(response[1])):
        result[response[1][i]]=response[0][0][i]
    return result