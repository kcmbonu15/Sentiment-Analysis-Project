'Kingsley Mbonu'
'Kallam, Vinod Kumar Reddy'
import json
import sys
import matplotlib.pyplot as plt
#from datetime import datetime
import numpy as np
import datetime
import csv
import re
import time
#from datetime import datetime
def read_stocktwits():
    
    with open('BAC.json') as f:
        data=f.read()
        jsondata=json.loads(data)
        #print jsondata
    result=[]
    for row_data in jsondata:
        row_date=str(row_data["created_at"]["$date"])
        row_date=int(row_date[:-3])
        #row_date = datetime.today().date()
        row_date=datetime.datetime.fromtimestamp(row_date).strftime("%Y-%m-%d %H:%M:%S")
        row_string=str(row_data["body"].encode('ascii','ignore'))
        row_string=(row_string.lower()).replace("\n","")
        string=[]
        for i in list(row_string):
            if (i.isalnum() or i.isspace()): string.append(i)
        else: string.append(' ')
        row_value=str(row_data["entities"]["sentiment"])
        if row_value=='None':
            row_value='unknown'
        else:
            row_value=row_data["entities"]["sentiment"]["basic"]
            row_value=row_value.encode('ascii','ignore')
          
        row_string=str(row_date)+","+"".join(string)+","+row_value
        result.append(row_string)
    file_name=open("BAC.csv","w")
    with file_name as values: values.write('\n'.join(result))
    file_name.close()
    return
        
def sentiment_analysis():
    pos_list = []
    neg_list = []
    with open ("positive_words.txt") as p:
        for line in p:
            pos_list.extend([elt.strip() for elt in line.split(',')])
            #pos_list.append(inner_list)
    p.close()
    with open ("negative_words.txt") as n:
        for line in n:
            neg_list.extend([elt.strip() for elt in line.split(',')])
    n.close()
    result=[]
    read=csv.reader(open('BAC.csv','r'))
    for line in read:
        pos_count = 0
        neg_count = 0
        value=line[2]
        if line[2] == 'unknown':
            read_text = []
            read_text = line[1].split()
            #print read_text
            for each_word in read_text:
                if each_word in pos_list: pos_count+=1
                if each_word in neg_list: neg_count+=1
            if pos_count > neg_count: value='Bullish'
            elif pos_count < neg_count : value='Bearish'
            else : value='Neutral'
        row_string = line[0]+','+value
        result.append(row_string) 
    file_name=open("BAC2.csv","w")
    with file_name as values: values.write('\n'.join(result))
    file_name.close()
    return
            
        
def get_sentiment_dates(start_date, end_date):
    positive_dict = {}
    negative_dict = {}
    neutral_dict = {}
    read=csv.reader(open('BAC2.csv','r'))
    start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_datetime=start_datetime.strftime("%Y-%m-%d")
    end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    end_datetime=end_datetime.strftime("%Y-%m-%d")
    

    # Creating return dictionaries with key values for each sentiment_file line
    for line in read:
        read_date = datetime.datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")
        read_date=read_date.strftime("%Y-%m-%d")
        if start_datetime <= read_date <= end_datetime:
            if line[1] == "Bullish":
                if read_date not in positive_dict:
                    positive_dict.update({read_date: 1})
                else:
                    positive_dict[read_date] += 1
            elif line[1] == "Bearish":
                if read_date not in negative_dict:
                    negative_dict.update({read_date: 1})
                else:
                    negative_dict[read_date] += 1
            else:
                if read_date not in neutral_dict:
                    neutral_dict.update({read_date: 1})
                else:
                    neutral_dict[read_date] += 1
    return [positive_dict, negative_dict, neutral_dict]

def drawing_pie(start_date, end_date):
    dict_list = get_sentiment_dates(start_date, end_date)
    pos_count, neg_count, neutral_count = 0, 0, 0

    # Counting the total number of sentiments by type
    for key in sorted(dict_list[0].keys()):
        pos_count += dict_list[0][key]
    for key in sorted(dict_list[1].keys()):
        neg_count += dict_list[1][key]
    for key in sorted(dict_list[2].keys()):
        neutral_count += dict_list[2][key]

    # Formatting data for Pie Chart
    total = float(pos_count + neg_count + neutral_count)
    positive_percent = pos_count / total * 100
    negative_percent = neg_count / total * 100
    neutral_percent = neutral_count / total * 100
    print positive_percent, negative_percent, neutral_percent
    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [positive_percent,negative_percent,neutral_percent]
    colors = ['blue', 'green', 'red']

    # Finding the greatest sentiment count to use for Plot Title
    def argmax(**kw):
        wk = {v:k for k,v in kw.items()}
        return wk[max(wk)]
    plt.title('Sentiment is ' + str(argmax(Positive=pos_count, Negative=neg_count, Neutral=neutral_count)), loc='left')

    # Plotting Data
    plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=0)
    plt.axis('equal')
    plt.show()
    return

