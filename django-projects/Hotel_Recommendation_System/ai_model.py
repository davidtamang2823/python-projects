from numpy import pi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import pickle
import os.path

if os.path.isfile('trained_model') == False:
    hotels = pd.read_csv('./Hotel_details.csv')
    rooms = pd.read_csv('./Hotel_Room_attributes.csv')

    roomindexes = rooms[rooms['roomamenities'].isnull() == True]['roomamenities'].index
    for i in roomindexes:
        rooms.drop(i, axis=0, inplace=True)

    rooms = rooms.drop_duplicates(subset=["hotelid","roomtype"])

    #Removing symbols which are not needed in roomamenities column value of rooms dataframe
    def remove_symbols(string):

        words = string.split(': ;')
        symbols = {'/':'/', '!':'!', '(':'(', ')':')', '[':'[', ']':']', '-':'-', ',':','}
        new_string = ''
        for w in range(len(words)):
            for c in words[w]:
                if c in symbols:
                    words[w] = words[w].replace(symbols[c], '')

        for new_words in words:
            new_string += new_words + ' '

        return new_string.strip()

    rooms['roomamenities'] = rooms['roomamenities'].apply(remove_symbols)

    newdf = pd.merge(hotels,rooms, on='hotelid', how ='inner')

    newdf['content'] = newdf[['hotelname','roomamenities']].astype('str').apply(lambda x:' // '.join(x), axis = 1)

    newdf = newdf.reset_index(drop = True)

    tf = TfidfVectorizer(analyzer = 'word', min_df = 0, ngram_range = (1, 2),stop_words = 'english')
    tfidf_matrix = tf.fit_transform(newdf['content'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}
    for idx, row in newdf.iterrows():
        hotel_id = row.hotelid
        rt = str(row.roomtype).strip()
        similar_indices = cosine_similarities[idx].argsort()
        similar_items = [(cosine_similarities[idx][i], newdf['hotelid'][i]) for i in similar_indices if newdf.loc[i].hotelid != hotel_id and str(newdf.loc[i].roomtype).strip() == rt]
        results[(row['hotelid'],row['roomtype'])] = similar_items


    with open('trained_model','wb') as f:
        pickle.dump(results, f)
        
    print('pretrained model created')