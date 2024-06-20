import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji


def stats ( selected_user, df ) :


    if selected_user!='Overall':
        df=df[df.users==selected_user]


    total_msgs=df.shape[0]

    words = []
    for i in df.msgs:
        k = i.split()
        words.extend(k)
    total_words=len(words)


    total_media=df[df.msgs=='<Media omitted>\n'].shape[0]

    extractor = URLExtract()
    links = []
    for i in df.msgs:
        k = extractor.find_urls(i)
        links.extend(k)
    total_links = len(links)

    return total_msgs,total_words,total_media,total_links

def most_busy_users(df):
    x=df.users.value_counts().head()

    percentage = round((df.users.value_counts() / df.shape[0]) * 100, 2)
    percentage_df = pd.DataFrame(percentage)
    percentage_df = percentage_df.reset_index()
    percentage_df = percentage_df.rename(columns={'index': 'names', 'users': 'percentages'})

    return x,percentage_df

def create_wordcloud(selected_user,df):

    f = open('hinglish_stopwords.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df.users == selected_user]

    temp = df[df['users'] != 'group_notif']
    temp = temp[temp['msgs'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['msgs'] = temp['msgs'].apply(remove_stop_words)
    df_wc_img=wc.generate(temp['msgs'].str.cat(sep=" "))

    return df_wc_img


def most_common_words(selected_user,df):

    if selected_user!='Overall':
        df=df[df.users==selected_user]

    words_df = df.msgs[df.users != 'group_notif']
    words_df = words_df[words_df != 'This message was deleted\n']

    hinglish_stopwords_file = open('hinglish_stopwords.txt', 'r', encoding='utf-8')
    hinglish_stopwords = hinglish_stopwords_file.read()
    hinglish_stopwords = hinglish_stopwords.split()

    words = []
    for msgs in words_df:
        k = msgs.split()
        for word in k:
            word = word.lower()
            if word not in hinglish_stopwords:  # removes hinglish stopwords
                if word != '<Media' and word != '<media' and word != 'omitted>':  # removes media ommited
                    words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    most_common_df = most_common_df.rename(columns={0: 'Words', 1: 'Count'})

    return most_common_df,words

def most_common_cuss_words(selected_user,words,df):

    if selected_user!='Overall':
        df=df[df.users==selected_user]

    cuss_words_file = open('cuss_words.txt', 'r', encoding='utf-8')
    cuss_words = cuss_words_file.read()
    cuss_words = cuss_words.split()

    total_cuss_words = []
    for word in words:
        if word in cuss_words:
            total_cuss_words.append(word)

    cuss_words_df = pd.DataFrame(Counter(total_cuss_words).most_common(15))
    cuss_words_df = cuss_words_df.rename(columns={0: 'Gaali', 1: 'Count'})

    return cuss_words_df

def most_common_emoji(selected_user,df):

    if selected_user!='Overall':
        df=df[df.users==selected_user]

    emojis = []
    for msg in df.msgs:
        list_of_dict = emoji.emoji_list(msg)
        for dict in list_of_dict:
            emojis.append(dict['emoji'])

    common_emoji_df=pd.DataFrame(Counter(emojis).most_common())
    common_emoji_df = common_emoji_df.rename(columns={0: 'Emoji', 1: 'Count'})

    return common_emoji_df

def timeline_data( selected_user, df):

    if selected_user != 'Overall':
        df = df[df.users == selected_user]

    df['month_num'] = df.msg_dates.dt.month

    timeline = df.groupby(['year', 'month_num', 'month']).msgs.count()
    timeline_df=timeline.reset_index()

    month_year=[]
    for i in range(0, timeline_df.shape[0]):
        month_year.append(str(timeline_df.month[i])[0:3] + ' - ' + str(timeline_df.year[i]))

    timeline_df['month_year']=month_year

    return timeline_df

def weekday_data(selected_user,df):

    if selected_user != 'Overall':
        df = df[df.users == selected_user]

    df['day_names'] = df.msg_dates.dt.day_name()

    weekday_count = df.groupby(['day_names']).count().msgs
    weekday_count_df = weekday_count.reset_index()

    weekday_count_df = weekday_count_df.sort_values(by=['msgs'], ascending=False)

    return weekday_count_df

def month_data(selected_user,df):

    if selected_user != 'Overall':
        df = df[df.users== selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df.users== selected_user]

    df['day_names'] = df.msg_dates.dt.day_name()

    period = []
    for i in df.hours:
        if i == 23:
            period.append(str(i) + '-' + '00')
        elif i == 0:
            period.append('00' + '-' + str(i + 1))
        else:
            period.append(str(i) + '-' + str(i + 1))

    df['period'] = period

    heatmap_df=df.copy()

    return heatmap_df