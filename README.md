# Temperature Analysis Profile 

This program analyzes the temperature of raw environmental test data for automotive lighting systems. The tests expose lighting systems to various temperature profiles while the systems are powered. The primary function of this project is to detect if the changing of temperature of each sample and the ambient is as consistent and regular as the particular and regular changed temperature condition.

## Input Raw Data Sample
**1. Thermal Shock data (CSV.)**

**2. PTC data (CSV. or TXT.)**

## Current Limits

This program can only analyze the cycles that can reach the threshold, but will leave those cycles cannot reach as blank. 

## Core Functions

**1. Temporal Plotting**

**2. Summary Tables with basic statistics**
* List out outrage data
* Statistic summary of all the cycles
* List out all the calculate result of each cycle: (the attributes listed as below)
   * Cold_soak_duration_minute
   * Cold_soak_mean_temp_c
   * Cold_soak_max_temp_c
   * Cold_soak_min_temp_c
   * Hot_soak_duration_minute
   * Hot_soak_mean_temp_c
   * Hot_soak_max_temp_c
   * Hot_soak_min_temp_c
   * Down_recovery_time_minute
   * Down_RAMP_temp_c
   * Down_RAMP_rate_c/minute
   * Up_recovery_time_minute
   * Up_RAMP_temp_c
   * Up_RAMP_rate_c/minute

### Introduction
**1. Gui**

![Gui UI](/images/tshock_gui.PNG)

   * In this interface, user give the input of this program.
   * Choose the raw testdata file and the type of this test.
   * Give a name or discription to this datafile over Test Name box.
   * Input the Upper & Lower Threshold, and Temperate Tolerance.
   * Input Component rate adjustment if it exists.
   

![Gui UI_2](/images/tshock_gui_2.PNG)

   * In this interface, this program can detect there are how many channels in this test.
   * User can label out which channel is the Ambient.
   * Give a brief discription for each channel or leave it blank.
   * All of these brief label will show in the tab of output excel file.
   
**2. Analyze! (Click "Analyze!" Button)**

![Analyze](/images/notification.PNG)

   * In this interface, the notification can show the progress of analysis, and also can show how the channel start.
   
**3. Plotting**

![general_graph](/images/general_plot.PNG)

   * This is the general plot of raw testdata.
   * The X axis is the time scale and index.
   * The Y axis is the temperature(C) over that scan.
   * This graph can show only selected channels, and also can zoom in and out.
   
![selected_graph](/images/scale_in_graph.PNG)

![selected_graph](/images/ambient_graph.PNG)

**4. Output Excel**

![selected_graph](/images/output.PNG)

   * Each tab of the output excel represent one channel.
   * Each sheet is consisted with 3 tables as this instruction mentioned above.

## Authors

* Siyu Chen
* Sam Bruno
