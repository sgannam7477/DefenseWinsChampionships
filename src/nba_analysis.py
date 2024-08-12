import matplotlib.pyplot as plt
import pandas
import seaborn as sns
from scipy import stats

# Creates two dfs for 2024 Advanced Stats and 2024 Playoff Advanced Stats
# Performs the appropriate calculations to create additional values not
# found in the csv files that are needed for data analysis

advanced_24 = pandas.read_csv('NBA/2023-2024 NBA Advanced Ratings.csv')
advanced_24 = advanced_24[0:len(advanced_24) - 1]

filter_advanced_24 = advanced_24[['Team', 'W', 'L', 'PW', 'MOV', 'SRS', 'ORtg', 'DRtg', 'NRtg']]
filter_advanced_24["RS_Win_Percentage"] = filter_advanced_24['W'] / (filter_advanced_24['W'] + filter_advanced_24['L'])
filter_advanced_24['Year'] = 2024
filter_advanced_24['Team'] = filter_advanced_24['Team'].str.strip('*')

filter_advanced_24['ORtg_Z_Score'] = stats.zscore(filter_advanced_24['ORtg'])
filter_advanced_24['DRtg_Z_Score'] = -1 * stats.zscore(filter_advanced_24['DRtg'])
filter_advanced_24['Comparative_Rating'] = filter_advanced_24['ORtg_Z_Score'] - filter_advanced_24['DRtg_Z_Score']
filter_advanced_24['Wins_Over_Expected'] = filter_advanced_24['W'] - filter_advanced_24['PW']

playoffs_24 = pandas.read_csv('NBA/2023-2024 NBA Playoff Advanced Ratings.csv')
playoffs_24 = playoffs_24[0:len(playoffs_24) - 1]

filter_playoffs_24 = playoffs_24[['Tm', 'W', 'L', 'PW', 'ORtg', 'DRtg', 'NRtg']]
filter_playoffs_24["PS_Win_Percentage"] = filter_playoffs_24['W'] / (filter_playoffs_24['W'] + filter_playoffs_24['L'])
filter_playoffs_24['Year'] = 2024

filter_playoffs_24['ORtg_Z_Score'] = stats.zscore(filter_playoffs_24['ORtg'])
filter_playoffs_24['DRtg_Z_Score'] = -1 * stats.zscore(filter_playoffs_24['DRtg'])
filter_playoffs_24['Comparative_Rating'] = filter_playoffs_24['ORtg_Z_Score'] - filter_playoffs_24['DRtg_Z_Score']
filter_playoffs_24['Wins_Over_Expected'] = filter_playoffs_24['W'] - filter_playoffs_24['PW']


for x in range(1951, 2024):

    # Creates regular season and playoff dfs for each year and appends these dfs
    # to their respective 2024 dfs, making the 2024 dfs the master dataframes with
    # all historical information

    file = "NBA/" + str(x - 1) + "-" + str(x) + " NBA Advanced Ratings.csv"
    season_ratings = pandas.read_csv(file)
    season_ratings = season_ratings[:len(season_ratings) - 1]

    filtered_ratings = season_ratings[['Team', 'W', 'L', 'PW', 'MOV', 'SRS', 'ORtg', 'DRtg', 'NRtg']]
    filtered_ratings["RS_Win_Percentage"] = filtered_ratings['W'] / (filtered_ratings['W'] + filtered_ratings['L'])
    filtered_ratings['Year'] = x
    filtered_ratings['Team'] = filtered_ratings['Team'].str.strip('*')

    filtered_ratings['ORtg_Z_Score'] = stats.zscore(filtered_ratings['ORtg'])
    filtered_ratings['DRtg_Z_Score'] = -1 * stats.zscore(filtered_ratings['DRtg'])
    filtered_ratings['Comparative_Rating'] = filtered_ratings['ORtg_Z_Score'] - filtered_ratings['DRtg_Z_Score']
    filtered_ratings['Wins_Over_Expected'] = filtered_ratings['W'] - filtered_ratings['PW']

    filter_advanced_24 = pandas.concat([filter_advanced_24, filtered_ratings], ignore_index=True)

    playoff_file = "NBA/" + str(x - 1) + "-" + str(x) + " NBA Playoff Advanced Ratings.csv"
    playoff_rating = pandas.read_csv(playoff_file)
    playoff_rating = playoff_rating[:len(playoff_rating) - 1]

    # Necessary since in some seasons playoff data basketball reference stores the
    # team value in different columns

    if 'Team' in playoff_rating.columns:
        team = 'Team'
    else:
        team = 'Tm'

    filtered_playoff_rating = playoff_rating[[team, 'W', 'L', 'PW', 'ORtg', 'DRtg', 'NRtg']]
    filtered_playoff_rating["PS_Win_Percentage"] = filtered_playoff_rating['W'] / (filtered_playoff_rating['W'] + filtered_playoff_rating['L'])
    filtered_playoff_rating['Year'] = x

    filtered_playoff_rating['ORtg_Z_Score'] = stats.zscore(filtered_playoff_rating['ORtg'])
    filtered_playoff_rating['DRtg_Z_Score'] = -1 * stats.zscore(filtered_playoff_rating['DRtg'])
    filtered_playoff_rating['Comparative_Rating'] = filtered_playoff_rating['ORtg_Z_Score'] - filtered_playoff_rating['DRtg_Z_Score']
    filtered_playoff_rating['Wins_Over_Expected'] = filtered_playoff_rating['W'] - filtered_playoff_rating['PW']

    filter_playoffs_24 = pandas.concat([filter_playoffs_24, filtered_playoff_rating], ignore_index=True)

