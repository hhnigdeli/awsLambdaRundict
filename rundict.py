from bs4 import BeautifulSoup
from math import sin, cos, sqrt, atan2, radians


def kml_to_df( file ,tag="coordinates",seperator=","):
            """
            to  convert .kml file  to Pandas DataFrame        
            ---------------------------------------------------------------------------------------------
            example,   
            DataFrame = route.kml_to_df(file_name= "file.kml",tag="LineString",seperator=",")
            """
            #infile = open(str(file_name),"r")
            #contents = infile.read()
            soup = BeautifulSoup(file,'xml')
            titles = soup.find_all(str(tag))
            data=[title.get_text() for title in titles]
            #to split merged text values by " "
            liste_0 =[data[i].split() for i in range(len(data))]
            liste_0[0].pop(0)
            #to merge liste_0 data
            liste_0_ =[]
            for i in liste_0:
                for c in i:
                    liste_0_.append(c)
            #to split one column values three columns represent Lat Long and Alt 
            liste_1=[i.split(seperator) for i in liste_0_]
            #to pop if any data missing 
            popindex = []
            for i in range(len(liste_1)):
                if len(liste_1[i]) != 3:
                    popindex.append(i)        
            for i in popindex:
                liste_1.pop(i)        
            lat  =  [i[0] for i in liste_1 ]
            long =  [i[1] for i in liste_1 ]
            alt  =  [i[2] for i in liste_1 ]
            dataJSON = { "Lat":lat , "Long":long , "Alt":alt}
            
            return dataJSON

def add_distance(data,radius=6371):
     
        #to calculate distances between to gps points and aculated distances 
        distances = []
        for i in range(len(data["Lat"])):
            if i == 0:
                distances.append(0)
            else:
                lat1 = radians(float(data["Lat"][i]))
                lon1 = radians(float(data["Long"][i]))
                lat2 = radians(float(data["Lat"][i-1]))
                lon2 = radians(float(data["Long"][i-1]))
                dlon = lon1 - lon2
                dlat = lat1 - lat2
        #to calculate distace between two points on the earth
                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = radius * c
                distances.append(distance*1000)
        cdistances = []
        for i in range(len(distances)):
            if i == 0:
                cdistances.append(i)
            else:
                cdistances.append(sum(distances[:(i+1)]))
        


        dist = {"Dist":list(map(str,distances)),"Cdist":list(map(str,cdistances))}

        return dist       


