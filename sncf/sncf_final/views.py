from django.http import JsonResponse
from sncf_final.models import Station,Communes
from django.views.decorators.csrf import csrf_exempt
from sncf_final.graph import astar,getAvailableTrips
from sncf_final.nlp import nlp_predict
from sncf_final.speech_to_text import audio_file_handler
import neomodel
from neomodel import db
import json

# Create your views here.
def getAllStations(request):
    if request.method == 'GET':
        #try:
            stations = Station.nodes.all()
            stationList=[]
            cities=[city[0]for city in db.cypher_query("match(n:Station)-[]-(c:Communes) return distinct(c.name)")[0]]
            for station in stations :
                stationList.append(station.name)

            response={"stations":stationList,"cities":cities} 
            return JsonResponse(response, safe=False)
        # except:
        #     response = {"error": "Neo4J error"}
        #     return JsonResponse(response, safe=False)



#Get best route between two set of stations
def stationsToStations(stationsS,stationsD):
    response=[]
    for s in stationsS:
        for d in stationsD:
            result=astar(s.name,d.name,"travel")
            path=[{"name": result["nodeNames"][i], "lat":result["nodelats"][i], "lon":result["nodelons"][i]}for i in range(len(result["nodeNames"]))]
            response.append({"path":path, "duration":result["totalCost"]})
    
    response.sort(key=lambda x: x["duration"])
    return response

#Get stations with a station name or a city name
def getStationsByName(name):
    stations=[]
    try:
        print("try")
        stations.append(Station.nodes.get(name=name))
    except neomodel.core.DoesNotExist:
        try:
            city=Communes.nodes.get(name=name)
            print("excedpt")
            for s in city.stations:
                stations.append(s)
        except Exception as e:
            print("cocudfhd")
    return stations

@csrf_exempt
def test(request):
    if request.method == 'POST':
        try:
            body=json.loads(request.body)
            
            stationsS=getStationsByName(body['start'])
            stationsD=getStationsByName(body['end'])
            response={
                "paths":stationsToStations(stationsS,stationsD),
                "start":body['start'],
                "dest":body['end']
            }
            return JsonResponse(response, safe=False)
        except Exception as e:
            response = {"error": str(e)}
        return JsonResponse(response, safe=False)


@csrf_exempt
def anyToAny(request):
    if request.method == 'POST':
        try:
            text = audio_file_handler(request.FILES.get('data'))
            prediction = nlp_predict(text)
            print("OK")

            depart=str(prediction[1])[0].upper()+str(prediction[1])[1:]
            destination=str(prediction[2])[0].upper()+str(prediction[2])[1:]
            print('PREDICTION: ', prediction[0])
            print('PREDICTION: ', depart)
            print('PREDICTION: ', destination)
            stationsS=getStationsByName(depart)
            stationsD=getStationsByName(destination)
            response={
                "paths":stationsToStations(stationsS,stationsD),
                "start":depart,
                "dest":destination
            }
            return JsonResponse(response, safe=False)
        except Exception as e:
            response = {"error": str(e)}
        return JsonResponse(response, safe=False)

