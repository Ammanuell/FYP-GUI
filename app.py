import streamlit as st



# Define the pages

dashboard = st.Page(
    page= "views/dashboard.py",
    title= "Dashboard",
    icon= ":material/home:",
    default= True
)

topology_viewer = st.Page(
    page= "views/topology_viewer.py",
    title= "Topology Viewer",
    icon= ":material/map:" 
)

topology_estimator = st.Page(
    page= "views/topology_estimator.py",
    title= "Topology Estimator",
    icon= ":material/hub:" 
)

customer_voltages = st.Page(
    page= "views/customer_voltages.py",
    title= "Customer Voltages",
    icon= ":material/electric_bolt:" 
)

# Navigation
pg = st.navigation(
    {
        "Home": [dashboard],
        "Widgets": [topology_viewer, topology_estimator, customer_voltages]
    }
    )

# Shared
st.logo(
    image= "assets/logo.png",
    size= "large")
# Run
pg.run()
