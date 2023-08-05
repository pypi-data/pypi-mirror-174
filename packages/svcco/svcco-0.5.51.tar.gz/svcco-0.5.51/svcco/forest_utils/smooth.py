# smooth connections between trees in a network
from geomdl import BSpline
from geomdl import utilities
from geomdl.visualization import VisMPL
import numpy as np
from copy import deepcopy
from .optimize_connection_v2 import *
from tqdm import trange

def get_initial_vectors(forest,network,assignment,tree,edge):
    # Terminal Vessel Vector
    P1 = forest.networks[network][tree].data[assignment[edge],0:3]
    P2 = forest.networks[network][tree].data[assignment[edge],3:6]
    V1 = P2 - P1
    V1 = V1/np.linalg.norm(V1)

    # Connection Vessel Vector
    P3 = forest.networks[network][tree].data[assignment[edge],3:6]
    P4 = forest.connections[network][0][edge]
    V2 = P4 - P3
    V2 = V2/np.linalg.norm(V2)
    return V1,V2,P4


def link(forest):
    all_connections = []
    for network in range(forest.number_of_networks):
        network_connections = []
        all_network_vessels = np.zeros((1,7))
        for tree in range(forest.trees_per_network[network]):
            tree_tmp_vessels = np.zeros((forest.networks[network][tree].data.shape[0],7))
            tree_tmp_vessels[:,0:6] = forest.networks[network][tree].data[:,0:6]
            tree_tmp_vessels[:,6]   = forest.networks[network][tree].data[:,21]
            all_network_vessels = np.vstack((all_network_vessels,tree_tmp_vessels))
        all_network_vessels = all_network_vessels[1:,:]
        all_network_mid_points = (all_network_vessels[0:3]+all_network_vessels[3:6])/2
        for tree in range(forest.trees_per_network[network]):
            assignment = forest.assignments[network][tree]
            tree_connections = []
            for edge in trange(len(assignment)):
                R        = forest.networks[network][tree].data[assignment[edge],21]
                P1       = forest.networks[network][tree].data[assignment[edge],0:3]
                P2       = forest.networks[network][tree].data[assignment[edge],3:6]
                ignore   = set(np.argwhere(np.all(all_network_mid_points[3:6]==P2)).flatten().tolist())

                P4       = forest.connections[network][0][edge]
                V        = P4 - P2/np.linalg.norm(P4-P2)
                P3       = P4 + V*0.25
                dist_to_mid = np.linalg.norm(P4-P2)
                dists       = np.linalg.norm(all_network)
                collision_vessels_idx = set(np.argwhere(dists<dist_to_mid).flatten().tolist())
                if len(collision_vessels_idx) == 0:
                    collision_vessels = None
                else:
                    collision_vessels_idx = np.array(list(collision_vessels_idx - ignore))
                    collision_vessels = all_network_vessels[collision_vessels_idx,:]
                link_pts = get_optimum_link_points(P1,P2,P3,P4,R,collision_vessels)
                link_pts = link_pts[1:-1,:]
                tree_connections.append(link_pts)
            network_connections.append(tree_connections)
        all_connections.append(network_connections)
    return all_connections

