#! /usr/bin/env python

########################################################################
#              Module to extract fundamental factors 
########################################################################

# '''
# Created on Sep 19, 2014
# 
#  model_factors script
# to run:
#  model_factor.py <cycles|time> latency bw <phase> <trace_list.txt> 
# report to:
#      measured_<phase>.csv
#      GNUPlot file: <phase>.gnuplot
# 
# @author: crosas
# '''

import argparse
from os import environ, getcwd
from os.path import exists
from utilities import emit_list, do_command, do_parse_2D
from utilities import get_processes, do_command_stdout, simulate
from genGNUPlot import genGNUPlotfile 

debug = False

if __name__ == '__main__':
    '''Points to the automatic_scripts folder'''
    MAIN_DIR = environ['AUTOMATIC_ANALYSIS']
    DATA_DIR = MAIN_DIR + '/data'
    CFGS_DIR = DATA_DIR + '/cfgs'
    SRC_DIR = MAIN_DIR + '/src/getfactors'
    
    parser = argparse.ArgumentParser()
    parser.add_argument('simulation', choices=['time', 'cycles'],
                        help="Choose bw time-based sims or on cycle-based")
    parser.add_argument('nominal_lat',
                        help="Nominal Latency for Dimemas simulations", type=int)
    parser.add_argument('nominal_bw',
                        help="Nominal BW for Dimemas simulations", type=int)
    parser.add_argument('phase',
                        help="Name of the phase represented in traces")
    parser.add_argument('trace_list', nargs='+',
                        help="List with the names of the traces")
    
    args = parser.parse_args()
    
    bw = args.nominal_bw
    latency = args.nominal_lat
    parser.print_help()
    
    if (debug):
        print args.simulation
        print args.traces_dir
        print args.trace_list
        print args.phase

#===================================================
#  Initialize variables 
#===================================================        
    paraver_files = {}
    metrics = {}
    Par_eff = []
    Eff_meas = []
    Ser_meas = []
    Trf_meas = []
    Trf_sche = []
    LB_meas = []
    Tcpu_meas = []
    X_list = []
    X_list_3 = []
    Sch_list = []
    LB_cst = 1.0
    Tcpu_cst = 0.0
    elems = 0
    accum = 0.0
    Tcpu_it = 0
    T0 = 0.0
    min_procs = 100000000000
      
#=======================================================================
#  Set paths and file names 
#=======================================================================

    graph_model_name = args.phase + "_model_factors.png"
    TMP_DIR = getcwd() + '/tmp'
    suffix = args.phase + '.csv'
    
    if (args.simulation == 'time'):
        measured_file = './model_factors_timeBased_' + suffix
    elif (args.simulation == 'cycles'):
        measured_file = './model_factors_cyclesBased_' + suffix
    else:
        print "Not a valid option!!!!"

    print "File %s stores resulting model factors" %measured_file 
    print "Traces to analyze: %s " %args.trace_list

#=======================================================================
#  Get number of processes in the trace 
#=======================================================================

###for name in traces_path:
    list_traces = args.trace_list

    for name in list_traces:
        #   full_path = traces_dir + name
        #   processes = get_processes(full_path)
        processes = get_processes(name)
        paraver_files[processes] = name

        if (processes < min_procs):
            min_procs = processes

#=======================================================================
#  Removes old files 
#=======================================================================

    if exists(TMP_DIR):
        print "TMP file already exists"
    else:
        do_command(['mkdir', './tmp'])
#   os.system("rm -rf ./tmp")
#
#
#if os.path.exists(measured_file):
#   do_command(['rm',measured_file])

#-----------------------------------------------------------------------
# BEGINS MAIN LOOP                                            ----------
#-----------------------------------------------------------------------
    for processes, trace in sorted(paraver_files.iteritems()):
#=======================================================================
#  Gets trace name 
#=======================================================================

    #print "Evaluates if there is a path in the name of the trace"
        occur = trace.count('/')
        print processes 

        trace_path = '' 

        if (occur >= 1):
            paths = trace.split('/')
            fields_path = int(len(paths))
            #print fields_path
            trace_name = paths[len(paths)-1]
        
            for i in range(len(paths)-1):
                #print paths[i]
                trace_path += paths[i] + '/'

        elif (occur == 0):
            trace_name = trace
        else:
            print "ERROR!!!!!"

        trace_path += trace_name
        #print trace_path

        print "========================================================"
        print 'Analyzing ', trace_name 
        print "========================================================"
