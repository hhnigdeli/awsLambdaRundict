from bs4 import BeautifulSoup


def kml_to_df( file ,tag="LineString",seperator=","):
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
            #to split one column values three columns represent Lat Long and Alt 
            liste_1=[i.split(seperator) for i in liste_0[0]]
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
