import folium
import streamlit as st
import numpy as np
import pandas as pd
from streamlit_folium import st_folium
from functions.map import find_circle

MAP_HEIGHT = 500
MAP_WIDTH = 1200
st.set_page_config(layout="wide")

# Title
st.markdown("# Topology Viewer")


locations = [[-37.963679, 144.707179], [-37.963836, 144.707689]]


if "last_object_clicked" not in st.session_state:
        st.session_state["last_object_clicked"] = None

if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = 1

if "zoom" not in st.session_state:
    st.session_state["zoom"] = 17

if "center" not in st.session_state:
    st.session_state["center"] = [-37.963170, 144.706499]

# Map
m = folium.Map(location=[-37.963170, 144.706499], zoom_start=17, width=MAP_WIDTH, height=MAP_HEIGHT)




zoom = st.session_state["zoom"]

# Map circles
fg = folium.FeatureGroup(name="Houses")
if zoom > 15: # Show all full networks within the bounding box
    
    for i in range(len(locations)):
        fg.add_child(folium.Circle(
            location=locations[i],
            radius=3,
            fill=True,
            fill_opacity=1,
            opacity=1,
            fillColor= "red",
            color= "black",
            weight= 2,
            stroke= True if st.session_state["selected_node"] == i
                        else False

        ))
else: # Show only transformers
    pass


map_data = st_folium(m, 
                     feature_group_to_add=fg, 
                     center=st.session_state["center"],
                     zoom=st.session_state["zoom"],
                     width=MAP_WIDTH, 
                     height=MAP_HEIGHT)


c1, c2 = st.columns(2)
with c1:
    # Title
    "# Customer " + str(st.session_state["selected_node"])

    # Metrics
    metric_container = st.container()
    with metric_container:
        metric_1, metric_2, metric_3 = st.columns(3)           
        with metric_1:
            st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
        with metric_2:
            st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
        with metric_3:
            st.metric(label="Temperature", value="70 °F", delta="1.2 °F")


    # Statistics
    c = st.container(border=True)
    with c:
        c2_1, c2_2 = st.columns(2)
        
        with c2_1:
            "###### Minimum Voltage: "
            "###### Maximum Voltage: "
            "###### Mean Voltage: "
            
        with c2_2:
            "###### Standard Deviation: "
            "###### Low Voltage Instances (<225): "
            "###### High Voltage Instances (<235): "
    

with c2:
    st.bar_chart(np.random.randn(50, 3))
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(chart_data)

# Reload if zoom changes
if map_data["zoom"] != st.session_state["zoom"]:
    st.session_state["zoom"] = map_data["zoom"]
    st.rerun()


st.write(map_data)
if (map_data["last_object_clicked"]
        and map_data["last_object_clicked"] != st.session_state["last_object_clicked"]):
    
    st.session_state["last_object_clicked"] = map_data["last_object_clicked"]

    circle_no = find_circle(*map_data["last_object_clicked"].values(), locations=locations)
    st.session_state["selected_node"] = circle_no
    st.session_state["center"] = locations[circle_no]
    
    st.rerun()

