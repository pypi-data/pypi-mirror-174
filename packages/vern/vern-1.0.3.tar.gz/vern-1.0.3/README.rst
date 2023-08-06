VERN: Very Easy Research Note

how to use
##########
Drop one or multiple files on `parse_all.bat`

contribute
##########

bug report
==========
Use the `issues` feature of GitHub. Please use only English

code update
===========
Use the `pull request` feature of GitHub. Please use only English

types of files
##############

profilometer (Tencor P7)
========================
* `*.txt` file will be regarded as a profilometer file
* modify filename to `*_i.txt` to enable interactive mode
    * interactive mode can crop part of the profile and apply it to normal plot and histogram

tabular
=======
* `*_m1.txt` file will be regarded as a tabular file
* tabular data is consisted of two columns
    * each column will be used as x and y data
    * the column labels will be used for the x and y axis label
    * x,y plot will be shown as dots
    * a linear approximation line will be added to the plot
        * the equations for the approximated line and the R2 value will appear on the plot

VSM
===
* in progress

oscilloscope
============
* in progress

dxf
===
* in progress