# Creates df for every NBA Champion and merging with regular season ratings df

champions = pandas.read_csv('NBA/NBA champions.csv')
champions = champions[champions['Lg'] == 'NBA']
champions['Year'] = champions['Year'].astype('int')
champions['Team'] = champions['Champion']
champions = champions[['Year', 'Team']]

champions_df = pandas.merge(champions, filter_advanced_24, how = 'left', on = ['Year', 'Team'])
champions_df_bool = pandas.notnull(champions_df['Team'])
champions_df = champions_df[champions_df_bool]

# Repeats process but with every NBA Runner-Up

runner_up = pandas.read_csv('NBA/NBA champions.csv')
runner_up = runner_up[runner_up['Lg'] == 'NBA']
runner_up['Year'] = runner_up['Year'].astype('int')
runner_up['Team'] = runner_up['Runner-Up']
runner_up = runner_up[['Year', 'Team']]

runner_df = pandas.merge(runner_up, filter_advanced_24, how = 'left', on = ['Year', 'Team'])
runner_df_bool = pandas.notnull(runner_df['Team'])
runner_df = runner_df[runner_df_bool]

# Set plt default size to fit all graphs

plt.rcParams['figure.figsize'] = [8, 6]

# Histogram of Comparative Regular Season Rating vs Count of NBA Champion

sns.histplot(champions_df, x = 'Comparative_Rating', color = 'green', binwidth = .25, kde = True)
plt.xlabel('Comparative Rating (ORtg Z Score - DRtg Z Score)')
plt.ylabel('Number of Champions')
plt.title("Regular Season Comparative Rating of NBA Champions")
plt.savefig("figures/champions_comp_rating.png", format='png')
plt.show()

# Histogram of Comparative Regular Season Rating vs Count of NBA Runner-Ups

sns.histplot(runner_df, x = 'Comparative_Rating', color = 'green', binwidth = .25, kde = True)
plt.xlabel('Comparative Rating (ORtg Z Score - DRtg Z Score)')
plt.ylabel('Number of Runner-Ups')
plt.title("Regular Season Comparative Rating of NBA Runner-Ups")
plt.savefig("figures/runners_comp_rating.png", format='png')
plt.show()

pre_three_point = filter_advanced_24[filter_advanced_24['Year'] < 1979]
post_three_point = filter_advanced_24[filter_advanced_24['Year'] >= 1979]

# Scatterplot of RS Win Percentage vs Comparative Ratings over NBA History

