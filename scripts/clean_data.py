#luk 

import pandas as pd 

def findExistingPlayerRating(row, historicalRatings): #finds existing ratings for each player

    playerRating = 4 #default player rating
    
    try:
        playerUSAU = int(row['USAU_member_id']) 
    except(ValueError, TypeError):
        print(row['first_name'], row['last_name'], row['USAU_member_id'])
        return playerRating
    

    existingPlayer = historicalRatings[historicalRatings['usau'] == playerUSAU] #search for existing player rating



    if not existingPlayer.empty: 
        playerRating = existingPlayer['rating'].values[0] #extract historical player rating
    

    return playerRating


def calculateSelfRating(row): #calculates each players' self rating 
    selfRating = 0



    return selfRating
if __name__ == "__main__":

    try: 
        raw_player_data = pd.read_csv("../data/raw_player_registration.csv")
    except FileNotFoundError:
        print("raw player data file is missing")

    #only need accepted players
    accepted_player_data_raw = raw_player_data[raw_player_data['status'] == 'accepted']

    #skipping first row and adding column names, might have to adjust depending on actual player rating file
    player_rating_col_names = ['first_name', 'last_name', 'usau', 'rating']
    try:
        existing_player_rating = pd.read_csv("../data/players_rating_list.csv" , skiprows = 1, names = player_rating_col_names, usecols = [0,1,2,3]) 
    except FileNotFoundError:
        print("ratings file is missing")

    try:
        self_rating_scales = pd.read_csv("../data/self_rating_scales.csv")
    except FileNotFoundError:
        print("self rating scales file is missing")

    accepted_players_data_column_subset = accepted_player_data_raw[['first_name', \
                                        'last_name', \
                                        'email_address', \
                                        'gender_id', \
                                        'age', \
                                        'shirt_size', \
                                        'USAU_member_id', \
                                        'baggage_group_id', \
                                        'baggage', \
                                        'Captain Interest', \
                                        'Experience Count', \
                                        'Level of Play', \
                                        'Height', \
                                        'Experience List', \
                                        'Throwing', \
                                        'Cutting', \
                                        'Athleticism', \
                                        'Endurance', \
                                        'Role', \
                                        'Names', \
                                        'New Player', \
                                        'Missing Games', \
                                        'Status']]

    #print(raw_player_data.head(10))
    #print(accepted_players_data_column_subset.head(10))
    #print(existing_player_rating.head())

    accepted_players_data_column_subset['player_rating'] = accepted_players_data_column_subset.apply( lambda row: findExistingPlayerRating(row, existing_player_rating), axis=1)
    accepted_players_data_column_subset.to_csv("../data/scoring.csv", index = False)

#incorporate scoring sheet logic from draft sheet