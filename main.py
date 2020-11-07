import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import teamestimatedmetrics as team_advanced_stats
from nba_api.stats.endpoints import leaguedashptstats as team_tracking


YEAR = '2019-20'

# Configure plot settings
mpl.rcParams['figure.figsize'] = (8, 5)
plt.style.use('ggplot')
nba_colors_rgb = {
    'Atlanta Hawks': (225, 68, 52),             # ATL
    'Boston Celtics': (0, 122, 51),             # BOS
    'Brooklyn Nets': (0, 0, 0),                 # BRO
    'Charlotte Hornets': (29, 17, 96),          # CHA
    'Charlotte Bobcats': (29, 17, 96),          # CHA
    'Chicago Bulls': (206, 17, 65),             # CHI
    'Cleveland Cavaliers': (134, 0, 56),        # CLE
    'Dallas Mavericks': (0, 83, 188),           # DAL
    'Denver Nuggets': (13, 34, 64),             # DEN
    'Detroit Pistons': (200, 16, 46),           # DET
    'Golden State Warriors': (29, 66, 138),     # GSW
    'Houston Rockets': (206, 17, 65),           # HOU
    'Indiana Pacers': (0, 45, 98),              # IND
    'LA Clippers': (200, 16, 46),               # LAC
    'Los Angeles Clippers': (200, 16, 46),      # LAC
    'Los Angeles Lakers': (85, 37, 130),        # LAL
    'Memphis Grizzlies': (93, 118, 169),        # MEM
    'Miami Heat': (152, 0, 46),                 # MIA
    'Milwaukee Bucks': (0, 71, 27),             # MIL
    'Minnesota Timberwolves': (12, 35, 64),     # MIN
    'New Orleans Pelicans': (0, 22, 65),        # NOP
    'New York Knicks': (0, 107, 182),           # NYK
    'Oklahoma City Thunder': (0, 125, 195),     # OKC
    'Orlando Magic': (0, 125, 197),             # ORL
    'Philadelphia 76ers': (0, 107, 182),        # PHI
    'Phoenix Suns': (29, 17, 96),               # PHO
    'Portland Trail Blazers': (224, 58, 62),    # POR
    'Sacramento Kings': (91, 43, 130),          # SAC
    'San Antonio Spurs': (196, 206, 211),       # SAS
    'Toronto Raptors': (206, 17, 65),           # TOR
    'Utah Jazz': (0, 43, 92),                   # UTA
    'Washington Wizards': (0, 43, 92),          # WAS
}
nba_colors_normalized = {}

# Normalize RGB values to 0-1
for key in nba_colors_rgb:
    nba_colors_normalized[key] = (nba_colors_rgb[key][0]/255, nba_colors_rgb[key][1]/255, nba_colors_rgb[key][2]/255)

# The api can't handle the multiple headers of this table
# so I manually created a csv
shot_locations = pd.read_csv('data/nba_19_20_midrange.csv')

advanced_stats = (
    team_advanced_stats
        .TeamEstimatedMetrics(season=YEAR)
        .get_data_frames()[0]
        .get(['TEAM_NAME', 'E_OFF_RATING', 'E_DEF_RATING', 'E_NET_RATING', 'E_PACE'])
)

# For team abbreviation
team_details = (
    team_tracking
        .LeagueDashPtStats(season=YEAR)
        .get_data_frames()[0]
        .get(['TEAM_NAME', 'TEAM_ABBREVIATION'])
)


merged_table = advanced_stats.merge(shot_locations, left_on='TEAM_NAME', right_on='team')
merged_table = merged_table.merge(team_details, left_on='TEAM_NAME', right_on='TEAM_NAME')
print(merged_table)

# region E_OFF_RATING vs DIST_MILES_OFF
# Label axis: E_OFF_RATING vs DIST_MILES_OFF
off_rat_vs_mid_att = merged_table.plot(x='mid_range_attempts', y='E_OFF_RATING', kind='scatter')
plt.title('Offensive Rating vs Midrange Shot Attempts ({})'.format(YEAR), fontname='DejaVu Sans', fontsize=18)
plt.xlabel('Midrange Shot Attempts', fontname='DejaVu Sans', fontsize=14)
plt.ylabel('Offensive Rating', fontname='DejaVu Sans', fontsize=14)

# Plot & color: E_OFF_RATING vs DIST_MILES_OFF
for team_id in merged_table.index:
    plt.scatter(merged_table.get('mid_range_attempts').loc[team_id],
                merged_table.get('E_OFF_RATING').loc[team_id],
                color=nba_colors_normalized[merged_table.get('TEAM_NAME').loc[team_id]])
    plt.text(merged_table.get('mid_range_attempts').loc[team_id] + 0.07,
                merged_table.get('E_OFF_RATING').loc[team_id] + 0.06,
                merged_table.get('TEAM_ABBREVIATION').loc[team_id],
                fontname='DejaVu Sans', fontsize=9)

plt.show()
