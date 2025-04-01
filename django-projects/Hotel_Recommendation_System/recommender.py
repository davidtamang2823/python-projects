# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from app.models import Hotel
import pickle

#userName, destination
def create_recommendation_list(userName, destination):
    url_user_details = f'http://localhost:8000/api/user_booking_details/{userName}'
    h = pd.read_csv('./Hotel_details.csv')
    h = h[h['destination'] == destination]
    #Reading csv file using pandas library
    cd = pd.read_json(url_user_details)
    
    if cd['hotelid'].count() > 0:
        print(h[h['hotelid']==2]['hotelid'].count(), 'hotel')
        results = None
        with open('trained_model', 'rb') as f:
            similarity = pickle.load(f)
            results = similarity

        
        def recommend_list(item_id, roomtype ,num, item_remove):    
            recs = results[(item_id,roomtype)]
            for x,y in recs:
                hotel_count = h[h['hotelid']==y]['hotelid'].count()
                if y in item_remove or hotel_count == 0:
                    recs.remove((x,y))
        
            return recs[:num]
            

        #Get unique hotel id booked by user
        unique_hotel_id = cd['hotelid'].unique()

        room_types_count = {'hotelid':[],'roomtype':[],'count':[]}
        room_type_count = {}
        for uh in unique_hotel_id:
            tmp = cd[cd['hotelid'] == uh]
            for rt in tmp['roomtype']:
                if rt not in room_type_count:
                    room_type_count[rt] = 1
                else:
                    room_type_count[rt] += 1
            
            for x, y in room_type_count.items():
                room_types_count['hotelid'].append(uh)
                room_types_count['roomtype'].append(x)
                room_types_count['count'].append(y)

        newcd = pd.DataFrame(room_types_count).sort_values('count',ascending = False)

        room_types = cd['roomtype']
        count_room_types = {}
        df = {'roomtype':[],'booked_count':[]}
        for rt in room_types:
            if rt not in count_room_types:
                count_room_types[rt] = 1
            else:
                count_room_types[rt] += 1
        for x,y in count_room_types.items():
            df['roomtype'].append(x)
            df['booked_count'].append(y)
            
        newcd2 = pd.DataFrame(df)

        newcd = pd.merge(newcd,newcd2, on ='roomtype', how='inner').sort_values(['count','booked_count'], ascending = (False, False))

        def create_recommendation_list(recommend_no):

            recommendation_list = []
            user_hid = newcd.loc[:recommend_no]
            length = len(user_hid.index)
            no_of_recommend = recommend_no 
            remove_item = list(user_hid['hotelid'].unique())
            for indx, row in user_hid.iterrows():
                
                if length == recommend_no:
                    no_to_get = no_of_recommend // length
                    for x,y in recommend_list(row['hotelid'], row['roomtype'] ,no_to_get, remove_item):
                        get_hotel = Hotel.objects.get(id = y)
                        recommendation_list.append(get_hotel) 
                        remove_item.append(int(get_hotel.id))

                else:

                    if length == 1:
                        no_to_get = no_of_recommend // length
                        length -= 1

                        
                        for x,y in recommend_list(row['hotelid'], row['roomtype'] ,no_to_get, remove_item):
                            
                            get_hotel = Hotel.objects.get(id = y)
                            recommendation_list.append(get_hotel)  
                            remove_item.append(int(get_hotel.id))

                    else:
                        no_to_get = no_of_recommend % length
                        no_of_recommend -= no_to_get
                        length -= 1
                        
                        for x,y in recommend_list(row['hotelid'], row['roomtype'] ,no_to_get, remove_item):
                        
                            get_hotel = Hotel.objects.get(id = y)
                            recommendation_list.append(get_hotel) 
                            remove_item.append(int(get_hotel.id))

            return recommendation_list

        return create_recommendation_list(6)
    
    else:
        return None
        




    


