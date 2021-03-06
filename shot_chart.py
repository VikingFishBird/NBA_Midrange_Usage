from nba_api.stats.endpoints import shotchartdetail
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import seaborn as sns

mpl.rcParams['figure.figsize'] = (12, 5)
plt.style.use('ggplot')

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

YEAR = '2019-20'
HOU_19_20_ID = 1610612745
SAS_19_20_ID = 1610612759
TUCKER_ID=200782

houston = (
    shotchartdetail.ShotChartDetail(team_id=HOU_19_20_ID, player_id=0)
        .get_data_frames()[0]
        .get(['PLAYER_NAME', 'LOC_X', 'LOC_Y', 'SHOT_DISTANCE'])
)

san_antonio = (
    shotchartdetail.ShotChartDetail(team_id=SAS_19_20_ID, player_id=0)
        .get_data_frames()[0]
        .get(['PLAYER_NAME', 'LOC_X', 'LOC_Y', 'SHOT_DISTANCE'])
)

# Shot Histograms
bins = np.arange(0, 31, 1)

houston.plot(kind='hist', y='SHOT_DISTANCE', bins=bins, color=(206/255, 17/255, 65/255))
plt.title('Houston FGA {}'.format(YEAR), fontname='DejaVu Sans', fontsize=18)
plt.xlabel('Distance', fontname='DejaVu Sans', fontsize=14)
plt.xticks(bins)

san_antonio.plot(kind='hist', y='SHOT_DISTANCE', bins=bins, color='black')
plt.title('San Antonio FGA {}'.format(YEAR), fontname='DejaVu Sans', fontsize=18)
plt.xlabel('Distance', fontname='DejaVu Sans', fontsize=14)
plt.xticks(bins)
# endregion

cmap = plt.cm.get_cmap('viridis')
# region Houston Heatmap
houston_jumpshots = houston[houston.get('SHOT_DISTANCE') >= 8]

joint_shot_chart = sns.jointplot(x=houston_jumpshots.LOC_X, y=houston_jumpshots.LOC_Y,
                                 kind='kde', space=0, color=cmap(0.1),
                                 cmap=cmap, n_levels=50, fill=True)

joint_shot_chart.fig.set_size_inches(12, 11)

ax = joint_shot_chart.ax_joint
draw_court(ax)

ax.set_xlim(-250,250)
ax.set_ylim(422.5, -47.5)

ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(labelbottom='off', labelleft='off')
ax.set_title('Houston Jumpshot FGA {}'.format(YEAR),
             y=1.2, fontsize=18)
# endregion

# region Houston Heatmap
san_antonio_jumpshots = san_antonio[san_antonio.get('SHOT_DISTANCE') >= 8]

joint_shot_chart = sns.jointplot(x=san_antonio_jumpshots.LOC_X, y=san_antonio_jumpshots.LOC_Y,
                                 kind='kde', space=0, color=cmap(0.1),
                                 cmap=cmap, n_levels=50, fill=True)

joint_shot_chart.fig.set_size_inches(12, 11)

ax = joint_shot_chart.ax_joint
draw_court(ax)

ax.set_xlim(-250,250)
ax.set_ylim(422.5, -47.5)

ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(labelbottom='off', labelleft='off')
ax.set_title('San Antonio Jumpshot FGA {}'.format(YEAR),
             y=1.2, fontsize=18)
# endregion


plt.show()
