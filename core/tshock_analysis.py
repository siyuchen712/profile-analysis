import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import re
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.plotly as py
import plotly.graph_objs as go
from operator import itemgetter
import itertools
import xlsxwriter

from core.tshock_helpers import *


def tshock_analyze_all_channels(df, channels, amb, amb_errors, tc_channel_names, upper_threshold, lower_threshold, tolerance, rate_adjustment, date_format, file_extension, test_name):

    writer = create_wb(test_name) ## create workbook
    print('inside tshock_analyze_all_channels...')
    ## analyze ambient
    amb_upper_threshold = upper_threshold - tolerance
    amb_lower_threshold = lower_threshold + tolerance
    result_each_cycle_amb, df_summary_amb, ambient, content_instruction_ambient, cycle_amount = ambient_analysis(df, channels, amb, amb_upper_threshold, amb_lower_threshold, date_format)

    write_multiple_dfs(writer, [amb_errors, df_summary_amb, result_each_cycle_amb], 'Amb '+str(amb), 3, content_instruction_ambient)

    ### all other channels
    if rate_adjustment:  ## apply rate adjustment if supplied
        temp_adjustment = rate_adjustment*(float(upper_threshold) - float(lower_threshold))/100
        upper_threshold = upper_threshold - temp_adjustment
        lower_threshold = lower_threshold + temp_adjustment

    else: ## otherwise use tolerance used for ambient
        upper_threshold = amb_upper_threshold
        lower_threshold = amb_lower_threshold
    for channel in channels:
        print(channel)
        if channel != amb:
            result_each_cycle, df_summary_tc, n_reach_summary = pd.DataFrame(), pd.DataFrame(), pd.DataFrame() ## ensure reset
            result_each_cycle, df_summary_tc, content_instruction = single_channel_analysis(df, channel, amb, ambient, upper_threshold, lower_threshold, date_format, cycle_amount)
            if tc_channel_names[channel]:
                if file_extension == 'csv':
                    tc_name = tc_channel_names[channel] + ' (' + channel.split(' ')[1] + ')'
                else:
                    tc_name = tc_channel_names[channel]
            else:
                tc_name = channel
            write_multiple_dfs(writer, [df_summary_tc, result_each_cycle, n_reach_summary], tc_name, 3, content_instruction)
    
    ### format output excel file
    format_excel_file(writer)
    writer.save()

def format_excel_file(writer):
    workbook = writer.book
    table_format = workbook.add_format({'align':'center'})
    for sheet_name in writer.sheets:
        writer.sheets[sheet_name].set_column('A:Z', 27, table_format)


