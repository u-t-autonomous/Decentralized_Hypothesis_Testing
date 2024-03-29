import json
import matplotlib
# matplotlib.use('pgf')
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from math import ceil
from math import pi
import math
from ast import literal_eval
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import (DrawingArea,OffsetImage,AnnotationBbox)
import numpy as np
from gridworld import *
import texfig



# ---------- PART 1: Globals

with open('5agents_4range_sync_average.json') as json_file:
	data = json.load(json_file)
df = pd.DataFrame(data)
my_dpi = 96
scale_factor = 0.6
# Writer = matplotlib.animation.writers['ffmpeg']
# writer = Writer(fps=2.5, metadata=dict(artist='Me'), bitrate=1800)
fig = texfig.figure(width=3.3*scale_factor,ratio=1, dpi=my_dpi)
my_palette = plt.cm.get_cmap("tab10",len(df.index))
categories = [str(d_i) for d_i in df['0'][0]['Id_no']]
# cat_hold = []
# cat_hold.append(categories.pop())
# cat_hold.append(categories.pop())
# cat_hold.append(categories.pop())
# categories.append(cat_hold.pop(0))
# categories.append(cat_hold.pop(0))
# categories.append(cat_hold.pop(0))
categories = [categories[0],categories[2],categories[1],categories[4],categories[3]]
belief_good = df['0'][0]['GoodBelief']
belief_bad = df['0'][0]['BadBelief']
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
axis_array = []
l_data = []
f_data = []
belief_x_good = []
belief_x_bad = []
belief_y_bad = []
belief_y_good = []
# plt.show()
frames = 50


def update(i):
	global plot_data, df
	l_d = plot_data[0]
	f_d = plot_data[1]
	for l,l_f,id_no in zip(l_d,f_d,categories):
		values = df[str(i)][id_no]['ActBelief']
		cat_range = range(N)
		value_dict = dict([[c_r, 0.0] for c_r in cat_range])
		for v_d in value_dict.keys():
			for k_i in values.keys():
				if literal_eval(k_i)[v_d] == 1:
					value_dict[v_d] += 100 * values[k_i]

		val = list(value_dict.values())
		val += val[:1]
		l.set_data(angles,val)
		l_f.set_xy(np.array([angles,val]).T)
	# plot_data = [l_d,f_d]
	return l_d + f_d


def grid_init(nrows, ncols, obs_range):
	# fig_new = plt.figure(figsize=(1000/my_dpi,1000/my_dpi),dpi=my_dpi)
	ax = plt.subplot(111)
	t = 0
	row_labels = range(nrows)
	col_labels = range(ncols)
	plt.xticks(range(ncols), col_labels)
	plt.yticks(range(nrows), row_labels)
	ax.set_xticks([x - 0.5 for x in range(1, ncols)], minor=True)
	ax.set_yticks([y - 0.5 for y in range(1, nrows)], minor=True)
	ax.set_xlim(-0.5,ncols-0.5)
	ax.set_ylim(-0.5,nrows-0.5)
	ax.invert_yaxis()
	ag_array = []
	plt.grid(which="minor", ls="-", lw=1*scale_factor)
	i = 0
	for id_no in categories:
		p_t = df[str(0)][id_no]['PublicTargets']
		color = my_palette(i)
		init_loc = tuple(reversed(coords(df[str(0)][id_no]['AgentLoc'][0], ncols)))
		c_i = plt.Circle(init_loc, 0.45, color=color)
		# route_x, route_y = zip(*[tuple(reversed(coords(df[str(t)][str(id_no)]['NominalTrace'][s][0],ncols))) for s in df[str(t)][str(id_no)]['NominalTrace']])
		cir_ax = ax.add_artist(c_i)
		lin_ax = ax.add_patch(patches.Rectangle(np.array(init_loc)-obs_range-0.5, 2*obs_range+1, 2*obs_range+1,fill=False, color=color, clip_on=True, alpha=0.5, ls='--', lw=4*scale_factor))
		# plt_ax, = ax.plot(route_x, route_y, color=color, linewidth=5, linestyle='solid')
		plt_ax = None
		# route_x, route_y = zip(*[tuple(reversed(coords(df[str(t)][str(id_no)]['BadTrace'][s][0], ncols))) for s in df[str(t)][str(id_no)]['BadTrace']])
		# plt_ax2, = ax.plot(route_x, route_y, color=color, linewidth=5, linestyle='--',dashes=[3, 8, 2, 5, 1, 6],alpha=0.8)
		plt_ax2 = None
		# ag_array.append([cir_ax, lin_ax, plt_ax,plt_ax2])
		ag_array.append([cir_ax, lin_ax])
		for k in p_t:
			s_c = coords(k, ncols)
			ax.fill([s_c[1]+0.4, s_c[1]-0.4, s_c[1]-0.4, s_c[1]+0.4], [s_c[0]-0.4, s_c[0]-0.4, s_c[0]+0.4, s_c[0]+0.4], color=color, alpha=0.9)
		i += 1
	return ag_array

