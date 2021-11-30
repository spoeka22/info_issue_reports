# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 17:27:23 2021

@author: AnnaWiniwarter
"""
import ixdat as ix
from ixdat.techniques.ec_ms import ECMSCalibration
 

#somehow if cv_1 is not calibrated, then it doesnt get saved with a "raw potential" column (which is really weird)
full_data = ix.Measurement.read("./full_data_COstrip_11-11-21.csv", reader="ixdat")
co_strip = full_data.cut(tspan=[13525,15450]) 

if True:
    #try to first convert to ECMSCyclicVoltammogram, then calibrate 
    co_strip_cv = co_strip.as_cv()
    co_strip_cv.redefine_cycle(start_potential=0.05, redox=False) #this is NOT optional!?
    co_strip_cv.tstamp +=13525
    #do the calibration based on the CO strip
    co2_cal = co_strip.ecms_calibration('CO2', 'M44', n_el=+2, tspan=[700, 800], tspan_bg=[600,700])
    co_strip_cv.calibration = ECMSCalibration(ms_cal_results=[co2_cal])

elif False:
    #try to first calibrate, then convert to ECMSCyclicVoltammogram
    co_strip.tstamp +=13525
    #do the calibration based on the CO strip
    co2_cal = co_strip.ecms_calibration('CO2', 'M44', n_el=+2, tspan=[700, 800], tspan_bg=[600,700])
    co_strip.calibration = ECMSCalibration(ms_cal_results=[co2_cal])
    co_strip_cal_cv = co_strip.as_cv()
    #and now select the cycles of interest
    stripping_cycle = co_strip_cal_cv[1]
    base_cycle =co_strip_cal_cv[2]
    axes_d = stripping_cycle.plot_vs_potential(mol_list=["CO2_M44"], logplot=False, legend=False, unit="nmol/s")
    base_cycle.plot_vs_potential(axes=axes_d, mol_list=["CO2_M44"], logplot=False, linestyle=":", legend=False, unit="nmol/s")

elif True:
    #what I actually want to do, and what works when choosing the cycles with tspan is
    #the following plotting calibrated CO strip vs potential with either 2nd cycle or blank cycle
    co_strip.tstamp +=13525
    co2_cal = co_strip.ecms_calibration('CO2', 'M44', n_el=+2, tspan=[700, 800], tspan_bg=[600,700])
    co_strip.calibration = ECMSCalibration(ms_cal_results=[co2_cal])
    stripping_cycle = co_strip.cut(tspan=[500,1290])
    base_cycle = co_strip.cut(tspan=[1290,1900])
    
    axes_d = stripping_cycle.plot_vs_potential(mol_list=["CO2_M44"], logplot=False, legend=False, unit="nmol/s")
    base_cycle.plot_vs_potential(axes=axes_d, mol_list=["CO2_M44"], logplot=False, linestyle=":", legend=False, unit="nmol/s")
    

