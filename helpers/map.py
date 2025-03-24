def find_circle(lat, lon, locations):
    location = min(locations, key=lambda l: (l[0] - lat) ** 2 + (l[1] - lon) ** 2)
    for i in range(len(locations)):
         if locations[i][0] == location[0] and locations[i][1] == location[1]:
              closest_node = i
    return closest_node

def zoom_to_line_weight(zoom):

     weight = 25/zoom
     return weight