def belief_chart_init():
	ax = plt.subplot(222)
	ax.set_xlim([0,frames])
	ax.set_ylim([-0.1,1.2])
	ax.yaxis.set_ticks(np.arange(0,1.1,0.1))
	plt.rc('text',usetex=True)
	plt.xlabel(r't')
	plt.ylabel(r'Belief $\left(b^a_j(\theta)\right)$')
	plt_array = []
	for i,id_no in enumerate(categories):
		belief_x_bad.append([])
		belief_x_bad[i].append(0)
		belief_y_bad.append([])
		belief_y_bad[i].append(df['0'][id_no]['ActBelief'][belief_bad])
		belief_x_good.append([])
		belief_x_good[i].append(0)
		belief_y_good.append([])
		belief_y_good[i].append(df['0'][id_no]['ActBelief'][belief_good])
		px1, = ax.plot([0,0.0], [0,0.0], color=my_palette(i), linewidth=3, linestyle='solid', label=r'Actual belief: $b^a_'+str(i)+r'(\theta^\star)$')
		px2, = ax.plot([0,0.0], [0.0,0.0], color=my_palette(i), linewidth=3, linestyle='dashed', label=r'Incorrect belief $b^a_'+str(i)+r'(\theta_0)$')
		plt_array.append((px1,px2))
	leg = ax.legend(loc='right')
	return plt_array

def con_init():
	ax = plt.subplot(224)
	plt.axis('off')
	ax.set_xlim([-ax.get_window_extent().height/2, ax.get_window_extent().height/2])
	ax.set_ylim([-ax.get_window_extent().height/2, ax.get_window_extent().height/2])
	radius = ax.get_window_extent().height/2 - 50
	cir_array = []
	loc_dict = {}
	for col, a_i in enumerate(angles[:-1]):
		loc = tuple(np.array([radius*math.sin(a_i),radius*math.cos(a_i)]))
		loc_dict.update({categories[col]:loc})
		p_c = patches.Circle(loc,36,color=my_palette(col),zorder=4)
		ax.add_artist(p_c)
		cir_array.append(p_c)
	line_dict = {}
	for l_d in loc_dict:
		for k_d in loc_dict:
			x_point,y_point = zip(*[loc_dict[l_d], loc_dict[k_d]])
			p_l, = ax.plot(x_point,y_point,linewidth=5,color=(0,0,0),zorder=1)
			p_l.set_visible(False)
			line_dict.update({(l_d, k_d): p_l})
	return line_dict

def grid_update(i):
	global ax_ar, df, ncols, obs_range
	write_objects = []
	for a_x, id_no in zip(ax_ar, categories):
		# c_i, l_i, p_i,p_2 = a_x
		c_i, l_i = a_x
		loc = tuple(reversed(coords(df[str(i)][id_no]['AgentLoc'][0], ncols)))
		c_i.set_center(loc)
		l_i.set_xy(np.array(loc)-obs_range-0.5)
		# route_x, route_y = zip(*[tuple(reversed(coords(df[str(i)][str(id_no)]['NominalTrace'][s][0], ncols))) for s in df[str(i)][str(id_no)]['NominalTrace']])
		# p_i.set_xdata(route_x)
		# p_i.set_ydata(route_y)
		# route_x2, route_y2 = zip(*[tuple(reversed(coords(df[str(i)][str(id_no)]['BadTrace'][s][0], ncols))) for s in
		#                          df[str(i)][str(id_no)]['BadTrace']])
		# p_2.set_xdata(route_x2)
		# p_2.set_ydata(route_y2)
		write_objects += [c_i] + [l_i] # + [p_i] + [p_2]
	return write_objects