def smooth_original(forest,curve_sample_size_min=5,curve_sample_size_max=21,curve_degree=3):
    #FOREST_CONNECT_COPY = deepcopy(forest)
    connections = []
    for network in range(forest.number_of_networks):
        if not np.any(forest.connections[network][0] is None):
            network_connections = []
            for tree in range(forest.trees_per_network[network]):
                tree_assignment = forest.assignments[network][tree]
                idx = max(forest.networks[network][tree].data[:,-1]) + 1
                #tree_connection_edges = np.zeros((len(forest.connections[network][0])*(curve_sample_size-1),forest.networks[network][tree].data.shape[1]))
                tree_connection_edges = []
                for edge in range(len(forest.connections[network][0])):
                    #print('Tree {}: Edge: {}'.format(tree,edge))
                    success = False
                    samples = curve_sample_size_min
                    # Check the angle formed
                    vec_1 = forest.networks[network][tree].data[tree_assignment[edge],0:3]-forest.networks[network][tree].data[tree_assignment[edge],3:6]
                    vec_2 = forest.connections[network][0][edge]-forest.networks[network][tree].data[tree_assignment[edge],3:6]
                    vec_1 = vec_1/np.linalg.norm(vec_1)
                    vec_2 = vec_2/np.linalg.norm(vec_2)
                    P0    = (forest.networks[network][tree].data[tree_assignment[edge],0:3]+forest.networks[network][tree].data[tree_assignment[edge],3:6])/2
                    P1    = forest.networks[network][tree].data[tree_assignment[edge],3:6]
                    ctr_0 = ((forest.networks[network][tree].data[tree_assignment[edge],0:3]*(3/4)+forest.networks[network][tree].data[tree_assignment[edge],3:6]*(1/4))).flatten().tolist()
                    ctr_1 = ((forest.networks[network][tree].data[tree_assignment[edge],0:3]+forest.networks[network][tree].data[tree_assignment[edge],3:6])/2).flatten().tolist()
                    if (np.arccos(np.dot(vec_1,vec_2))/np.pi)*180 > 120:
                        ctr_2 = forest.networks[network][tree].data[tree_assignment[edge],3:6].flatten().tolist()
                        ctr_3 = forest.connections[network][0][edge].tolist()
                    else:
                        A = 140
                        t = ((np.cos(np.pi*(A/180))-P0[0]*vec_2[0]-P0[1]*vec_2[1]-P0[2]*vec_2[2]+P1[0]*vec_2[0]+P1[1]*vec_2[1]+P1[2]*vec_2[2])/(vec_2[0]**2+vec_2[1]**2+vec_2[2]**2))
                        t = min(t,0.3)
                        conn_len = np.linalg.norm(forest.connections[network][0][edge]-forest.networks[network][tree].data[tree_assignment[edge],3:6])/2
                    #    vec_12_average = (vec_1+vec_2)/2
                        adj_0 = (P1-t*(conn_len)*vec_2)
                        if conn_len < forest.networks[network][tree].data[tree_assignment[edge],21]:
                            print("WARNING: Sharp Corner, lofting may fail")
                    #    vec_adj = adj_0 - P0/np.linalg.norm(adj_0 - P0)
                    #    vec_diff = vec_adj - vec_12_average
                    #    vec_diff = np.argwhere(vec_diff != 0).flatten()
                    #    vec_idx  = vec_diff[:2]
                    #    #AA = np.array([[vec_adj[vec_idx[0]],vec_12_average[vec_idx[0]]],
                    #    #               [vec_adj[vec_idx[1]],vec_12_average[vec_idx[1]]]])
                    #    #BB = np.array([[P0[vec_idx[0]]-P1[vec_idx[0]]],
                    #    #               [P0[vec_idx[1]]-P1[vec_idx[1]]]])
                    #    #AA_inv = np.linalg.inv(AA)
                    #    #sol = BB @ AA
                    #    sol  = (P0-P1)/(vec_adj - vec_12_average)
                    #    tt = sol[0]
                        ctr_2 = ((P0 + adj_0)/2).flatten().tolist()
                        ctr_3 = forest.connections[network][0][edge].tolist()
                    curve = BSpline.Curve()
                    curve.degree = curve_degree
                    #if (np.arccos(np.dot(vec_1,vec_2))/np.pi)*180 > 90:
                    curve.ctrlpts = [ctr_1,ctr_2,ctr_3]
                    #else:
                    #curve.ctrlpts = [ctr_0,ctr_1,ctr_2,ctr_3]
                    curve.knotvector = utilities.generate_knot_vector(curve.degree,len(curve.ctrlpts))
                    while samples <= curve_sample_size_max and not success:
                        curve.sample_size = samples
                        curve.evaluate()
                        pts = curve.evalpts
                        d0  = forest.networks[network][tree].data[tree_assignment[edge],12:15]
                        for p in range(len(pts)-1):
                            p0 = np.array(pts[p])
                            p1 = np.array(pts[p+1])
                            l  = np.linalg.norm(p1-p0)
                            d1 = (p1-p0)/l
                            A  = (abs(np.arccos(np.dot(-d0,d1)))/np.pi)*180
                            if A < 90:
                                success = False
                                samples += 2
                                break
                            else:
                                success = True
                            d0 = d1
                    if samples > curve_sample_size_max:
                        samples -= 2
                    for i in range(samples-1):
                        tmp = np.zeros(forest.networks[network][tree].data.shape[1])
                        tmp[0:3] = np.array(pts[i])
                        tmp[3:6] = np.array(pts[i+1])
                        tmp[21]  = forest.networks[network][tree].data[tree_assignment[edge],21]
                        tmp[20]  = np.linalg.norm(np.array(pts[i+1])-np.array(pts[i]))
                        tmp[12:15] = (np.array(pts[i+1])-np.array(pts[i]))/tmp[20]
                        tmp[26] = forest.networks[network][tree].data[tree_assignment[edge],26]+i+1
                        tmp[22] = forest.networks[network][tree].data[tree_assignment[edge],22]
                        tmp[-1] = idx
                        tmp[15] = -1
                        tmp[16] = -1
                        idx += 1
                        if i == 0:
                            tmp[17] = forest.networks[network][tree].data[tree_assignment[edge],-1]
                        elif i > 0:
                            tree_connection_edges[-1][15] = tmp[-1]
                            tree_connection_edges[-1][16] = -1
                            tmp[17] = tree_connection_edges[-1][-1]
                        #else:
                        #    tree_connection_edges[-1][15] = -1
                        #    tree_connection_edges[-1][16] = -1
                        #    tmp[17] = tree_connection_edges[-1][-1]
                        tree_connection_edges.append(tmp.tolist())
                network_connections.append(np.array(tree_connection_edges))
            connections.append(network_connections)
        else:
            connections.append([None])
    return connections, None

