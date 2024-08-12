# Data Analysis Project: Defense Wins Championships

## Overview

My initiative for this project was to investigate the validity of arguably the most prevalent claim
in all of sports: "Defense Wins Championships". Specifically, the National Basketball Association, 
or NBA, was tested to see whether rosters more proficient defensively were more capable of winning, both in
terms of regular season success and post season success, compared to teams more proficient offensively. All data
was scraped from basketball reference's advanced stats and playoff advanced stats web pages, which were saved
in csv files located in the NBA folder. From these csv files, pandas dataframes were created to store and manipulate
the recorded data which were then plotted as graphs using seaborn.

## Methodology

Using the beautiful soup library, NBA Advanced Team Statistics, NBA Playoff Advanced Team Statistic, and NBA
finals results dating back to the 1950-1951 NBA Season were scraped from various basketball reference webpages
before being saved in csv files within the NBA folder. From this data, the advanced stats portfolio of every
NBA team along with the playoff advanced stats portfolio of every NBA playoff team were stored in a pandas 
database. From this data, two metrics were created for use in this data analysis project.

**Comparative Rating**

Comparative Rating was the measurement I created to assess a team's relative proficiency in either the
offensive or defensive side of the ball. Teams with with a higher magnitude of this metric are ones who are
far superior on one side of the ball or the other, whereas teams with a positive comparative rating are ones
who are better offensively than defensively, whereas a negative comparative rating indicates that they are
more superior defensively than offensively. This metric is the difference between the z-score of the offensive
rating of a team for that season and the z-score of the defensive rating of a team for that season. Offensive 
rating and defensive rating are provided measurements from basketball reference that are the industry standard
in reflecting a team's proficiency on each side of the court. Offensive rating is the average point's score per
100 offensive possessions, whereas defensive rating is the average point's allowed per 100 defensive possessions.

**Wins Over Expected**

Wins Over Expected was another measurement I created to assess a team's ability to overperform or underperform
their expected win record based on their advanced stats, with a positive WOE reflecting an overperforming team, 
whereas a negative WOE reflects an underperforming team. This metric is calculated by finding the difference
between the win count of a team and the pythagorean win count of a team. Pythagorean wins are a statistical
model used by NBA general managers, that predicts a team's win count based on their points scored and points
allowed. For more information on pythagorean wins: https://en.wikipedia.org/wiki/Pythagorean_expectation#Use_in_basketball


## Findings

