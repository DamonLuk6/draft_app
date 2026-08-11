#luk 
#incorporate scoring sheet logic from draft sheet

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


def convertSelfRatingToNumeric(row, skillCategory, ratingScale): #converts each players' self rating text response to number
    responseNumericRating = 0
    selfResponse = row[skillCategory].strip()

    skillRatingScaleDict = ratingScale[skillCategory]
    try:
        responseNumericRating = skillRatingScaleDict[selfResponse]
    except KeyError:
        print(skillCategory)
        print(row['first_name'], row['last_name'])
        print("key does not exist in scale dictionary")

    return responseNumericRating

def calculateSelfRating(row): #calculates self rating using each skill and their score
    selfRating = (0.05 * row['experience rating'] + \
                0.25 * row['level of play rating'] + \
                0.2 * row['throwing rating'] + \
                0.15 * row['cutting rating'] + \
                0.2 * row['athleticism rating'] + \
                0.15 * row['endurance rating']) * 2 

    return selfRating
                
def calculateRecommendedAdj(row):
    recommendedAdjustment = 0
    lowerLimit = 0.98
    upperLimit = 1.23

    if row['ratio self to vet rating'] < lowerLimit:
        recommendedAdjustment = 1 - row['ratio self to vet rating']
    elif row['ratio self to vet rating'] > upperLimit: 
        recommendedAdjustment = (row['self skill rating'] - row['historical player rating']) / (row['ratio self to vet rating'] * 1.4)

    return recommendedAdjustment


if __name__ == "__main__":

    try: #getting registered players
        raw_player_data = pd.read_csv("../data/raw_player_registration.csv")
    except FileNotFoundError:
        print("raw player data file is missing")

    #only need accepted players
    accepted_player_data_raw = raw_player_data[raw_player_data['status'] == 'accepted']

    #skipping first row and adding column names, might have to adjust depending on actual player rating file
    player_rating_col_names = ['first_name', 'last_name', 'usau', 'rating']
    try: #getting historical ratings
        existing_player_rating = pd.read_csv("../data/players_rating_list.csv" , skiprows = 1, names = player_rating_col_names, usecols = [0,1,2,3]) 
    except FileNotFoundError:
        print("ratings file is missing")

    try: #getting rating scale
        self_rating_scales = pd.read_csv("../data/self_rating_scales.csv")
    except FileNotFoundError:
        print("self rating scales file is missing")

    scaleDict = {} #transforming rating scale to a dictionary
    for index,row in self_rating_scales.iterrows():
        scaleDict.setdefault(row['Category'], {})[row['Response']] = row['Score'] #gets category dict, if it doesn't exist, make one

    accepted_players_data_subset = accepted_player_data_raw[['first_name', \
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


    accepted_players_data_subset['historical player rating'] = accepted_players_data_subset.apply( lambda row: findExistingPlayerRating(row, existing_player_rating), axis=1)

    accepted_players_data_subset['throwing rating'] = accepted_players_data_subset.apply( lambda row: convertSelfRatingToNumeric(row, "Throwing", scaleDict), axis = 1)

    accepted_players_data_subset['cutting rating'] = accepted_players_data_subset.apply( lambda row: convertSelfRatingToNumeric(row, "Cutting", scaleDict), axis = 1)

    accepted_players_data_subset['athleticism rating'] = accepted_players_data_subset.apply( lambda row: convertSelfRatingToNumeric(row, "Athleticism", scaleDict), axis = 1)

    accepted_players_data_subset['endurance rating'] = accepted_players_data_subset.apply( lambda row: convertSelfRatingToNumeric(row, "Endurance", scaleDict), axis = 1)

    accepted_players_data_subset['experience rating'] = accepted_players_data_subset.apply( lambda row: convertSelfRatingToNumeric(row, "Experience Count", scaleDict), axis = 1)

    accepted_players_data_subset['level of play rating'] = accepted_players_data_subset.apply( lambda row: convertSelfRatingToNumeric(row, "Level of Play", scaleDict), axis = 1)

    accepted_players_data_subset['self skill rating'] = accepted_players_data_subset.apply(calculateSelfRating, axis = 1)

    accepted_players_data_subset['ratio self to vet rating'] = accepted_players_data_subset['self skill rating'] / accepted_players_data_subset['historical player rating']

    accepted_players_data_subset['recommended adjustment'] = accepted_players_data_subset.apply(calculateRecommendedAdj, axis = 1)

    accepted_players_data_subset['attendance adjustment'] = accepted_players_data_subset.apply( lambda row: convertSelfRatingToNumeric(row, "Missing Games", scaleDict), axis = 1)

    accepted_players_data_subset['manual adjustment'] = 0

    accepted_players_data_subset['calculated total rating'] = 0.75 * accepted_players_data_subset['historical player rating'] + \
                                                                0.25 * accepted_players_data_subset['self skill rating'] - \
                                                                0.12 * accepted_players_data_subset['attendance adjustment']

    accepted_players_data_subset.to_csv("../data/scoring.csv", index = False, float_format = "%.3f")

