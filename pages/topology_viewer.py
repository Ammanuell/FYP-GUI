import folium
import streamlit as st
import numpy as np
import pandas as pd
from streamlit_folium import st_folium
from helpers.map import find_circle
from helpers.data import load_network_from_file

MAP_HEIGHT = 500
MAP_WIDTH = 1200
st.set_page_config(layout="wide")

# Title
st.markdown("# Topology Viewer")


node_locations, types, edges, impedances = load_network_from_file(8)


if "last_object_clicked" not in st.session_state:
        st.session_state["last_object_clicked"] = None

if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = 1

if "zoom" not in st.session_state:
    st.session_state["zoom"] = 17

if "center" not in st.session_state:
    st.session_state["center"] = node_locations[0]

# Map
m = folium.Map(location=node_locations[0], zoom_start=17, width=MAP_WIDTH, height=MAP_HEIGHT)



# Overlay Network on Map
fg = folium.FeatureGroup(name="Houses")
zoom = st.session_state["zoom"]
if zoom > 15: # Show all full networks within the bounding box
    # Nodes
    for i in range(len(node_locations)):

        if types[i] == 0:
            colour = "red"
            rad = 3
        elif types[i] == 1:
            colour = "black"
            rad = 2
        elif types[i] == 2:
            colour = "cyan"
            rad = 4
        elif types[i] == 3:
            colour = "lightgreen"
            rad = 3
        elif types[i] == 4:
            colour = "blue"
            rad = 3

        fg.add_child(folium.Circle(
            location=node_locations[i],
            radius=rad,
            fill=True,
            fill_opacity=1,
            opacity=1,
            fillColor= colour,
            color= "black",
            weight= 2,
            stroke= True if st.session_state["selected_node"] == i
                        else False,
            tooltip="Customer: {}".format(i)

        ))
    
    # Edges
    for i in range(len(edges)):
        edge = [int(edges[i, 0]), int(edges[i, 1])]
        imped = impedances[i]
        fg.add_child(folium.PolyLine(
            locations=[node_locations[edge[0]], node_locations[edge[1]]],
            color="#000000",
            weight=2,
            opacity= 1, 
            tooltip="Impedance: {} + {}j".format(np.round(imped[0],4), np.round(imped[1],4))

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
    st.empty()
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

# Rerun after user interaction
if map_data["zoom"] != st.session_state["zoom"]:
    st.session_state["zoom"] = map_data["zoom"]
    st.rerun()

if (map_data["last_object_clicked"]
        and map_data["last_object_clicked"] != st.session_state["last_object_clicked"]):
    
    st.session_state["last_object_clicked"] = map_data["last_object_clicked"]

    circle_no = find_circle(*map_data["last_object_clicked"].values(), locations=node_locations)
    st.session_state["selected_node"] = circle_no
    st.session_state["center"] = node_locations[circle_no]
    
    st.rerun()