I began my study by first analyzing the comparative ratings of both champions and runner-ups, 
creating histograms for both types of teams.
![image](https://github.com/user-attachments/assets/58b176d6-326d-4fe4-aac0-7d59dbd03e2d)
![image](https://github.com/user-attachments/assets/ce0e7076-67c8-4455-9f86-ae6483799e7e)
From this, although we can see that both offensively proficiency and defensively proficient
teams were capable of deep post-season runs, these teams tended to be more offensively-minded
in the regular season, although this trend was much more noticeable with runner-ups than
champions.

I then took a look at the regular season win percentages of all teams against their comparative rating,
analyzing both the complete picture as well as dividing the data before and after 1978, the year the
three-point line was introduced, to see if this major addition to this store impacted the trends in anyway.

![image](https://github.com/user-attachments/assets/bf7c458c-7cdc-4b3e-90d3-679d4f5867f6)
![image](https://github.com/user-attachments/assets/da647ec8-853b-466e-88df-5a71aed78b30)
![image](https://github.com/user-attachments/assets/0abdaa8a-ad6e-4976-a4d7-d15156aad500)

Overall, across the entirety of NBA history, there isn't much of a trend between comparative rating
and regular season win percentage, but when we look at the divided data a different story emerges.
While there are many outliers to both trends, there is a negative association between comparative rating and win percentage,
indicating teams with greater defensive proficiency compared to offensive proficiency won more games.
However, this flips around in the post-three point line era, where, along with a much larger dataset,
there is a slightly positive association, where superior offensive teams are more likely to
have a greater win percentage. Thus, it appears that a strong defensive team led to greater
success in the past, but after the implementation of the three-point line, which offers offenses
more points per possession, a superior offense was the means for a better team.

The next set of graphs I looked at were an attempt to see if a high mangitude of comparative
rating was conducive to a team overperforming or underperforming their expected win totals. Once again,
I made sure to divide the data by the introduction of the three-point line to see if it altered
the trend in anyway. However, from all three graphs no association could be found, thus no conclusions
could be made.

![image](https://github.com/user-attachments/assets/8d5e1ab5-567f-497c-bed7-98ce6badc532)
![image](https://github.com/user-attachments/assets/78bfebd5-5fbb-4ca6-ac93-6074d78ff4af)
![image](https://github.com/user-attachments/assets/6745d13c-bcc1-4b61-95bf-8cbce4a43db0)

I then repeated the same proccesses with playoff data, to see the affect of a team's
comparative rating on their performance in a playoff environment, where championships are earned.

![image](https://github.com/user-attachments/assets/3585dbaa-a234-466c-9e0f-af106ade9568)
![image](https://github.com/user-attachments/assets/146b6617-9201-49c6-8f77-583ee7dadd1b)
![image](https://github.com/user-attachments/assets/9585771c-1dba-4fe9-96a4-838cca962c73)

Dividing the data once again by the three-point line, it can be seen that, independent of era,
there is a slight but non-marginal negative association between a team's comparative rating and
their post-season win-percentage. Although there are plenty of instances where the contrary is true,
it seems that when teams hold defensive superiority in terms of their playoff comparative rating, they have a
higher likelihood of having a higher post season win percentage.

![image](https://github.com/user-attachments/assets/295b8287-95ec-49e0-8882-04f43330f518)
![image](https://github.com/user-attachments/assets/a1e9ca68-90e9-4b5a-ba8e-bcef17387a32)
![image](https://github.com/user-attachments/assets/4288a18c-5196-48a7-9070-c98d730c9d26)

As for the relation between post-season Wins Over Expected and a team's comparative rating, it appears
that once again there isn't much of a relation between the two factors.

Following this analysis, I then moved towards focusing on analyzing the ratings of team's that
made deep playoff runs, specifically the champions and runner-ups.

![image](https://github.com/user-attachments/assets/ed72ac25-d7a1-4f10-9a2d-3bafe66fcb2c)
![image](https://github.com/user-attachments/assets/bd7af847-6f53-49f6-b8fe-950c54132ea0)

This first graph shows the regular season comparative rating of each champions and runner-up, while
the second graph shows the difference in comparative rating between the two. The biggest takeaway
from these two graphs are that although both more offensive and more defensive teams have both
won championships, there are two stretches in particular, one during the 1960s and the other during
the mid-2010's, where for many consecutive years, defensively superior teams won the championship.
The 60's stretch corresponds to the Celtics dynasty, who during the period were renowned for their all-time
caliber defense which offset a talented but unnoteworthy offense. 

![image](https://github.com/user-attachments/assets/1307fcc5-88b6-44c3-bdae-fcf42d3e55c4)
![image](https://github.com/user-attachments/assets/005aff47-3c11-43d8-be6f-27c33a7c29f2)

From these next two box plots, it can be seen how NBA Champions tended to be more defensively oriented
in comparison to their runner-up counterparts, with the median difference in comparative ratings being
a negative value, indicating superior defensive teams.

![image](https://github.com/user-attachments/assets/1a22bb8a-3b63-431c-a3d7-d6d8ebaec747)
![image](https://github.com/user-attachments/assets/143e2b8c-727d-4691-a222-199f8440bb4d)

These next two graphs are histograms for the post-season comparative rating of NBA Champions and NBA
Runner-Ups, and the biggest finding from these graphs are that NBA Champions, are much more frequently defensively
oriented, in comparison to runner-ups who show more of tendency to be offensive favoring.

![image](https://github.com/user-attachments/assets/7425e931-f489-4daf-a467-2998211f1908)
![image](https://github.com/user-attachments/assets/9cbd327b-dbda-4ed1-ad06-fcbd59ba715a)
![image](https://github.com/user-attachments/assets/50271427-9c52-431d-a725-d70475332638)
![image](https://github.com/user-attachments/assets/4fd3c95a-f9b4-48dc-a749-55c1c286da36)

These last four graphs perform a similar assessment as was done earlier, instead using post-season comparative rating.
From these graphs, while there are outliers to the trend, there is a tendency for champions to have
a more defensively oriented post-season performance compared to the runner-ups.

## Takeaways

- In terms of regular season success, especially after the introduction of the three-point line, offensively oriented teams tend to have a greater regular season win percentage
- In terms of post season success, as is best exemplified in the comparison between champions and runner-ups, defensively oriented teams have greater success than offensively oriented teams
- There is evidence to presume that the saying "defense wins championships" has validity, although there are outliers in the data that shows that it is not certainly the only factor that leads to success
