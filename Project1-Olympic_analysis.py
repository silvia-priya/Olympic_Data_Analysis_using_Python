#Program to enter multiple values into the table

import matplotlib.pyplot as plt
import pymysql,pandas as pd

connect=pymysql.connect(user='root',password='silvia',db='silvia')

try:

    with connect.cursor() as cursor:
        sql1= "select * from olympic"
        cursor.execute(sql1)
        connect.commit()
        #To view the records which are inserted from teh pgm itself, we need to run a select qry here
        rows=cursor.fetchall()
        print(rows)
        name_col=[]
        age_col=[]
        country_col=[]
        year_col=[]
        dates_col=[]
        sports_col=[]
        gold_col=[]
        silver_col=[]
        bronze_col=[]
        total_col=[]

        for row in rows:
            #print(row)
            name,age,country,year,dates,sports,gold,silver,bronze,total=row
            name_col.append(name)
            age_col.append(age)
            country_col.append(country)
            year_col.append(year)
            dates_col.append(dates)
            sports_col.append(sports)
            gold_col.append(gold)
            silver_col.append(silver)
            bronze_col.append(bronze)
            total_col.append(total)



        proj_dataframe=pd.DataFrame() #Creating an empty dataframe
        proj_dataframe['name']=name_col #Converting the list of all cols into cols in dataframe
        proj_dataframe['age']=age_col
        proj_dataframe['country'] = country_col
        proj_dataframe['year'] = year_col
        proj_dataframe['dates'] = dates_col
        proj_dataframe['sports'] = sports_col
        proj_dataframe['gold'] = gold_col
        proj_dataframe['silver'] = silver_col
        proj_dataframe['bronze'] = bronze_col
        proj_dataframe['total'] = total_col
        print(proj_dataframe)
        proj_dataframe=proj_dataframe.set_index('name') #Changing the index col of dataframe
        print("dataframe with name",proj_dataframe)

        #Find the total medals  won by every country
        tot_medals=proj_dataframe.groupby(['country'])[['total']].sum()
        print("total medals won by every country",tot_medals)

        #Rank the people based on the total medals obtained and give me the names of top10

        top_10_medals=proj_dataframe.groupby(['name'])[['total']].sum().head(10)
        print("Top 10 medal winners",top_10_medals)

        #Find out the country which won more medals on the year 2000
        year_2000=proj_dataframe[proj_dataframe.year==2000]
        ratings_2000=year_2000.groupby(['country'])[['total']].sum()
        ratings_2000=ratings_2000.groupby(['country'])[['total']].sum()
        print("In 2000 the below countries won more medals",ratings_2000.sort_values(by='total',ascending=False))


        #find out the top 3 country which won the maximum combo of gold,silver and bronze medals
        g_s_b_medals=proj_dataframe.groupby(['country'])[['bronze','silver','gold']]
        print(g_s_b_medals.max().sort_values(by=['bronze','silver','gold'],ascending=False).head(3))


        #Find out the age group, which grabs most number of gold medals in olympic
        age_grp_medals=proj_dataframe.groupby(['age'])[['gold']].max().sort_values(by=['gold'],ascending=False)
        print("The age group which grabs more number of gold medals",age_grp_medals)

        #plot a graph with year and number of medals for USA
        usa_medals=proj_dataframe[(proj_dataframe.country=='United States') & (proj_dataframe.sports=='Swimming')]
        x_axis=usa_medals['year']
        y_axis=usa_medals['total']
        plt.title('USA Medals graph year wise for swimming')
        plt.xlabel('years')
        plt.ylabel('No.of medals')
        plt.bar(x_axis,y_axis)
        plt.show()

finally:
    cursor.close()