sns.lmplot(x = 'Comparative_Rating', y = 'RS_Win_Percentage', data = filter_advanced_24, height=6, aspect=8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Regular Season Win Percentage")
plt.title("RS Win Percentage vs Comparative Rating over NBA History")
plt.subplots_adjust(top = .9)
plt.savefig("figures/overall_rs_comp_rating.png", format='png')
plt.show()

# Scatterplot of RS Win Percentage vs Comparative Ratings prior to the Introduction of the 3-Point Line

sns.lmplot(x = 'Comparative_Rating', y = 'RS_Win_Percentage', data = pre_three_point, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Regular Season Win Percentage")
plt.title("RS Win Percentage vs Comparative Rating Before the 3-Point Line was Introduced")
plt.subplots_adjust(top = .9)
plt.savefig("figures/rs_comp_rating_pre_three.png", format='png')
plt.show()

# Scatterplot of RS Win Percentage vs Comparative Ratings after the Introduction of the 3-Point Line

sns.lmplot(x = 'Comparative_Rating', y = 'RS_Win_Percentage', data = post_three_point, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Regular Season Win Percentage")
plt.title("RS Win Percentage vs Comparative Rating After the 3-Point Line was Introduced")
plt.subplots_adjust(top = .9)
plt.savefig("figures/rs_comp_rating_post_three.png", format='png')
plt.show()

# Scatterplot of Wins Above Expected (Wins - Potential Wins) vs Comparative Rating over NBA History

sns.lmplot(x = "Comparative_Rating", y = "Wins_Over_Expected", data=filter_advanced_24, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Wins Above Expected")
plt.title("Wins Above Expected vs Comparative Rating over NBA History")
plt.subplots_adjust(top = .9)
plt.savefig("figures/overall_woe_comp_rating.png", format='png')
plt.show()

# Scatterplot of Wins Above Expected vs Comparative Rating before the 3-Point Line

sns.lmplot(x = "Comparative_Rating", y = "Wins_Over_Expected", data=pre_three_point, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Wins Above Expected")
plt.title("Wins Above Expected vs Comparative Rating Before the 3-Point Line was Introduced")
plt.subplots_adjust(top = .9)
plt.savefig("figures/woe_comp_rating_pre_three.png", format='png')
plt.show()

# Scatterplot of Wins Above Expected vs Comparative Rating after the 3-Point Line

sns.lmplot(x = "Comparative_Rating", y = "Wins_Over_Expected", data=post_three_point, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Wins Above Expected")
plt.title("Wins Above Expected vs Comparative Rating After the 3-Point Line was Introduced")
plt.subplots_adjust(top = .9)
plt.savefig("figures/woe_comp_rating_post_three.png", format='png')
plt.show()

pre_three_playoffs = filter_playoffs_24[filter_playoffs_24['Year'] < 1979]
post_three_playoffs = filter_playoffs_24[filter_playoffs_24['Year'] >= 1979]

# Scatterplot of PS Win Percentage vs Comparative Ratings over NBA History

sns.lmplot(x = 'Comparative_Rating', y = 'PS_Win_Percentage', data = filter_playoffs_24, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Post Season Win Percentage")
plt.title("PS Win Percentage vs Comparative Rating over NBA History")
plt.subplots_adjust(top = .9)
plt.savefig("figures/overall_ps_comp_rating.png", format='png')
plt.show()

# Scatterplot of PS Win Percentage vs Comparative Ratings prior to the Introduction of the 3-Point Line

sns.lmplot(x = 'Comparative_Rating', y = 'PS_Win_Percentage', data=pre_three_playoffs, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Post Season Win Percentage")
plt.title("PS Win Percentage vs Comparative Rating Before Three-Point Line Introduced")
plt.subplots_adjust(top = .9)
plt.savefig("figures/ps_comp_rating_pre_three.png", format='png')
plt.show()

# Scatterplot of PS Win Percentage vs Comparative Ratings after the Introduction of the 3-Point Line

sns.lmplot(x = 'Comparative_Rating', y = 'PS_Win_Percentage', data = post_three_playoffs, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Post Season Win Percentage")
plt.title("PS Win Percentage vs Comparative Rating After Three-Point Line Introduced")
plt.subplots_adjust(top = .9)
plt.savefig("figures/ps_comp_rating_post_three.png", format='png')
plt.show()

# Scatterplot of PS Wins Above Expected (Wins - Potential Wins) vs Comparative Rating over NBA History

sns.lmplot(x = 'Comparative_Rating', y = 'Wins_Over_Expected', data = filter_playoffs_24, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Wins Over Expected")
plt.title("Post Season Wins Over Expected vs Comparative Rating over NBA History")
plt.subplots_adjust(top = .9)
plt.savefig("figures/overall_ps_woe_comp_rat.png", format='png')
plt.show()

# Scatterplot of PS Wins Above Expected vs Comparative Rating before the 3-Point Line

sns.lmplot(x = 'Comparative_Rating', y = 'Wins_Over_Expected', data = pre_three_playoffs, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Wins Over Expected")
plt.title("Post Season Wins Over Expected vs Comparative Rating Before Three-Point Line Introduced")
plt.subplots_adjust(top = .9)
plt.savefig("figures/ps_woe_comp_rat_pre_three.png", format='png')
plt.show()

# Scatterplot of PS Wins Above Expected vs Comparative Rating after the 3-Point Line

sns.lmplot(x = 'Comparative_Rating', y = 'Wins_Over_Expected', data = post_three_playoffs, height = 6, aspect = 8/6)
plt.xlabel("Comparative Rating (ORTG Z Score - DRTG Z Score)")
plt.ylabel("Wins Over Expected")
plt.title("Post Season Wins Over Expected vs Comparative Rating After Three-Point Line Introduced")
plt.subplots_adjust(top = .9)
plt.savefig("figures/ps_woe_comp_rat_post_three.png", format='png')
plt.show()

# Calculates the difference in RS comparative rating between each year's champion and runner-up

difference_df = pandas.merge(champions_df, runner_df, how = 'inner', on = 'Year')
difference_df.rename(columns = {'Comparative_Rating_x': 'Champion_Rating', 'Comparative_Rating_y': 'Runner-Up_Rating'}, inplace=True)
difference_df = difference_df[['Year', 'Champion_Rating', 'Runner-Up_Rating']]
difference_df.dropna(subset = ['Champion_Rating', 'Runner-Up_Rating'], inplace=True)
difference_df['Diff_Comp_Rating'] = difference_df['Champion_Rating'] - difference_df['Runner-Up_Rating']

# Lineplot of RS Comparative Rating of Each Finalist Every Season
sns.lineplot(x = 'Year', y = 'Champion_Rating', data = difference_df, label = "Champion", color = 'green')
sns.lineplot(x = 'Year', y = 'Runner-Up_Rating', data = difference_df, label = 'Runner-Up', color = 'grey')
plt.ylabel('Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.title("RS Comparative Rating of Champions and Runner Ups Each Season")
plt.savefig("figures/rs_comp_rating_of_finalists.png", format='png')
plt.show()

# Lineplot of the RS Difference in Comparative Rating of Each Finalist Every Season

sns.lineplot(x = 'Year', y = 'Diff_Comp_Rating', data = difference_df, label = 'Difference', color = 'black')
plt.ylabel('Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.title('Champions vs Runner Ups Difference In RS Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.savefig("figures/rs_comp_rating_dif_each_finalist_line.png", format='png')
plt.show()

# Boxplot of the RS Difference in Comparative Rating of Each Finalist Every Season

sns.boxplot(data = difference_df, x = 'Diff_Comp_Rating')
plt.xlabel('Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.title('RS Champions vs Runner Ups Difference In Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.savefig("figures/rs_comp_rating_dif_each_finalist_box.png", format='png')
plt.show()

# Pivot longer
difference_df = pandas.melt(difference_df, id_vars=['Year'], value_vars=['Champion_Rating', 'Runner-Up_Rating'], var_name = 'Result', value_name = 'Comparative_Rating')
difference_df['Result'] = difference_df['Result'].str.replace('_Rating', '')

# Boxplots of the RS Comparative Rating of Each Finalist
sns.boxplot(data = difference_df, x = 'Result', y = 'Comparative_Rating', hue = 'Result')
plt.ylabel('Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.title('RS Comparative Rating of NBA Finalists')
plt.savefig("figures/rs_comp_rating_each_finalist_box.png", format='png')
plt.show()

# Create dfs for playoff data of champions and runners ups

champions_playoff_df = pandas.merge(champions, filter_playoffs_24, how = 'left', on = ['Year', 'Team'])
champions_playoff_df_bool = pandas.notnull(champions_playoff_df['Team'])
champions_playoff_df = champions_playoff_df[champions_playoff_df_bool]

runners_playoff_df = pandas.merge(runner_up, filter_playoffs_24, how = 'left', on = ['Year', 'Team'])
runners_playoff_df_bool = pandas.notnull(runners_playoff_df['Team'])
runners_playoff_df = runners_playoff_df[runners_playoff_df_bool]

# Histogram of Comparative Post Season Rating vs Count of NBA Champion

sns.histplot(champions_playoff_df, x = 'Comparative_Rating', color = 'green', binwidth = .25, kde = True)
plt.xlabel('Comparative Rating (ORtg Z Score - DRtg Z Score)')
plt.ylabel('Number of Champions')
plt.title("Post Season Comparative Rating of NBA Champions")
plt.savefig("figures/hist_comp_ps_rating_champion.png", format='png')
plt.show()

# Histogram of Comparative Post Season Rating vs Count of NBA Runner-Ups

sns.histplot(runners_playoff_df, x = 'Comparative_Rating', color = 'green', binwidth = .25, kde = True)
plt.xlabel('Comparative Rating (ORtg Z Score - DRtg Z Score)')
plt.ylabel('Number of Runner-Ups')
plt.title("Post Season Comparative Rating of NBA Runner-Ups")
plt.savefig("figures/hist_comp_ps_rating_runner.png", format='png')
plt.show()

# Calculates the difference in PS comparative rating between each year's champion and runner-up

difference_playoff_df = pandas.merge(champions_playoff_df, runners_playoff_df, how = 'inner', on = 'Year')
difference_playoff_df.rename(columns = {'Comparative_Rating_x': 'Champion_Rating', 'Comparative_Rating_y': 'Runner-Up_Rating'}, inplace=True)
difference_playoff_df = difference_playoff_df[['Year', 'Champion_Rating', 'Runner-Up_Rating']]
difference_playoff_df.dropna(subset = ['Champion_Rating', 'Runner-Up_Rating'], inplace=True)
difference_playoff_df['Diff_Comp_Rating'] = difference_playoff_df['Champion_Rating'] - difference_playoff_df['Runner-Up_Rating']

# Lineplot of PS Comparative Rating of Each Finalist Every Season

sns.lineplot(x = 'Year', y = 'Champion_Rating', data = difference_playoff_df, label = "Champion", color = 'green')
sns.lineplot(x = 'Year', y = 'Runner-Up_Rating', data = difference_playoff_df, label = 'Runner-Up', color = 'grey')
plt.ylabel('Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.title("PS Comparative Rating of Champions and Runner Ups Each Season")
plt.savefig("figures/line_ps_comp_rating_finalist.png", format='png')
plt.show()

# Lineplot of the PS Difference in Comparative Rating of Each Finalist Every Season

sns.lineplot(x = 'Year', y = 'Diff_Comp_Rating', data = difference_playoff_df, label = 'Difference', color = 'black')
plt.ylabel('Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.title('Champions vs Runner Ups Difference In PS Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.savefig("figures/line_ps_diff_comp_rating_finalist.png", format='png')
plt.show()

# Boxplot of the PS Difference in Comparative Rating of Each Finalist Every Season

sns.boxplot(data = difference_playoff_df, x = 'Diff_Comp_Rating')
plt.xlabel('Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.title('PS Champions vs Runner Ups Difference In Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.savefig("figures/box_ps_diff_comp_rating_finalist.png", format='png')
plt.show()

# Pivot longer
difference_playoff_df = pandas.melt(difference_playoff_df, id_vars=['Year'], value_vars=['Champion_Rating', 'Runner-Up_Rating'], var_name = 'Result', value_name = 'Comparative_Rating')
difference_playoff_df['Result'] = difference_playoff_df['Result'].str.replace('_Rating', '')

# Boxplots of the PS Comparative Rating of Each Finalist

sns.boxplot(data = difference_playoff_df, x = 'Result', y = 'Comparative_Rating', hue = 'Result')
plt.ylabel('Comparative Rating (ORTG Z Score - DRTG Z Score)')
plt.title('PS Comparative Rating of NBA Finalists')
plt.savefig("figures/box_ps_comp_rating_finalist.png", format='png')
plt.show()






