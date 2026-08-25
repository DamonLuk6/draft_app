#luk
#note to self: need to ask for user input on flask for tier cutoffsÍ

import pandas as pd

def assignTiers(rankByGender, gender, tier_cutoff: dict): #use user input to figure out how many of each gender is in each tier, separate by gender, sort by rating

    try:
        tierCutoffByGender = tier_cutoff[gender]
    except KeyError:
        print("no tier cutoff defined for gender")
        return "Unassigned"

    if rankByGender <= tierCutoffByGender['tier_1']:
        return "1"
    elif rankByGender <= tierCutoffByGender['tier_2']:
        return "2"
    else:
        return "3"

def calculateBaggageEval(scoringSheetWithBaggages): 

    noBaggage = scoringSheetWithBaggages[scoringSheetWithBaggages['baggage'].isna()] #players without baggage
    baggage = scoringSheetWithBaggages[scoringSheetWithBaggages['baggage'].notna()] #players with baggage

    noBaggage['Baggage Eval'] = noBaggage['final rating'] #players without baggage, their "baggage eval" is just their indiv. rating


    baggageEvalDF = baggage.groupby('baggage_group_id')['final rating'].mean().reset_index()
    baggageEvalDict = baggageEvalDF.set_index('baggage_group_id')['final rating'].to_dict()

    baggage['Baggage Eval'] = baggage['baggage_group_id'].apply(lambda x: baggageEvalDict.get(x))

    fullDraftWithBaggageEval = pd.concat([noBaggage, baggage], ignore_index = True).sort_values(by = 'Baggage Eval', ascending = False)

    return fullDraftWithBaggageEval
    

def generateDraftSheet(tier_cutoff: dict):

    try:
        scoringSheetDF = pd.read_csv("data/scoring.csv")
    except FileNotFoundError:
        print("scoring sheet file not found")
        raise

    scoringSheetDF['final rating'] = scoringSheetDF['manual adjustment'] + scoringSheetDF['calculated total rating']

    scoringSheetDF['rank by gender'] = scoringSheetDF.groupby('gender_id')['final rating'].rank(ascending = False)
    scoringSheetDF['tier'] = scoringSheetDF.apply( lambda row: assignTiers(row['rank by gender'], row['gender_id'], tier_cutoff), axis = 1)

    fullDraftSheet = calculateBaggageEval(scoringSheetDF)

    return fullDraftSheet


if __name__ == "__main__":

    test_tier_cutoff = {
        "Man/Boy": {"tier_1": 15, "tier_2": 44},
        "Woman/Girl": {"tier_1": 9, "tier_2": 28}
    }


    result = generateDraftSheet(test_tier_cutoff)
    result.to_csv("./data/draft_sheet.csv", index = False, float_format = "%.3f")