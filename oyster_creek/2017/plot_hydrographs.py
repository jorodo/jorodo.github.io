#!/usr/bin/env python
import os
import sys
import numpy as np
import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates


oyster_lines = file('oyster_creek_data.txt').read().strip().split('\n')
rosharon_lines = file('rosharon_gauge_data.txt').read().strip().split('\n')

oyster_dates_list = []
oyster_stages_list = []
rosharon_dates_list = []
rosharon_stages_list = []

for line in oyster_lines:
    line_data = line.split()
    if line_data[0] != '#':
        str_date = '%s %s %s %s'%(line_data[0],line_data[1],
                                  line_data[2],line_data[3])
        date_object = datetime.datetime.strptime(str_date, '%B %d %Y %H:%M')
        oyster_dates_list.append(mpl.dates.date2num(date_object))
        oyster_stages_list.append(float(line_data[4]))
        
for line in rosharon_lines:
    line_data = line.split()
    if line_data[0] != '#':
        str_date = '%s %s'%(line_data[2],line_data[3])
        date_object = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M')
        rosharon_dates_list.append(mpl.dates.date2num(date_object))
        rosharon_stages_list.append(float(line_data[7]))
        
oyster_dates = np.array(oyster_dates_list)
oyster_stages = np.array(oyster_stages_list)
rosharon_dates = np.array(rosharon_dates_list)
rosharon_stages = np.array(rosharon_stages_list)
communication_stage = 50.8*np.ones(len(rosharon_dates))

mpl.rc('axes', labelsize=16)

fig, ax = plt.subplots()
kwargs = {'marker': 'o', 'markeredgecolor': 'b', 'markerfacecolor': 'None',
          'markersize': '8', 'markeredgewidth': 1.5, 'linestyle': 'None',
          'label': 'Oyster Creek (Dow Pump Station)'}
p1, = ax.plot_date(oyster_dates, oyster_stages, **kwargs)
ax.set_ylabel('Dow Pump Station Gauge Height [ft]')
ax1 = ax.twinx()
kwargs = {'linestyle': '-', 'color': 'k', 'marker':
          'None', 'label': 'Brazos River (Rosharon)'}
p2, = ax1.plot_date(rosharon_dates, rosharon_stages, **kwargs)
kwargs = {'linestyle': '--', 'color': 'r', 'linewidth': '0.75', 'marker':
          'None', 'label': 'Communication Stage (Rosharon)'}
p3, = ax1.plot_date(rosharon_dates, communication_stage, **kwargs)
ax1.set_ylabel('Rosharon Gauge Height [ft]')
ax.set_xlim(mpl.dates.date2num(datetime.datetime(2016,5,30)),
            mpl.dates.date2num(datetime.datetime(2016,6,21)))
# ax.xaxis.set_major_locator(mpl.dates.DayLocator())
# ax.xaxis.set_minor_locator(mpl.dates.HourLocator(np.arange(0, 25, 8)))
# ax.xaxis.set_minor_locator(mpl.dates.DayLocator())
# ax.xaxis.set_minor_locator(mpl.dates.HourLocator(np.arange(0, 25, 8)))
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%Y-%m-%d'))
ax.grid(True)
ax.fmt_xdata = mpl.dates.DateFormatter('%Y-%m-%d %H:%M:%S')
lines = [p1, p2, p3]
ax.legend(lines, [l.get_label() for l in lines], loc=4, frameon=False)
#     ax.legend(lines, [l.get_label() for l in lines], loc=4)
fig.autofmt_xdate()
fig.savefig('brazos_and_oyster_creek_hydrograph.pdf')
# fig.savefig('brazos_and_oyster_creek_hydrograph.png')
fig.clf()
    