def ambient_analysis(df, channels, amb, upper_threshold, lower_threshold, date_format):
    ''' Analysis for ambient channel '''

    ## get the big gap of ambient (channel_1)
    print('inside ambient_analysis...')
    df_chan_Ambient = df[['Sweep #', 'Time', amb]].sort_values(['Sweep #']).reset_index(drop=True)
    sweep_screen = []
    for i in range(df_chan_Ambient.shape[0]):
        sweep_screen.append(i)
    df_chan_Ambient.insert(0,'Sweep_screen',pd.Series(sweep_screen, index=df_chan_Ambient.index).tolist())
    
    ambient, n_reach_ls_period = df_keypoints(amb, df_chan_Ambient, upper_threshold, lower_threshold)
    ambient = calculate_ramp_stats(amb, ambient, date_format)

    start_index_list = find_starting_point_case(amb, ambient, upper_threshold, lower_threshold)  

    down_i = start_index_list[0]
    up_i = start_index_list[1]
    cold_i = start_index_list[2]
    hot_i = start_index_list[3]

    ls_index_down, ls_index_up, ls_index_cold, ls_index_hot = [], [], [], []
    for i in range(int(ambient.shape[0]/4)):
        ls_index_down.append(i*4 + down_i)
        ls_index_up.append(i*4 + up_i)
        ls_index_cold.append(i*4 + cold_i)
        ls_index_hot.append(i*4 + hot_i)

    ### SOAK ANALYSIS
    df_soak_high, df_soak_low = soak_analysis(amb, amb, ambient, df_chan_Ambient, ls_index_cold, ls_index_hot, start_index_list)
    ### RAMP ANALYSIS
    df_transform_down, df_transform_up = ramp_analysis(ambient, df_chan_Ambient, ls_index_down, ls_index_up)
    ### Create summary
    result_each_cycle, df_summary = create_analysis_summary(amb, amb, df_soak_high, df_soak_low, df_transform_down, df_transform_up)
    cycle_amount = len(result_each_cycle)
    
    if n_reach_ls_period == []: 
        content_instruction = ['Version 3.0\n\nIn this tshock test file, there are '+ str(cycle_amount) +' cycles.\n\nThe First Table: List out the test data that have reading error.', 'The Second Table: Summary table for the ambient.', 'The Third Table: List out the calculation result for each cycle of ambient.']
    else: 
        content_instruction = ['Version 3.0\n\nIn this tshock test file, there are '+ str(cycle_amount) +' cycles.\n\nThe First Table: List out the test data that have reading error.', 'The Second Table: Summary table for the ambient.\n\nNot every cycle reached the threshold!', 'The Third Table: List out the calculation result for each cycle of ambient.']

    return result_each_cycle, df_summary, ambient, content_instruction, cycle_amount


def single_channel_analysis(df, channel, amb, ambient, upper_threshold, lower_threshold, date_format, cycle_amount):
    ''' Analysis for non-ambient channels '''

    df_summary = pd.DataFrame()
    n_reach_summary = pd.DataFrame()
    n_reach = pd.DataFrame()
    ####Test for one channel
    df_chan = df[['Sweep #', 'Time']+[channel]].sort_values(['Sweep #']).reset_index(drop=True)
    sweep_screen = []
    for i in range(df_chan.shape[0]):
        sweep_screen.append(i)
    df_chan.insert(0,'Sweep_screen',pd.Series(sweep_screen, index=df_chan.index).tolist())
    
    selected_channel, n_reach_ls_period = df_keypoints(channel, df_chan, upper_threshold, lower_threshold)
    #### Cycle Statistics #####
    selected_channel = calculate_ramp_stats(channel, selected_channel, date_format)

    start_index_list = find_starting_point_case(channel, selected_channel, upper_threshold, lower_threshold)  

    down_i = start_index_list[0]
    up_i = start_index_list[1]
    cold_i = start_index_list[2]
    hot_i = start_index_list[3]

    ls_index_down, ls_index_up, ls_index_cold, ls_index_hot = [], [], [], []
    for i in range(int(ambient.shape[0]/4)):
        ls_index_down.append(i*4 + down_i)
        ls_index_up.append(i*4 + up_i)
        ls_index_cold.append(i*4 + cold_i)
        ls_index_hot.append(i*4 + hot_i)

    ### SOAK ANALYSIS
    df_soak_high, df_soak_low = soak_analysis(channel, amb, selected_channel, df_chan, ls_index_cold, ls_index_hot, start_index_list)   

    ### RAMP ANALYSIS
    df_transform_down, df_transform_up = ramp_analysis(selected_channel, df_chan, ls_index_down, ls_index_up)

    ### Create summary
    result_each_cycle, df_summary = create_analysis_summary(amb, amb, df_soak_high, df_soak_low, df_transform_down, df_transform_up)
    if n_reach_ls_period == []: 
        content_instruction = ['Every cycle of this channel can reach the threshold!\n\nThe First Table: List out the summary table.', 'The Second Table: Calculate result for cycle of this channel.', 'Analysis Finished!']
    else:
    	content_instruction = ['Not every cycle of this channel can reach the threshold!\n\nThe First Table: List out the summary table.', 'The Second Table: Calculate result for cycle of this channel.', 'Analysis Finished!']

    return result_each_cycle, df_summary, content_instruction

