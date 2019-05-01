import numpy as np

from scipy.io import wavfile
from scipy.signal import spectrogram
from bokeh.plotting import *

fs, raw_data = wavfile.read('testaudio/testaudio.wav')


f, t, Sxx = spectrogram(raw_data, fs)
i=0
for freq in range(f.shape[0]):
    for time in range(t.shape[0]):
        df_spectogram.loc[i] = [f[freq],t[time],Sxx[freq][time]]
        i = i+1

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
PALETTE = ['#081d58', '#253494', '#225ea8', '#1d91c0', '#41b6c4', '#7fcdbb', '#c7e9b4', '#edf8b1', '#ffffd9']
mapper = LinearColorMapper(palette=PALETTE, low=np.min(Sxx), high=np.max(Sxx))
spectogram_figure = figure(title="Spectogram",x_axis_location="below", plot_width=900, plot_height=400,
            tools=TOOLS)
spectogram_figure.background_fill_color = "#eaeaea"
spectrogram_source = ColumnDataSource(data=dict(Sxx=df_spectogram['Sxx'],Frequency=df_spectogram['Frequency'],Time=df_spectogram['Time']))
spectogram_figure.circle(x="Time", y="Frequency", source=spectrogram_source, fill_color={'field': 'Sxx', 'transform': mapper}, line_color=None)