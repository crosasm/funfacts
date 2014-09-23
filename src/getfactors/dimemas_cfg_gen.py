#! /usr/bin/env python


#generates dimemas cfg
#imput arguments: trace bandwidth latency cpuratio inlinks outlinks

import sys
from os import environ

dim_trace = sys.argv[1]

num_tasks = 1
with open(dim_trace) as f:
    for line in f:
        words = line.split(':')
        if len(words) > 1:
            if words[0] == '#DIMEMAS':
                subwords = words[3].split("(")
                num_tasks =  subwords[0]
                break


num_nodes = int(num_tasks)
NET_BW = sys.argv[2]
LAT = sys.argv[3]
CPU_RATIO = sys.argv[4]
in_links = sys.argv[5]
out_links = sys.argv[6]

MAIN_DIR = environ['AUTOMATIC_ANALYSIS']
CFGS_DIR = MAIN_DIR + '/data/cfgs'

filetocat = CFGS_DIR+'/1ppn.head.cfg'
with open(filetocat) as f:
    for line in f:
        print line[:-1]

env_line = ['"environment information" {""', 0, '""', num_nodes, NET_BW, ' 0, 3};;']
line=', '.join(map(str,env_line))
print line
for node in range(num_nodes):
    #node_line = ['"node information" {0', node, '""', 1, in_links, out_links, 0.0, LAT, CPU_RATIO, 0.0, '0.0};;']
    node_line = ['"node information" {0', node, '""', 1, CPU_RATIO, 0.0, 0.0, 1, 1, 0, LAT, in_links, in_links, '0.0};;']
    line=', '.join(map(str,node_line))
    print line

mapping = range(num_nodes)
map_line = ','.join(map(str,mapping))
braced_tasks = ''.join(['[',num_tasks,']'])
trace_string = ''.join(['"',dim_trace,'"'])
begin_mapping_string = ''.join(['"mapping information" {', trace_string])
mapping_line = [begin_mapping_string, num_tasks, ''.join([braced_tasks, '{', map_line, '}};;'])]
line=', '.join(map(str,mapping_line))
print line

filetocat = CFGS_DIR + '/1ppn.tail.cfg'
with open(filetocat) as f:
    for line in f:
        print line[:-1]
