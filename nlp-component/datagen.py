import csv
import random

# Get all the train stops in the txt file provided
with open('stops.txt', encoding='UTF-8') as file_stops:
    data_stops = csv.reader(file_stops, delimiter=',')
    next(data_stops)
    list_stops=[]
    for row in data_stops:
        list_stops.append(row[1])

# Get all the cities of France 
with open('commune_2022.csv', encoding='ISO-8859-1') as file_cities : 
    data_cities = csv.reader(file_cities, delimiter=',')
    next(data_cities)
    
    list_cities=[]
    for row in data_cities:
        list_cities.append(row[6])

# Define the structure of the data

# 1. Open a new CSV file
# with open('data.csv', 'w', encoding='UTF-8', newline='') as file:
    
#     # 2. Create a CSV writers
#     writer = csv.writer(file)

#     # 3. Write data to the file
#     # Generate itinerary phrases with random cities (just change 'list_cities' to 'list_stops' for itinerary with station names)
#     for x in range(0, 500):
#         sentence = 'Je veux aller de {} à {}'.format(list_cities[random.randint(0, len(list_cities)-1)], list_cities[random.randint(0, len(list_cities)-1)+1])
#         trajet = 1
#         row = [sentence]
#         writer.writerow(row)
#         sentence = 'Trajet de {} à {}'.format(list_cities[random.randint(0, len(list_cities)-1)], list_cities[random.randint(0, len(list_cities)-1)+1])
#         row = [sentence]
#         writer.writerow(row)
#         sentence = 'Aller-retour de {} à {}'.format(list_cities[random.randint(0, len(list_cities)-1)], list_cities[random.randint(0, len(list_cities)-1)+1])
#         row = [sentence]
#         writer.writerow(row)
#         sentence = 'Je veux aller de {} à {}'.format(list_stops[random.randint(0,len(list_stops)-1)], list_stops[random.randint(0, len(list_stops)-1)+1])
#         row = [sentence]
#         writer.writerow(row)
#         sentence = 'Trajet de {} à {}'.format(list_stops[random.randint(0,len(list_stops)-1)], list_stops[random.randint(0, len(list_stops)-1)+1])
#         row = [sentence]
#         writer.writerow(row)
#         sentence = 'Aller-retour de {} à {}'.format(list_stops[random.randint(0,len(list_stops)-1)], list_stops[random.randint(0, len(list_stops)-1)+1])
#         row = [sentence]
#         writer.writerow(row)
        
with open('random_itinerary.csv', 'w', encoding='UTF-8', newline='') as file:
    
    # 2. Create a CSV writers
    writer = csv.writer(file)

    # 3. Write data to the file
    # Generate itinerary phrases with random cities (just change 'list_cities' to 'list_stops' for itinerary with station names)
    for x in range(0, 700):
        sentence = 'Je veux aller de depart à destination'
        row = [sentence]
        writer.writerow(row)
        sentence = 'Trajet de depart à destination'
        row = [sentence]
        writer.writerow(row)
        sentence = 'Aller-retour de depart à destination'
        row = [sentence]
        writer.writerow(row)


        