def belief_update(i):
	global bel_lines, df, belief_x_good, belief_y_good, belief_x_bad, belief_y_bad
	change_array = []
	for j, id_no in enumerate(categories):
		belief_x_bad[j].append(i)
		belief_x_good[j].append(i)
		belief_y_good[j].append(df[str(i)][id_no]['ActBelief'][belief_good])
		belief_y_bad[j].append(df[str(i)][id_no]['ActBelief'][belief_bad])
		bel_lines[j][0].set_xdata(belief_x_good[j])
		bel_lines[j][0].set_ydata(belief_y_good[j])
		bel_lines[j][1].set_xdata(belief_x_bad[j])
		bel_lines[j][1].set_ydata(belief_y_bad[j])
		change_array += bel_lines[j]
	return change_array

def connect_update(i):
	global con_dict, df
	change_array = []
	for id_no in categories:
		for id_other in categories:
			if int(id_other) in df[str(i)][id_no]['Visible']:
				# if con_dict[(id_no,id_other)]._visible != True:
				con_dict[(id_no, id_other)].set(visible=True, zorder=0)
				change_array.append(con_dict[(id_no, id_other)])
			else:
				# if con_dict[(id_no,id_other)]._visible == True:
				con_dict[(id_no, id_other)].set(visible=False, zorder=0)
				change_array.append(con_dict[(id_no, id_other)])
	return change_array
	


def coords(s,ncols):
	return (int(s /ncols), int(s % ncols))




# ---------- PART 2:

nrows = 10
ncols = 10
moveobstacles = []
obstacles = []
# # # 5 agents small range
# initial = [(33,0),(80,0),(69,1),(7,0),(41,0)]
# targets = [[0,9],[69,95],[99,11],[20,39],[60,69]]
# public_targets = [[0,9],[55,95],[99,11],[20,39],[60,69]]
# obs_range = 4

# # # 6 agents small range
# initial = [(33,0),(41,0),(7,0),(80,0),(69,1),(92,0)]
# targets = [[0,9],[60,69],[20,39],[69,95],[99,11],[9,91]]
# public_targets = [[0,9],[60,69],[20,39],[55,95],[99,11],[9,91]]
# obs_range = 2

# # # 8 agents small range
# initial = [(50,0),(43,0),(75,0),(88,0),(13,0),(37,0),(57,0),(73,0)]
# targets = [[0,90],[3,93],[5,95],[98,8],[11,19],[31,39],[51,59],[55,71]]
# public_targets = [[0,90],[3,93],[5,95],[98,8],[11,19],[31,39],[51,59],[79,71]]
# obs_range = 2

# #4 agents larger range
obs_range = 3

# #4 agents big range
# initial = [(33,0),(41,0),(7,0),(80,0)]
# targets = [[0,9],[60,69],[20,39],[69,95]]
# public_targets = [[0,9],[60,69],[20,39],[55,95]]
# obs_range = 4

# con_dict = con_ar = con_init()
# bel_lines = belief_chart_init()
ax_ar = grid_init(nrows, ncols, obs_range)
# update_all(50)
# texfig.savefig("test")
# update()
# plt.show()
# ani = FuncAnimation(fig, update_all, frames=frames, interval=1000, blit=True,repeat=False)
# plt.show()
texfig.savefig("case_environment_5")
# ani.save('decen.gif',dpi=80,writer='imagemagick')


# fig = plt.figure(figsize=(4,4))
# ax = fig.add_subplot(111, projection='polar')
# ax.set_ylim(0,100)
#
# data = np.random.rand(50)*6+2
# theta = np.linspace(0,2.*np.pi, num=50)
# l,  = ax.plot([],[])
#
# def update(i):
#     global data
#     data += (np.random.rand(50)+np.cos(i*2.*np.pi/50.))*2
#     data[-1] = data[0]
#     l.set_data(theta, data )
#     return l,
#
# ani = FuncAnimation(fig, update, frames=50, interval=200, blit=True)
# plt.show()