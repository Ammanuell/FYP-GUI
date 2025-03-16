import folium
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# Title
st.markdown("# Topology Viewer")


def find_circle(lat, lon):
    location = min(locations, key=lambda l: (l[0] - lat) ** 2 + (l[1] - lon) ** 2)
    for i in range(len(locations)):
         if locations[i][0] == location[0] and locations[i][1] == location[1]:
              closest_node = i
    return closest_node
    


# Map
m = folium.Map(location=[-37.963170, 144.706499], zoom_start=17)


# Map circles
if "last_object_clicked" not in st.session_state:
        st.session_state["last_object_clicked"] = None

if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = 1


locations = [[-37.963679, 144.707179], [-37.963836, 144.707689]]

fg = folium.FeatureGroup(name="State bounds")

for i in range(len(locations)):
    fg.add_child(folium.Circle(
        location=locations[i],
        radius=3,
        fill=True,
        fill_opacity=1,
        opacity=1,
        color= "blue" if st.session_state["selected_node"] == i
                    else "red"
    ))


c1, c2 = st.columns(2)
with c1:
    map_data = st_folium(m, feature_group_to_add=fg, width=700, height=500)

with c2:
    st.write(map_data)

if (map_data["last_object_clicked"]
        and map_data["last_object_clicked"] != st.session_state["last_object_clicked"]):
    
    st.session_state["last_object_clicked"] = map_data["last_object_clicked"]

    circle_no = find_circle(*map_data["last_object_clicked"].values())
    st.session_state["selected_node"] = circle_no

    st.rerun()

