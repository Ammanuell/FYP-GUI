import folium
import streamlit as st
import numpy as np
import pandas as pd
from streamlit_folium import st_folium
from helpers.map import find_circle, zoom_to_line_weight, in_bounding_box
from helpers.data import load_network_from_file, load_all_networks
from helpers.ui import remove_top_padding

MAP_HEIGHT = 650
MAP_WIDTH = 1200

NETWORK_ZOOM = 15

st.set_page_config(layout="wide")
remove_top_padding()


# Title
st.markdown("# Topology Viewer")

net_nodes, net_types, net_edges, net_edge_impedances = load_all_networks()

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

# if st.session_state["zoom"] > NETWORK_ZOOM: # Show all full networks within the bounding box
#     # Nodes
#     for i in range(len(node_locations)):

#         if types[i] == 0:
#             colour = "red"
#             rad = 3
#         elif types[i] == 1:
#             colour = "black"
#             rad = 2
#         elif types[i] == 2:
#             colour = "cyan"
#             rad = 4
#         elif types[i] == 3:
#             colour = "lightgreen"
#             rad = 3
#         elif types[i] == 4:
#             colour = "blue"
#             rad = 3

#         fg.add_child(folium.Circle(
#             location=node_locations[i],
#             radius=rad,
#             fill=True,
#             fill_opacity=1,
#             opacity=1,
#             fillColor= colour,
#             color= "black",
#             weight= 2,
#             stroke= True if st.session_state["selected_node"] == i
#                         else False,
#             tooltip="Customer: {}".format(i)

#         ))
    
#     # Edges
#     for i in range(len(edges)):
#         edge = [int(edges[i, 0]), int(edges[i, 1])]
#         imped = impedances[i]
#         fg.add_child(folium.PolyLine(
#             locations=[node_locations[edge[0]], node_locations[edge[1]]],
#             color="#000000",
#             weight=zoom_to_line_weight(st.session_state["zoom"]),
#             opacity= 1, 
#             tooltip="Impedance: {} + {}j".format(np.round(imped[0],4), np.round(imped[1],4))

#         ))
# else: # Show only transformers
#     fg.add_child(folium.Circle(
#             location=node_locations[0],
#             radius=200,
#             fill=True,
#             fill_opacity=0.5,
#             fillColor= "lightblue",
#             color= "cyan",
#             weight= 2,
#             stroke= True,
#             tooltip="Network {}".format(0)

#         ))

if st.session_state["zoom"] > NETWORK_ZOOM: # Show all full networks within the bounding box
    # Nodes
    for i in range(len(net_nodes)):
        for j in range(len(net_nodes[i])):

            if net_types[i][j] == 0:
                colour = "red"
                rad = 3
            elif net_types[i][j] == 1:
                colour = "black"
                rad = 2
            elif net_types[i][j] == 2:
                colour = "cyan"
                rad = 4
            elif net_types[i][j] == 3:
                colour = "lightgreen"
                rad = 3
            elif net_types[i][j] == 4:
                colour = "blue"
                rad = 3

            fg.add_child(folium.Circle(
                location=net_nodes[i][j],
                radius=rad,
                fill=True,
                fill_opacity=1,
                opacity=1,
                fillColor= colour,
                color= "black",
                weight= 2,
                stroke= True if st.session_state["selected_node"] == j
                            else False,
                tooltip="Customer: {}".format(j)

            ))
        
        # Edges
        for i in range(len(net_edges)):
            for j in range(len(net_edges[i])):
                edge = [int(net_edges[i][j][0]), int(net_edges[i][j][1])]
                imped = net_edge_impedances[i][j]
                fg.add_child(folium.PolyLine(
                    locations=[net_nodes[i][edge[0]], net_nodes[i][edge[1]]],
                    color="#000000",
                    weight=zoom_to_line_weight(st.session_state["zoom"]),
                    opacity= 1, 
                    tooltip="Impedance: {} + {}j".format(np.round(imped[0],4), np.round(imped[1],4))

                ))
else: # Show only transformers
    for i in range(len(net_nodes)):
        fg.add_child(folium.Circle(
                location=net_nodes[i][0],
                radius=200,
                fill=True,
                fill_opacity=0.5,
                fillColor= "lightblue",
                color= "cyan",
                weight= 2,
                stroke= True,
                tooltip="Network {}".format(i)

            ))

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

# Rerun after user interaction
if map_data["zoom"] != st.session_state["zoom"]:
    st.session_state["zoom"] = map_data["zoom"]
    st.rerun()

if (map_data["last_object_clicked"]
        and map_data["last_object_clicked"] != st.session_state["last_object_clicked"]):
    if st.session_state["zoom"] > NETWORK_ZOOM:
        st.session_state["last_object_clicked"] = map_data["last_object_clicked"]

        circle_no = find_circle(*map_data["last_object_clicked"].values(), locations=node_locations)
        st.session_state["selected_node"] = circle_no
        st.session_state["center"] = node_locations[circle_no]
    else:
        pass


    st.rerun()

st.empty()

st.write(map_data)