#=======================================================================
#  Useful Time 
#=======================================================================
        duration  = 0.0
        with open (trace_path) as f:
            for line in f:
                words = line.split(':')
                if words[0] == str(2):
                    event_time = float(words[5])
                    if event_time > duration:
                        duration = event_time 
            if words[0] == str(1):
                if words[7] == str(1):
                    event_time = float(words[6])
                    if event_time > duration:
                        duration = event_time 

        duration = duration/1000000000

#=======================================================================
#  prv2dim 
#=======================================================================
        if (args.simulation == 'time'):
            dim_trace = TMP_DIR + '/' + trace_name[:-4]+'.dim'
        elif (args.simulation == 'cycles'):
            dim_trace =  TMP_DIR + '/' + trace_name[:-4] + '_cyc.dim'
        else:
            print "Choice not valid!!!"

        if exists(dim_trace):
            print dim_trace, ' Dimemas trace already exists. Reusing it'
        else:
            Dimemas_file = TMP_DIR + '/Dimemas.out' 
            fd=open(Dimemas_file, 'w')

            if (args.simulation == 'time'):   
#                 print "command prv2dim TIME"
                prv2dim = environ['DIMEMAS_HOME'] + '/bin/prv2dim'
#                 print prv2dim
                do_command_stdout([prv2dim, '-n', trace_path, dim_trace], fd)
            elif (args.simulation == 'cycles'):
                do_command_stdout([prv2dim, '-n', '-b',
                                   '42000059,0.000000000339', trace_path, dim_trace], fd)
            else:
                print "ERROR using prv2dim!!!!!"

#=======================================================================
#  Paramedir with a trace with unlimited BW and No-Latency
#=======================================================================
  
        if (args.simulation == 'time'):
            D_trace_name = TMP_DIR + '/' + '.'.join(['D', trace_name[:-4],
                                                     'ideal.prv' ])
            Tideal = simulate(dim_trace, 0.0, 0.0, 1.0, 1, 1, D_trace_name, TMP_DIR, SRC_DIR)
        elif (args.simulation == 'cycles'):
            D_trace_name = TMP_DIR + '/' + '.'.join(['D', trace_name[:-4],
                                                      'cyc_ideal.prv' ])
            CPUr = 1.0
            in_links = 1
            out_links = 1
            Tideal = simulate(dim_trace, 0.0, 0.0, CPUr, in_links,
                              out_links, D_trace_name, TMP_DIR)
        else:
            print "ERROR measuring Ideal Time"
  
        paramedir = environ['PARAVER_HOME'] + '/bin/paramedir'
        print paramedir
        command = [paramedir, D_trace_name ]
        command.extend ([ CFGS_DIR+'/2dp_mpi_stats.cfg',
                         TMP_DIR + '/2dp_mpi_stats.D.stats'])
        do_command( command )
  
        if (args.simulation == 'cycles'):
            D_trace_name = '.'.join(['D',trace_name[:-4],'cyc_based',
                                      ''.join(['BW', str(bw)]), ''.join(['L', str(latency)]), 'prv' ])
            exec_time_0_n = simulate (dim_trace, float(bw),
                                       float(latency)/1000000, CPUr, in_links, out_links,
                                       D_trace_name, TMP_DIR)
