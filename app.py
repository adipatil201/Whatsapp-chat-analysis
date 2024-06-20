import numpy as np
import preprocessor
import streamlit as st
import helpfunc
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file=st.sidebar.file_uploader('chose the file')       #creates a window on the left of screen where we can upload any whatsapp chat
if uploaded_file is not None:
    data=uploaded_file.getvalue()
    data=data.decode('utf-8')           # decodes the data using utf-8
    # st.text(data)                     #can be used to print the entire chat on the site

    df=preprocessor.preprocess(data)    #uses the preprocess() in the preprocessor.py file to convert the str data to a df
    st.dataframe(df)                    #prints a dataframe on the site


    #getting unique users from the chat
    list_of_users=df.users.unique().tolist()              # gets all unique users from users in df
    list_of_users.remove('group_notif')                   # removes 'group_notif' as it is pointless to do its analysis rn
    list_of_users.sort()                                  # sorts list alphabetically
    list_of_users.insert(0,'Overall')                     # inserts 'overall' so as to have a option to do complete analysis

    selected_user=st.sidebar.selectbox('Show analysis for', list_of_users)   # gives a dropdown of all the unique users to select on who's chat we want to do analysis

    if st.sidebar.button('Show analysis'):

        #statistics
        total_msgs,total_words,total_media,total_links=helpfunc.stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header('Messages')
            st.title(total_msgs)
        with col2:
            st.header('Words')
            st.title(total_words)
        with col3:
            st.header('Media')
            st.title(total_media)
        with col4:
            st.header('Links')
            st.title(total_links)

        #timeline
        st.title("Monthly Timeline")
        timeline_df = helpfunc.timeline_data(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline_df['month_year'], timeline_df['msgs'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #weekday data
        st.title("Activity Map")

        col1,col2=st.columns(2)

        with col1:
            st.header("Most Active Days")
            weekday_count_df=helpfunc.weekday_data(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(weekday_count_df['day_names'], weekday_count_df['msgs'], color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Active Months")
            month_count_df = helpfunc.month_data(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(month_count_df.index, month_count_df.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heatmap
        st.title("Activity Heatmap")

        heatmap_df=helpfunc.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(heatmap_df.pivot_table(index='day_names', columns='period', values='msgs', aggfunc='count').fillna(0))
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)


        #group level analysis
        if selected_user=='Overall':
            st.title('Most Busy Users')

            x,percentage_df=helpfunc.most_busy_users(df)

            col1,col2=st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(percentage_df)

        #wordcloud

        st.title("WordCloud")
        wordcloud_img=helpfunc.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(wordcloud_img)
        st.pyplot(fig)

        #most common words

        st.title('Most Common Words')

        most_common_df,words=helpfunc.most_common_words(selected_user,df)

        fig,ax=plt.subplots()
        ax.barh(most_common_df['Words'],most_common_df['Count'])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # most common cuss words

        st.title('Most Common Cuss Words')

        cuss_word_df=helpfunc.most_common_cuss_words(selected_user,words,df)

        fig, ax = plt.subplots()
        ax.barh(cuss_word_df['Gaali'], cuss_word_df['Count'])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        #emojis

        st.title('Most Common Emojis')

        common_emoji_df=helpfunc.most_common_emoji(selected_user,df)

        col1,col2=st.columns(2)
        with col1:
            st.dataframe(common_emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(common_emoji_df['Count'].head(10), labels=common_emoji_df['Emoji'].head(10), autopct="%0.2f")
            st.pyplot(fig)

