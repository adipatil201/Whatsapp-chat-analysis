import pandas as pd
import re

def preprocess(chat):             # applies the same prerprocessing steps to the str data like the jupyter notebook and finally gives a dataframe

    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s..\s-\s'

    messages=re.split(pattern,chat)[1:]
    date_time = re.findall(pattern,chat)

    df = pd.DataFrame({'user_msgs': messages, 'msg_dates': date_time})

    df.msg_dates = pd.to_datetime(df.msg_dates, format='%m/%d/%y, %I:%M %p - ')

    users = []
    msgs = []
    for i in df.user_msgs:
        entry = re.split('([\w\W]+?):\s',i)
        if entry[1:]:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notif')
            msgs.append(entry[0])

    df['users'] = users
    df['msgs'] = msgs
    df.drop(columns=['user_msgs'], inplace=True)


    df['year'] = df.msg_dates.dt.year
    df['month'] = df.msg_dates.dt.month_name()
    df['day'] = df.msg_dates.dt.day
    df['hours'] = df.msg_dates.dt.hour
    df['minutes'] = df.msg_dates.dt.minute

    return df