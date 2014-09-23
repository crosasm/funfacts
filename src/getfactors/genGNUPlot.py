#! /usr/bin/env python
import os
import argparse

#####################################################################################
###             Function to generate the .gnuplot file
#####################################################################################
def genGNUPlotfile(measured_file, name): 

   if (name == 'time'):
      gnuplot_file     = measured_file[:-4] + '.gnuplot'
   elif (name == 'cycles'):
      gnuplot_file     = measured_file[:-4] + '.gnuplot'

   name = measured_file[:-4
]
   with open(gnuplot_file, "w") as f:
      f.write('set datafile separator ","\n')
      f.write('\n')
      f.write("set title \"Model Factors Summary\\n{%s}\" \n"%name)
      #f.write('set title \'Model Factors Summary  -- ' + measured_file[:-4] + '\n')
      f.write('set xlabel \'Processes\' \n')
      f.write('set ylabel \'Performance\' \n')
#      f.write('set y2label \'Execution time (s)\' \n')
      f.write('\n')
      f.write('set xrange [:]\n')
#      f.write('set x2range [:]\n')
      f.write('set yrange [0:1]\n')
#      f.write('set y2range [0:]\n')
      f.write('set logscale x 2\n')
      f.write('\n')
#  f.write('set grid linewidth 0.5\n')
#  f.write('set border lw 1\n')
      f.write('set key bottom right inside\n')
      f.write('\n')
      f.write('set style data linespoints\n')
      f.write('\n')
      f.write('plot \'%s\' using 1:3 lt 1 lc 1 lw 1.5 title \"Load Balance\",'%measured_file)
      f.write('\'%s\' using 1:4 lt 2 lc 2 lw 1.5 title \"Serialization\",' %measured_file)
      f.write('\'%s\' using 1:5 lt 3 lc 3 lw 1.5 title \"Transfer\",' %measured_file)
      f.write('\'%s\' using 1:6 lt 4 lc 4 lw 1.5 title \"Parallel Efficiency\"\n'  %measured_file)
#      f.write('\'%s\' using 1:6 lt 4 lc 4 lw 1.5 title \"Paralell Efficiency\",'  %measured_file)
#      f.write('\'%s\' using 1:2 lt 0 lw 1.5 title \"Time Efficiency\"\n'  %measured_file)
#  f.write('quit\n') #close the gnuplot window
      f.write('\n')
      f.write('pause -1 "Press return to continue..."\n')

   f.close()
   print "File %s has been generated" %gnuplot_file

def genGNUPlotfileFactorsPredicted(prediction_file):

   gnuplot_file     = prediction_file[:-4] + '.ALLMODELFACTORSprediction.gnuplot'
   name = prediction_file[2:-4]
   with open(gnuplot_file, "w") as f:
      f.write('set datafile separator ","\n')
      f.write('\n')
      f.write("set title \"Extrapolation of Fundamental Factors\\n{%s}\"\n"%name)
      f.write('set xlabel \'Processes\' \n')
      f.write('set ylabel \'Performance\' \n')
      f.write('\n')
      f.write('set xrange [:]\n')
      f.write('set yrange [0:1]\n')
      f.write('set logscale x 10\n')
      f.write('\n')
#  f.write('set grid linewidth 0.5\n')
#  f.write('set border lw 1\n')
      f.write('set key right bottom inside\n')
      f.write('\n')
      f.write('set style data linespoints\n')
      f.write('\n')
      f.write('plot \'%s\' using 1:3 lt 1 lc 1 lw 1.5 title \"Load Balance\",'%prediction_file)
      f.write('\'%s\' using 1:4 lt 2 lc 2 lw 1.5 title \"Serialization\",' %prediction_file)
      f.write('\'%s\' using 1:5 lt 3 lc 3 lw 1.5 title \"Transfer\",' %prediction_file)
      f.write('\'%s\' using 1:2 lt 4 lc 4 lw 1.5 title \"Parallel Efficiency\"\n'  %prediction_file)
#  f.write('quit\n') #close the gnuplot window
      f.write('\n')
      f.write('pause -1 "Press return to continue..."\n')

   f.close()
   print "File %s has been generated" %gnuplot_file


def genGNUPlotfilePrediction(measured_file, prediction_file):

   gnuplot_file     = measured_file[:-4] + '_Pred_vs_Meas.gnuplot'

   name = measured_file[:-4]

   with open(gnuplot_file, "w") as f:
      f.write('set datafile separator ","\n')
      f.write('\n')
      f.write("set title \"Comparison of Predicted and Measured Fundamental Factors\\n{%s}\"\n"%name)
      f.write('set xlabel \'Processes\' \n')
      f.write('set ylabel \'Performance\' \n')
      f.write('\n')
      f.write('set xrange [:]\n')
      f.write('set yrange [0:1]\n')
      f.write('set logscale x 10\n')
      f.write('\n')
#  f.write('set grid linewidth 0.5\n')
#  f.write('set border lw 1\n')
      f.write('set key right bottom inside\n')
      f.write('set style data linespoints\n')
      f.write('\n')
      f.write('plot \'%s\' using 1:3  lt 5 ps 0.5 lc 1 lw 1.5 title \"Model Load Balance\",'%prediction_file)
      f.write('\'%s\' using 1:3 lt 1 lc 1 lw 1.5 title \"Measured Load Balance\",' %measured_file)
      f.write('\'%s\' using 1:4 ps 0.5 lt 5 lc 2 lw 1.5 title \"Model Serialization\",' %prediction_file)
      f.write('\'%s\' using 1:4 lt 2 lc 2 lw 1.5 title \"Measured Serialization\",' %measured_file)
      f.write('\'%s\' using 1:5 ps 0.5 lt 5 lc 3 lw 1.5 title \"Model Transfer\",' %prediction_file)
      f.write('\'%s\' using 1:5 lt 3 lc 3 lw 1.5 title \"Measured Transfer\",'  %measured_file)
      f.write('\'%s\' using 1:2 ps 0.5 lt 5 lc 4 lw 1.5 title \"Model Parallel Eff.\",' %prediction_file)
      f.write('\'%s\' using 1:6 lt 4 lc 4 lw 1.5 title \"Measured Parallel Eff.\"\n'  %measured_file)
#  f.write('quit\n') #close the gnuplot window
      f.write('\n')
      f.write('pause -1 "Press return to continue..."\n')

   f.close()
   print "File %s has been generated" %gnuplot_file
