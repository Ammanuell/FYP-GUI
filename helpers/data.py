import pandas as pd
import numpy as np
from pathlib import Path


parent_dir = Path(__file__).resolve().parent.parent

DATA_PATH =  parent_dir / "data" / "Example_Data" / "Output"


def load_network_from_file(net_no):

    file_path = DATA_PATH / str(net_no)

    # Nodes
    df = pd.read_csv(file_path / (str(net_no) + "_3p_Output_Nodes.csv")).to_numpy()
    
    phase_1 =pd.read_csv(file_path / (str(net_no) + "_1_Output_Nodes.csv")).to_numpy()
    type_1 = phase_1[:, 7]
    

    phase_2 =pd.read_csv(file_path / (str(net_no) + "_2_Output_Nodes.csv")).to_numpy()
    type_2 = phase_2[1:, 7]
    type_2[type_2 == 0] = 3

    phase_3 =pd.read_csv(file_path / (str(net_no) + "_3_Output_Nodes.csv")).to_numpy()
    type_3 = phase_3[1:, 7]
    type_3[type_3 == 0] = 4

    types = np.hstack((type_1,type_2,type_3))
    locations = df[:, [2,1]]

    # Edges
    df = pd.read_csv(file_path / (str(net_no) + "_3p_Output_Edges.csv")).to_numpy()
    edges = df[:,[0,1]]
    impedances = df[:,[2,3]]
    return locations, types, edges, impedances

