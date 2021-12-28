import networkx as nx
import numpy as np
from scipy import sparse
import time
import pandas as pd
from tqdm import tqdm


def motif_parallel(adj,node_list):
    '''
    模体识别，已获得数据
    :param adj: lil_matrix
    快速按行切片，高效查找
    每个进程获得需要开始查找的node_list
    :return:
    '''
    '''for i in node_list:
        tmp = motif_find3(adj,i)'''
    time1 = time.time()
    for i in node_list:
        tmp = motif_find1(adj,i)
    time2 = time.time()
    print('time:',time2-time1)


def motif_find1(adj, node):
    '''
    从某个节点node开始出发，寻找模体1
    :param adj:
    :param node:
    :return:
    '''
    motif = []
    node2 = motif_part1(adj, node)
    node3 = []
    for i in node2:
        tmp = motif_part2(adj, i)
        node3.append(tmp)
    for i in range(len(node3)):
        for j in node3[i]:
            if adj[node, j] == 0 and adj[j, node] == 0:
                tmp = []
                tmp.append(node)
                tmp.append(node2[i])
                tmp.append(j)
                motif.append(tmp)
    print(motif)

def motif_find2(adj, node):
    '''
    从某个节点node开始出发，寻找模体2
    :param adj:
    :param node:
    :return:
    '''
    motif = []
    node2 = motif_part1(adj, node)
    node3 = motif_part2(adj, node)
    for i in node2:
        for j in node3:
            if adj[i, j] == 0 and adj[j, i] == 0:
                tmp = []
                tmp.append(node)
                tmp.append(i)
                tmp.append(j)
                motif.append(tmp)
    print(motif)

def motif_find3(adj, node):
    '''
    从某个节点node开始出发，寻找模体3
    :param adj:
    :param node:
    :return:
    '''
    motif = []
    node2 = motif_part1(adj, node)
    node3 = motif_part1(adj, node)
    for i in node2:
        for j in node3:
            if adj[i, j] == 0 and adj[j, i] == 0 and i != j:
                tmp = []
                tmp.append(node)
                tmp.append(i)
                tmp.append(j)
                motif.append(tmp)
    #去除对称情况
    sort_motif = [sorted(i) for i in motif]
    index = 0
    while len(sort_motif) != 0:
        tmp = sort_motif.pop(0)
        if tmp in sort_motif:
            motif.pop(index)
            continue
        index += 1
    #return len(motif)
    print(motif)

def motif_find4(adj, node):
    '''
    从某个节点node开始出发，寻找模体3
    :param adj:
    :param node:
    :return:
    '''
    motif = []
    node2 = motif_part2(adj, node)
    node3 = motif_part2(adj, node)
    for i in node2:
        for j in node3:
            if adj[i, j] == 0 and adj[j, i] == 0 and i != j:
                tmp = []
                tmp.append(node)
                tmp.append(i)
                tmp.append(j)
                motif.append(tmp)
    #去除对称情况
    sort_motif = [sorted(i) for i in motif]
    index = 0
    while len(sort_motif) != 0:
        tmp = sort_motif.pop(0)
        if tmp in sort_motif:
            motif.pop(index)
            continue
        index += 1
    #return len(motif)
    print(motif)


def motif_part1(adj, node):
    '''
    连边种类1 A->B
    :param adj:
    :param node:
    :return:
    '''
    tmp_list = []
    nozero = list(adj.rows)
    for i in nozero[node]:
        if adj[i, node] == 0:
            # print('step1:({},{}) {}; ({},{}) {}'.format(node, i, adj[node, i], i, node, adj[i, node]))
            tmp_list.append(i)
    return tmp_list

def motif_part2(adj, node):
    '''
    连边种类2 A->B B->A
    :param adj:
    :param node:
    :return:
    '''
    tmp_list = []
    nozero = list(adj.rows)
    for i in nozero[node]:
        if adj[i, node] != 0:
            # print('step1:({},{}) {}; ({},{}) {}'.format(node, i, adj[node, i], i, node, adj[i, node]))
            tmp_list.append(i)
    return tmp_list


if __name__ == '__main__':
    #max_weight
    G1 = nx.read_weighted_edgelist('Wiki-Vote.txt',create_using=nx.DiGraph)
    G1 = nx.convert_node_labels_to_integers(G1)
    adj = nx.adjacency_matrix(G1)
    adj = sparse.lil_matrix(adj)
    node_list = nx.nodes(G1)
    motif_parallel(adj, node_list)





