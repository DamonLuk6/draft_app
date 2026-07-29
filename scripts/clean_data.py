#luk 

import pandas as pd 

raw_player_data = pd.read_csv("data/raw_player_registration.csv")

raw_player_data_column_subset = raw_player_data[['first_name', \
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

print(raw_player_data.head(10))
print(raw_player_data_column_subset.head(10))

#incorporate scoring sheet logic from draft sheet