def drawing_lines(start_date, end_date):
    dict_list = get_sentiment_dates(start_date, end_date)
    date_list = []
    positive_count = []
    negative_count = []
    neutral_count = []

    # Counting the total number of sentiments by type
    for key in sorted(dict_list[0].keys()):
        date_list.append(key)
        positive_count.append(dict_list[0][key])
    for key in sorted(dict_list[1].keys()):
        negative_count.append(dict_list[1][key])
    for key in sorted(dict_list[2].keys()):
        neutral_count.append(dict_list[2][key])
    fig,ax=plt.subplots()
    ax.set_xticklabels(date_list[0:29:5],rotation=30)
    
    # Plotting Data
    ax.plot(positive_count, 'o-', label='Positive')
    ax.plot(negative_count, 'o-', label='Negative')
    ax.plot(neutral_count, 'o-', label='Neutral')
    plt.title("Sentiment between"+start_date+" and "+end_date)
    plt.legend(loc="right")
    plt.savefig("lines_sentiment.png")
    plt.show()
    return
def main():
    read_stocktwits()# output: BAC.csv
    sentiment_analysis() # output BAC2.csv
    get_sentiment_dates('2013-01-02', '2013-01-31')#output:[{datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 44, datetime.date(2013, 1, 6): 31, datetime.date(2013, 1, 4): 63, datetime.date(2013, 1, 2): 108, datetime.date(2013, 1, 23): 41, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 25, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 11, datetime.date(2013, 1, 17): 153, datetime.date(2013, 1, 10): 75, datetime.date(2013, 1, 31): 19, datetime.date(2013, 1, 8): 66, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 6, datetime.date(2013, 1, 25): 25, datetime.date(2013, 1, 7): 79, datetime.date(2013, 1, 5): 27, datetime.date(2013, 1, 3): 60, datetime.date(2013, 1, 22): 44, datetime.date(2013, 1, 15): 45, datetime.date(2013, 1, 20): 7, datetime.date(2013, 1, 13): 14, datetime.date(2013, 1, 18): 59, datetime.date(2013, 1, 11): 52, datetime.date(2013, 1, 16): 66, datetime.date(2013, 1, 9): 137, datetime.date(2013, 1, 30): 19, datetime.date(2013, 1, 28): 23}, {datetime.date(2013, 1, 26): 3, datetime.date(2013, 1, 24): 20, datetime.date(2013, 1, 6): 5, datetime.date(2013, 1, 4): 24, datetime.date(2013, 1, 2): 27, datetime.date(2013, 1, 23): 18, datetime.date(2013, 1, 21): 2, datetime.date(2013, 1, 14): 18, datetime.date(2013, 1, 19): 1, datetime.date(2013, 1, 12): 2, datetime.date(2013, 1, 17): 70, datetime.date(2013, 1, 10): 37, datetime.date(2013, 1, 31): 10, datetime.date(2013, 1, 8): 39, datetime.date(2013, 1, 29): 11, datetime.date(2013, 1, 27): 1, datetime.date(2013, 1, 25): 4, datetime.date(2013, 1, 7): 33, datetime.date(2013, 1, 5): 6, datetime.date(2013, 1, 3): 8, datetime.date(2013, 1, 22): 24, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 4, datetime.date(2013, 1, 18): 36, datetime.date(2013, 1, 11): 17, datetime.date(2013, 1, 16): 22, datetime.date(2013, 1, 9): 124, datetime.date(2013, 1, 30): 12, datetime.date(2013, 1, 28): 6}, {datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 15, datetime.date(2013, 1, 6): 9, datetime.date(2013, 1, 4): 40, datetime.date(2013, 1, 2): 63, datetime.date(2013, 1, 23): 34, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 19, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 12, datetime.date(2013, 1, 17): 148, datetime.date(2013, 1, 10): 51, datetime.date(2013, 1, 31): 13, datetime.date(2013, 1, 8): 49, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 3, datetime.date(2013, 1, 25): 15, datetime.date(2013, 1, 7): 77, datetime.date(2013, 1, 5): 7, datetime.date(2013, 1, 3): 40, datetime.date(2013, 1, 22): 37, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 6, datetime.date(2013, 1, 18): 48, datetime.date(2013, 1, 11): 40, datetime.date(2013, 1, 16): 49, datetime.date(2013, 1, 9): 104, datetime.date(2013, 1, 30): 26, datetime.date(2013, 1, 28): 15}]
    drawing_pie('2013-01-02', '2013-01-31') #output: pie_sentiment.png - you can see a graph in a pop-up window. you don't need to save the graph
    drawing_lines('2013-01-02', '2013-01-31') # output: lines_sentiment.png
    return

if __name__ == '__main__':
    main()
