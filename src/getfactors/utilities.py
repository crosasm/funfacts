#! /usr/bin/env python
######################################################################
# utilities
# methods used in some of the scripts
######################################################################
import csv
import os
import subprocess

debug = False

def do_command(command):
    if (debug):
        print command
    process = subprocess.Popen(command)
    process.wait()
    if process.returncode != 0:
        print 'error', process.returncode , ' reported by command: ', ' '.join(command)

def do_command_stdout(command, out):
#     if (debug):
    print command
    process = subprocess.Popen(command, stdout=out)
    process.wait()
    if process.returncode != 0:
        print 'error', process.returncode , ' reported by command: ', ' '.join(command)
        
def do_parse_2D(stats_file, tag, col):
    with open(stats_file) as f:
        for line in f:
            words = line.split('\t')
            if len(words) > 1:
                if words[0] == tag:
                    return words[col]

def simulate (dim_trace, bw, lat, CPUr, in_links, out_links, D_trace_name, TMP_DIR, SRC_DIR):
    command = [SRC_DIR+'/dimemas_cfg_gen.py',  dim_trace, str(float(bw)), '%.8f'%lat, str(CPUr), str(in_links), str(out_links) ]
    configuration_file = TMP_DIR + '/configuration.cfg'
    fd=open(configuration_file, 'w')
    do_command_stdout(command, fd)
    
    Dimemas = os.environ['DIMEMAS_HOME'] + '/bin/Dimemas'
    command = [Dimemas,'-S',' 32K', '-pa ', D_trace_name, configuration_file ]
    Dimemas_file = TMP_DIR + '/Dimemas.out'
    fd=open(Dimemas_file, 'w')
    do_command_stdout(command, fd)
    
    with open(Dimemas_file) as f:
        for line in f:
            words = line.split(':')
            if words[0] == 'Execution time':
                return float(words[1][1:-1])

def get_processes(paraver_file):
    print paraver_file
    print os.getcwd()
    with open(paraver_file) as f:
        for line in f:
            words = line.replace('(',':').replace(')',':').split(':')
            return int(words[9])

def wait(str_ng=None, prompt='Press return to show results...\n'):
    if str_ng is not None:
        print str_ng
        raw_input(prompt)

def emit_list(filename, header, list_name):
    with open(filename, "w") as w:
        w.write(header)
        for key, val in sorted(list_name.iteritems()):
            w.write(str(key))
            for item in val:
                w.write(','+ str(item))
            w.write('\n')

def get_dict (filename):                        #Reads the *.csv into a dictionary
    meas_csv = {}
    if (debug):
        print filename
    input_file = csv.DictReader(open(filename))
    for row in input_file:                       #Loads the .csv into memory
        meas_csv[row["proc"]] = {'Eff':float(row[" Eff"]), 'LB':float(row[" LB"]), 'Ser': row[" Ser"], 'Trf': row[" Trf"],
                              'CommEff':row[" CommEff"], 'err':row[" err"], 'Tcpu':row[" TCPU"], 'Time':row[" Time"],
                              'ui':row[" ui"], 'IPC':row[" ipc"], 'Pred':row[" prediction"], 'Scal_eff':row[" Scaled_eff"] }
    return meas_csv


def get_fields (field_name, proc, filename):
    #Reads data from an specific field and number of processes
#     dict_csv     = {}
    elem         = []
    dict_csv = get_dict(filename)
    
    if (debug):
        print field_name
        print dict_csv
        print proc
        print dict_csv[str(proc)][field_name]
        
    elem.append(float(dict_csv[str(proc)][field_name]))
    return elem

def get_elem (field_name, proc, filename):
#     #Reads data from an specific field and number of processes
#     dict_csv = {}
#     elem = []
    dict_csv = get_dict(filename)
    
    if (debug):
        print field_name
        print dict_csv
        print proc
        print dict_csv[str(proc)][field_name]
    return (float(dict_csv[str(proc)][field_name]))