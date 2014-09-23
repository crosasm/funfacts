***********************************************************************
******								 ******
******		Performance factors extrapolation.		 ******
******								 ******
******				v.0.0r06			 ******
****** 		Questions?, please contact: crosas@bsc.es	 ******
******								 ******
***********************************************************************

Pre-requisites:
=========================================================================================
  - Point local variable AUTOMATIC_ANALYSIS to this folder (more information in setup.sh)
  - Dimemas installation (scripts has been evaluated with version 5.2.5)
  - Python 2.7.3 (other versions had not been evaluated yet)
  - The following python modules:
      - numpy 1.6.4
      - scipy 0.11.1 (or greater)
      - lmfit 0.7.2 (or greater) -- http://cars9.uchicago.edu/software/python/lmfit/
      numpy and scipy can be installed from the package manager.
      To install lmfit, decompress the file included here, and as a root user type: 
      
	  #	python setup.py install
	  
  - Traces to be analyzed (some example traces are included in nekbone_bgq)

NOTE: To verify the versions of the modules installed, you can run

> python run_this_first.py

=========================================================================================
1. Extracting model factors (Load Balance, Serialization, Transfer, Parallel Efficiency):
=========================================================================================

To obtain a summary with information for performance factors:
    
     $ model_factors.py {time|cycles} {latency} {bandwitdh} <name_defined_by_user> <list_of_traces>.prv
     
     For example:
     
     $ model_factors.py time 2 1000 nekbone_example nekbone_bgq/*.prv
     
     Extracts the performance factors from all the traces included in nekbone_bgq. Results are shown in a
     model_factors_<name_defined_by_user>.csv file and a gnuplot file.
     
     To see the resulting graph:
     
     $ gnuplot model_factors_timeBased_nekbone_example.gnuplot
     
=========================================================================================
2. Projection of performance factors based on the knowledge of the application:
=========================================================================================

To extrapolate the collected performance factors (from a very small number of core counts to larger core counts),
user must indicate the appropiate fitting model to each one of the factors.

From the measured values, Serialization and Transfer can be extrapolated based on an Amdahl's Law-based model
or on a Pipeline-based fitting model, under this form:

      Amdalh_fit = elem_0 / (f_elem - (1-f_elem) * P)
      
      Pipeline_fit = (elem_0 * P) / ((1-f_elem) + f_elem*(2*P-1))
  
     *** elem_0 and f_elem are estimated using the least squares method over the collected measuremes, 
     and P the is number of processes used.
     
While Load Balance supports Amdahl's-based fitting, it also supports the use of constants: the minimum (min) --or
worst value from collected measurements--, or the average (avg) value.

Therefore, the framework is called:

    $ projection_efficiency.py {linear|cubic} <Serialization>{amdahl|pipeline} <Transfer>{amdahl|pipeline} <LoadBalance> {min|avg|amdahl} <name_of_csv_file>.csv
    
    From previous example:
    
    $ projection_efficiency.py model_factors_timeBased_nekbone_example.csv 
    
    or 
    
    $ projection_efficiency.py linear amdahl amdahl amdahl model_factors_timeBased_nekbone_example.csv 
    
    Generates the extrapolation of performance factors, with the comparison between measurements and projected variables using amdahl's model to fit 
    (model_factors_timeBased_nekbone_example_Pred_vs_Meas.gnuplot),  and the final estimation of the parallel efficiency 
    (prediction_model_model_factors_timeBased_nekbone_example.linear_P_amdahl.ALLMODELFACTORSprediction.gnuplot).
    CSV files are also generated to facilitate porting data to a spreadsheet. 
    
    For this example the number of processes has been considered linear. The cubic option was implemented for applications where the total data is distributed
    among the processes under a cubic shape (e.g. HACC from Coral Benchmark has this peculiarity)

    Projection_Efficiency.py has by default the values of linear for the number of processes, and Amdahl's model to fit all performance factors. To change these values
    the framework can be called using pipeline or min instead of amdahl as parameter (if the performance factors has this option for fitting). For example:
    
    $ projection_efficiency.py linear pipeline pipeline min model_factors_timeBased_nekbone_example.csv
    
    New fitting modules and additional enhancements are still under development.

=========================================================================================
Any further questions or doubts, please contact: crosas@bsc.es      (v.0.0r7)
=========================================================================================
 
