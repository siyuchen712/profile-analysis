import plotly.plotly as py
import plotly.graph_objs as go

def plot_profile(upper_threshold, lower_threshold, tolerance, title, df, channels, tc_channel_names, gl = False):
    data_all = []

    ls_index = list(df.index)

    for channel in channels:
        if tc_channel_names[channel]:
            tc_name = tc_channel_names[channel]
        else:
            tc_name = channel
        if gl:
            channel_plot = go.Scattergl(
                                x = df.index,
                                y = df[channel],
                                mode = 'lines',
                                name = tc_name)
        else:
            channel_plot = go.Scatter(
                                x = df.index,
                                y = df[channel],
                                mode = 'lines',
                                name = tc_name)
        data_all.append(channel_plot)

    dash_upper_threshold = go.Scatter(
        x = [ls_index[0], ls_index[-1]],
        y = [upper_threshold - tolerance, upper_threshold - tolerance],
        name = 'upper_threshold',
        line = dict(
            width = 4,
            dash = 'dot')
    )

    dash_lower_threshold = go.Scatter(
        x = [ls_index[0], ls_index[-1]],
        y = [lower_threshold + tolerance, lower_threshold + tolerance],
        name = 'lower_threshold',
        line = dict(
            width = 4,
            dash = 'dot')
    )

    data_all.append(dash_upper_threshold) 
    data_all.append(dash_lower_threshold)

    layout = dict(title = title,
              xaxis = dict(title = 'Time'),
              yaxis = dict(title = 'Temperature'))
    fig = dict(data=data_all, layout=layout)
    py.plot(fig, filename=title)



def plot_profile_ra(upper_threshold, lower_threshold, tolerance, rate_adjustment, title, df, channels, tc_channel_names, gl = False):
    data_all = []
    ls_index = list(df.index)
    
    for channel in channels:
        if tc_channel_names[channel]:
            tc_name = tc_channel_names[channel]
        else:
            tc_name = channel
        if gl:
            channel_plot = go.Scattergl(
                                x = df.index,
                                y = df[channel],
                                mode = 'lines',
                                name = tc_name)
        else:
            channel_plot = go.Scatter(
                                x = df.index,
                                y = df[channel],
                                mode = 'lines',
                                name = tc_name)
        data_all.append(channel_plot)

    dash_upper_threshold = go.Scatter(
        x = [ls_index[0], ls_index[-1]],
        y = [upper_threshold - tolerance, upper_threshold - tolerance],
        name = 'upper_threshold_amb',
        line = dict(
            width = 4,
            dash = 'dot')
    )

    dash_lower_threshold = go.Scatter(
        x = [ls_index[0], ls_index[-1]],
        y = [lower_threshold + tolerance, lower_threshold + tolerance],
        name = 'lower_threshold_amb',
        line = dict(
            width = 4,
            dash = 'dot')
    )


    dash_upper_ra = go.Scatter(
        x = [ls_index[0], ls_index[-1]],
        y = [upper_threshold - (upper_threshold-lower_threshold)*rate_adjustment/100, upper_threshold - (upper_threshold-lower_threshold)*rate_adjustment/100],
        name = 'upper_threshold',
        line = dict(
            width = 4,
            dash = 'dashdot')
    )

    dash_lower_ra = go.Scatter(
        x = [ls_index[0], ls_index[-1]],
        y = [lower_threshold + (upper_threshold-lower_threshold)*rate_adjustment/100, lower_threshold + (upper_threshold-lower_threshold)*rate_adjustment/100],
        name = 'lower_threshold',
        line = dict(
            width = 4,
            dash = 'dashdot')
    )

    data_all.append(dash_upper_threshold) 
    data_all.append(dash_lower_threshold)
    data_all.append(dash_upper_ra)
    data_all.append(dash_lower_ra)
 
    layout = dict(title = title,
              xaxis = dict(title = 'Time'),
              yaxis = dict(title = 'Temperature'))
    fig = dict(data=data_all, layout=layout)
    py.plot(fig, filename=title)