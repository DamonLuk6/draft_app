#luk
#note to self: need to ask for user input on flask for tier cutoffsÍ

import pandas as pd

def calculateTiers(): #use user input to figure out how many of each gender is in each tier, separate by gender, sort by rating

    return 

def generateDraftSheet():

    scoringSheetDF = pd.read_csv("data/scoring.csv")
    scoringSheetDF['final rating'] = scoringSheetDF['manual adjustment'] + scoringSheetDF['calculated total rating']

    scoringSheetDF['rank by gender'] = scoringSheetDF.groupby('gender_id')['final rating'].rank(ascending = False)

    #breakpoint()
    #draft_sheet = pd.DataFrame()


    return scoringSheetDF


if __name__ == "__main__":
    result = generateDraftSheet()
    result.to_csv("./draft_sheet_test.csv", index = False)

    #print(result[["first_name", "last_name", "final_rating", "draft_rank"]].head(10))