#=======================================================================
#  Paramedir with traces based on time
#=======================================================================
        command = ['paramedir', trace_path ]
        command.extend ([ CFGS_DIR+'/2dp_mpi_stats.cfg',
                          TMP_DIR+'/2dp_mpi_stats.stats'])
        command.extend ([ CFGS_DIR+'/2dp_mpi_time_stats.cfg',
                         TMP_DIR+'/2dp_mpi_time_stats.stats'])
        command.extend ([ CFGS_DIR+'/2dp_total_mpi_time_stats.cfg',
                         TMP_DIR+'/2dp_total_mpi_time_stats.stats'])
        command.extend ([ CFGS_DIR+'/2dp_ui.cfg',
                         TMP_DIR+'/2dp_ui.stats'])
        command.extend ([ CFGS_DIR+'/2dp_ipc.cfg',
                         TMP_DIR+'/2dp_ipc.stats'])
        do_command( command )
  
        usefulTime = float(do_parse_2D(TMP_DIR + '/2dp_mpi_time_stats.stats',
                                       'Average', 1)) / 1000000
        MPItime = float(do_parse_2D( TMP_DIR +'/2dp_total_mpi_time_stats.stats', 
                                    'Average', 2)) / 1000000
        efficiency = float(do_parse_2D(TMP_DIR + '/2dp_mpi_stats.stats', 
                                        'Average', 1)) / 100
        LB = float(do_parse_2D(TMP_DIR + '/2dp_mpi_stats.stats', 'Avg/Max', 1))
        accum += usefulTime
        uLB = float(do_parse_2D(TMP_DIR + '/2dp_mpi_stats.D.stats', 
                                 'Maximum', 1)) / 100
        CommEff = float(do_parse_2D(TMP_DIR + '/2dp_mpi_stats.stats', 
                                    'Maximum', 1)) / 100
        Transfer = CommEff/uLB
        err = (efficiency - LB*uLB*Transfer) / efficiency
        ui = float(do_parse_2D(TMP_DIR + '/2dp_ui.stats', 'Average', 1))
        ipc = float(do_parse_2D(TMP_DIR + '/2dp_ipc.stats', 'Average', 1))
        predicted = float((usefulTime) / efficiency)
  
        par_Eff = float(LB * uLB * Transfer)
        elems += 1
  
        if elems == 1:
            T0 = predicted
        predScal     = T0 / predicted  
#=======================================================================
#    Printing fundamental factors per trace  
#=======================================================================
        print "=== Fundamental factors using %d processes ==="%processes
        print "LB " + "\t" + " Trf " + "\t" + " Ser " + "\t" + " ParEff"
        print ("%.6f"%LB , "\t" , "%.6f"%Transfer , "\t" ,
               "%.6f"%uLB , "\t" , "%.6f"%efficiency)
        print "========================================================="
        print "Load Balance   : %.6f"%LB
        print "Serialization  : %.6f"%uLB
        print "Transfer       : %.6f"%Transfer   
        print "Par. Efficiency: %.6f"%efficiency
        print "========================================================="
#=======================================================================
#  Final store into arrays, dictionary and .csv file
#=======================================================================
  
    # Stores measured values into arrays
        Eff_meas.append(float(efficiency))
        Par_eff.append(float(par_Eff))
        LB_meas.append(float(LB))
        Tcpu_meas.append(float(usefulTime))
        Ser_meas.append(float(uLB))
        Trf_meas.append(float(Transfer))
        X_list.append(int(processes))
        Pro_3 = float(int(processes)**(1/3.0))
        X_list_3.append(float(Pro_3))
        Sch_list.append(float(1.0))
  
    # Stores data for proc_n into a dictionary
        metrics[int(processes)] = (float(efficiency), float(LB), float(uLB), 
                                   float(Transfer), float(par_Eff), float(CommEff),
                                    abs(err), float(usefulTime), float(duration),
                                    float(ui/1000000), float(ipc), float(predicted),
                                    float(predScal), float(Pro_3), float(1.0))
        processes = 0
        efficiency = 0.0
        par_Eff = 0.0
        LB = 0.0
        usefulTime = 0.0
        uLB = 0.0
        Transfer = 0.0
        CommEff = 0.0
        err = 0.0
        duration = 0.0
        ui = 0.0
        ipc = 0.0
        predicted = 0.0
        predScal = 0.0
        Pro_3 = 0
  
#-----------------------------------------------------------------------
# END LOOP                                                    ----------
#-----------------------------------------------------------------------
# ======================================================================
# Saves model factors into measured_<name_of_the_phase>.csv file
# =======================================================================
  
    emit_list(measured_file, ('proc, Eff, LB, Ser, Trf, ParEff, CommEff, err, TCPU, Time, ui, ipc, prediction, Scaled_eff, proc_13, Sche\n'), metrics)
  
# =======================================================================
# Builds GNUPlot file to be shown in Paraver
# # ======================================================================
    genGNUPlotfile(measured_file, args.simulation)