def smooth(forest,curve_sample_size_min=5,curve_sample_size_max=21,curve_degree=3):
    #FOREST_CONNECT_COPY = deepcopy(forest)
    connections = []
    splines     = []
    for network in range(forest.number_of_networks):
        if not np.any(forest.connections[network][0] is None):
            network_connections = []
            network_splines     = []
            for tree in range(forest.trees_per_network[network]):
                tree_assignment = forest.assignments[network][tree]
                idx = max(forest.networks[network][tree].data[:,-1]) + 1
                #tree_connection_edges = np.zeros((len(forest.connections[network][0])*(curve_sample_size-1),forest.networks[network][tree].data.shape[1]))
                tree_connection_edges = []
                for edge in range(len(forest.connections[network][0])):
                    #print('Tree {}: Edge: {}'.format(tree,edge))
                    success = False
                    samples = curve_sample_size_min
                    # Check the angle formed
                    vec_1 = forest.networks[network][tree].data[tree_assignment[edge],0:3]-forest.networks[network][tree].data[tree_assignment[edge],3:6]
                    vec_2 = forest.connections[network][0][edge]-forest.networks[network][tree].data[tree_assignment[edge],3:6]
                    vec_1 = vec_1/np.linalg.norm(vec_1)
                    vec_2 = vec_2/np.linalg.norm(vec_2)
                    print((np.arccos(np.dot(vec_1,vec_2))/np.pi)*180)
                    P0    = (forest.networks[network][tree].data[tree_assignment[edge],0:3]+forest.networks[network][tree].data[tree_assignment[edge],3:6])/2
                    P1    = forest.networks[network][tree].data[tree_assignment[edge],3:6]
                    ctr_0 = ((forest.networks[network][tree].data[tree_assignment[edge],0:3]*(3/4)+forest.networks[network][tree].data[tree_assignment[edge],3:6]*(1/4))).flatten().tolist()
                    #ctr_1 = ((forest.networks[network][tree].data[tree_assignment[edge],0:3]+forest.networks[network][tree].data[tree_assignment[edge],3:6])/2).flatten().tolist()
                    ctr_1 = P0.flatten().tolist()
                    if False:
                        #if (np.arccos(np.dot(vec_1,vec_2))/np.pi)*180 > 0:
                        ctr_2 = forest.networks[network][tree].data[tree_assignment[edge],3:6].flatten().tolist()
                        ctr_3 = forest.connections[network][0][edge].tolist()
                    else:
                        A = 120
                        t = ((np.cos(np.pi*(A/180))-P0[0]*vec_2[0]-P0[1]*vec_2[1]-P0[2]*vec_2[2]+P1[0]*vec_2[0]+P1[1]*vec_2[1]+P1[2]*vec_2[2])/(vec_2[0]**2+vec_2[1]**2+vec_2[2]**2))
                        t = min(t,0.3)
                        conn_len = np.linalg.norm(forest.connections[network][0][edge]-forest.networks[network][tree].data[tree_assignment[edge],3:6])/2
                    #    vec_12_average = (vec_1+vec_2)/2
                        adj_0 = (P1-t*(conn_len)*vec_2)
                        if conn_len < forest.networks[network][tree].data[tree_assignment[edge],21]:
                            print("WARNING: Sharp Corner, lofting may fail")
                    #    vec_adj = adj_0 - P0/np.linalg.norm(adj_0 - P0)
                    #    vec_diff = vec_adj - vec_12_average
                    #    vec_diff = np.argwhere(vec_diff != 0).flatten()
                    #    vec_idx  = vec_diff[:2]
                    #    #AA = np.array([[vec_adj[vec_idx[0]],vec_12_average[vec_idx[0]]],
                    #    #               [vec_adj[vec_idx[1]],vec_12_average[vec_idx[1]]]])
                    #    #BB = np.array([[P0[vec_idx[0]]-P1[vec_idx[0]]],
                    #    #               [P0[vec_idx[1]]-P1[vec_idx[1]]]])
                    #    #AA_inv = np.linalg.inv(AA)
                    #    #sol = BB @ AA
                    #    sol  = (P0-P1)/(vec_adj - vec_12_average)
                    #    tt = sol[0]
                        ctr_2 = ((P0+P1)/2).flatten().tolist()
                        ctr_3 = ((P1+adj_0)/2).flatten().tolist()
                        ctr_4 = forest.connections[network][0][edge].tolist()
                    curve = BSpline.Curve()
                    curve.degree = curve_degree
                    #if (np.arccos(np.dot(vec_1,vec_2))/np.pi)*180 > 90:
                    curve.ctrlpts = [ctr_1,ctr_2,ctr_3,ctr_4]
                    #else:
                    #curve.ctrlpts = [ctr_0,ctr_1,ctr_2,ctr_3]
                    curve.knotvector = utilities.generate_knot_vector(curve.degree,len(curve.ctrlpts))
                    network_splines.append(deepcopy(curve))
                    while samples <= curve_sample_size_max and not success:
                        curve.sample_size = samples
                        curve.evaluate()
                        pts = curve.evalpts
                        d0  = forest.networks[network][tree].data[tree_assignment[edge],12:15]
                        for p in range(len(pts)-1):
                            p0 = np.array(pts[p])
                            p1 = np.array(pts[p+1])
                            l  = np.linalg.norm(p1-p0)
                            d1 = (p1-p0)/l
                            A  = (abs(np.arccos(np.dot(-d0,d1)))/np.pi)*180
                            if A < 90:
                                success = False
                                samples += 2
                                break
                            else:
                                success = True
                            d0 = d1
                    if samples > curve_sample_size_max:
                        samples -= 2
                    for i in range(samples-1):
                        tmp = np.zeros(forest.networks[network][tree].data.shape[1])
                        tmp[0:3] = np.array(pts[i])
                        tmp[3:6] = np.array(pts[i+1])
                        tmp[21]  = forest.networks[network][tree].data[tree_assignment[edge],21]
                        tmp[20]  = np.linalg.norm(np.array(pts[i+1])-np.array(pts[i]))
                        tmp[12:15] = (np.array(pts[i+1])-np.array(pts[i]))/tmp[20]
                        tmp[26] = forest.networks[network][tree].data[tree_assignment[edge],26]+i+1
                        tmp[22] = forest.networks[network][tree].data[tree_assignment[edge],22]
                        tmp[-1] = idx
                        tmp[15] = -1
                        tmp[16] = -1
                        idx += 1
                        if i == 0:
                            tmp[17] = forest.networks[network][tree].data[tree_assignment[edge],-1]
                        elif i > 0:
                            tree_connection_edges[-1][15] = tmp[-1]
                            tree_connection_edges[-1][16] = -1
                            tmp[17] = tree_connection_edges[-1][-1]
                        #else:
                        #    tree_connection_edges[-1][15] = -1
                        #    tree_connection_edges[-1][16] = -1
                        #    tmp[17] = tree_connection_edges[-1][-1]
                        tree_connection_edges.append(tmp.tolist())

                network_connections.append(np.array(tree_connection_edges))
            connections.append(network_connections)
            splines.append(network_splines)
        else:
            connections.append([None])
    return connections, None, splines


#def get_angle(V1,V2):
#    return np.arccos(np.dot(V1,V2))*(180/np.pi)

def smooth_new(forest,max_angle=45):
    connections = []
    for network in range(forest.number_of_networks):
        if not np.any(forest.connections[network][0] is None):
            network_connections = []
            for tree in range(forest.trees_per_network[network]):
                idx = max(forest.networks[network][tree].data[:,-1]) + 1
                tree_connection_edges = []
                for edge in range(len(forest.connections[network][0])):
                    edge_1   = forest.assignments[network][0][edge]
                    edge_2   = forest.assignemnts[network][1][edge]
                    match_vector = forest.networks[network][0].data[edge_1,3:6] - forest.networks[network][1].data[edge_2,3:6]
                    match_vector = match_vector/np.linalg.norm(match_vector)
                    vector_1 = forest.networks[network][0].data[edge_1,12:15]
                    vector_2 = forest.networks[network][1].data[edge_2,12:15]

    return connections, None
