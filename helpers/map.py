def find_circle(lat, lon, locations):
    location = min(locations, key=lambda l: (l[0] - lat) ** 2 + (l[1] - lon) ** 2)
    for i in range(len(locations)):
         if locations[i][0] == location[0] and locations[i][1] == location[1]:
              closest_node = i
    return closest_node

def zoom_to_line_weight(zoom):

     weight = 25/zoom
     return weight

def in_bounding_box(loc, bounding_box):
     lat = loc[0]
     lon = loc[1]

     bl_lat = bounding_box["_southWest"]["lat"]
     bl_lon = bounding_box["_southWest"]["lng"]
     tr_lat = bounding_box["_northEast"]["lat"]
     tr_lon = bounding_box["_northEast"]["lng"]

     return (lat >  bl_lat) and (lat < tr_lat) and (lon > bl_lon) and (lon < tr_lon)