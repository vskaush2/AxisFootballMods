import os
import pandas as pd
import requests
import json

madden_database_URL='https://ratings-api.ea.com/v2/entities/m22-ratings?filter=iteration:week-{}%20AND%20teamId:({})&sort=overall_rating:DESC,firstName:ASC&limit=100&offset=0'

with open("Madden_to_Axis_Positions.json" ,'r') as f:
    madden_to_axis_positions_dict = json.load(f)

with open("Axis_To_Madden_Attributes.json",'r') as f:
    axis_to_madden_attributes_dict = json.load(f)

with open('Madden_Team_IDs.json', 'r') as f:
    madden_IDs_dict = json.load(f)


class RosterGenerator:

    def __init__(self, team_name, week_num):
        self.team_name = team_name
        self.week_num = week_num
        self.madden_ID_number = self.get_madden_ID_number()
        self.madden_database_URL = madden_database_URL.format(self.week_num, self.madden_ID_number)
        if self.week_num == '19':
            self.madden_database_URL = self.madden_database_URL.replace("week-19","wild-card-round")
        if self.week_num == '20':
            self.madden_database_URL = self.madden_database_URL.replace("week-20","divisional-round")
        self.madden_roster_df = self.get_madden_roster_df()
        self.axis_roster_df = self.get_axis_roster_df()
        self.madden_position_count_dict = self.get_madden_position_count_dict()
        self.axis_roster_starting_offense_df = self.get_axis_roster_starting_offense_df()
        self.axis_roster_starting_defense_df = self.get_axis_roster_starting_defense_df()
        self.axis_roster_starting_ST_df = self.get_axis_roster_starting_ST_df()
        self.axis_roster_starters_df = self.get_axis_roster_starters_df()
        self.axis_roster_backups_df = self.get_axis_roster_backups_df()



    def get_madden_ID_number(self):
        madden_ID_number= madden_IDs_dict[self.team_name]
        return madden_ID_number

    def get_madden_roster_df(self, update=False):
        madden_roster_df = pd.DataFrame()
        directory = "Madden Rosters"
        try:
            os.makedirs(directory)
        except:
            pass
        file_path="{}/{}.csv".format(directory,self.team_name)

        if os.path.exists(file_path):
            madden_roster_df = pd.read_csv(file_path, index_col=0)
        else:
            update=True

        if update:
            try:
                madden_roster_df = pd.DataFrame(requests.get(self.madden_database_URL).json()['docs'])
                madden_cols = ['firstName', 'lastName', 'position', 'jerseyNum', 'age', 'height', 'weight', 'overall_rating'] + \
                              [col for col in madden_roster_df.columns if '_rating' in col and 'overall' not in col]
                madden_roster_df = madden_roster_df[madden_cols]
                madden_roster_df.to_csv(file_path)
            except:
                pass

        return madden_roster_df

    def get_axis_roster_df(self):
        file_path = 'Original Team Mods/{}/ROSTER.csv'.format(self.team_name)
        axis_roster_df = pd.read_csv(file_path)
        return axis_roster_df

    def get_madden_position_df(self, madden_position_abbrev):
        madden_position_df = self.madden_roster_df[self.madden_roster_df['position'] == madden_position_abbrev]
        return madden_position_df

    def get_madden_position_count_dict(self):
        madden_position_abbrevs = ['QB', 'HB', 'FB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT',
                                   'LE', 'DT', 'RE', 'LOLB', 'MLB', 'ROLB', 'CB', 'FS', 'SS',
                                   'K', 'P']
        madden_position_counts=[len(self.get_madden_position_df(madden_position_abbrev)) for madden_position_abbrev in madden_position_abbrevs]
        madden_position_count_dict = dict(zip(madden_position_abbrevs, madden_position_counts))
        return madden_position_count_dict

    def get_axis_roster_starting_offense_df(self):
        madden_offense_position_abbrevs = ['QB', 'HB', 'FB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT']
        QBs_df, RBs_df, FBs_df, WRs_df, TEs_df, LTs_df, LGs_df, Cs_df, RGs_df, RTs_df =\
            [self.get_madden_position_df(position_abbrev) for position_abbrev in madden_offense_position_abbrevs]

        axis_roster_starting_offense_df= QBs_df.iloc[:1]

        if len(FBs_df) !=0: # Starting offensive backfield will be HB 1 and FB 1 if a FB exists on the team
            axis_roster_starting_offense_df = pd.concat([axis_roster_starting_offense_df, RBs_df.iloc[:1], FBs_df.iloc[:1]], axis=0)
        else: # Starting offensive backfield will be HB 1 and HB 2 if a FB does not exist on the team
            axis_roster_starting_offense_df = pd.concat([axis_roster_starting_offense_df, RBs_df.iloc[:2]], axis=0)

        axis_roster_starting_offense_df = pd.concat([axis_roster_starting_offense_df,
                                                     WRs_df.iloc[:5], TEs_df.iloc[:1],
                                                     LTs_df.iloc[:1], LGs_df.iloc[:1], Cs_df.iloc[:1],
                                                     RGs_df.iloc[:1], RTs_df.iloc[:1]], axis=0)

        axis_roster_starting_offense_df.dropna(axis=0,how='any',inplace=True)
        return axis_roster_starting_offense_df

    def get_axis_roster_starting_defense_df(self):
        madden_defense_position_abbrevs = ['LE', 'DT', 'RE', 'LOLB', 'MLB', 'ROLB', 'CB', 'SS', 'FS']
        LEs_df, DTs_df, REs_df, LOLBs_df, MLBs_df, ROLBs_df, CBs_df, SSs_df, FSs_df = \
            [self.get_madden_position_df(position_abbrev) for position_abbrev in madden_defense_position_abbrevs]

        axis_roster_starting_defense_df=None

        if len(DTs_df) > 1: # Starting Defensive Line will be LE 1, DT 1, DT 2, RE 1 if team has least 2 DTs
            axis_roster_starting_defense_df = pd.concat([LEs_df.iloc[:1], DTs_df.iloc[:2], REs_df.iloc[:1]], axis=0)
        elif len(REs_df) > 1: # Starting Defensive Line will be LE 1, DT 1, RE 1, RE 2 if team has only 1 DT, but 2 REs
            axis_roster_starting_defense_df = pd.concat([LEs_df.iloc[:1], DTs_df.iloc[:1], REs_df.iloc[:2]], axis=0)
        elif len(LEs_df) > 1: # Starting Defensive Line will be LE 1, LE 2, DT 1, RE 1 if team has only 1 DT and 1 RE, but 2 LEs
            axis_roster_starting_defense_df = pd.concat([LEs_df.iloc[:2], DTs_df.iloc[:1], REs_df.iloc[:2]], axis=0)

        if len(MLBs_df) > 1: # Starting Linebackers will be LOLB 1, MLB 1, MLB 2, ROLB 1 if team has at least 2 MLBs
            axis_roster_starting_defense_df = pd.concat([axis_roster_starting_defense_df, LOLBs_df.iloc[:1], MLBs_df.iloc[:2], ROLBs_df.iloc[:1]], axis=0)
        elif len(ROLBs_df) > 1: # Starting Linebackers will be LOLB 1, MLB 1, ROLB 1, ROLB 2 if team has only 1 MLB, but 2 ROLBs
            axis_roster_starting_defense_df = pd.concat([axis_roster_starting_defense_df, LOLBs_df.iloc[:1], MLBs_df.iloc[:1], ROLBs_df.iloc[:2]], axis=0)
        elif len(LOLBs_df) > 1: # Starting Linebackers will be LOLB 1, LOLB 2, MLB 1, ROLB 1 if team has only 1 MLB and 1 ROLB, but 2 LOLBs
            axis_roster_starting_defense_df = pd.concat([axis_roster_starting_defense_df, LOLBs_df.iloc[:2], MLBs_df.iloc[:1], ROLBs_df.iloc[:1]], axis=0)

        axis_roster_starting_defense_df=pd.concat([axis_roster_starting_defense_df,
                                                   CBs_df.iloc[:1], CBs_df.iloc[2:3],
                                                   SSs_df.iloc[:1], FSs_df.iloc[:1],
                                                   CBs_df.iloc[1:2], CBs_df.iloc[3:4]] , axis=0)

        axis_roster_starting_defense_df.dropna(axis=0,how='any',inplace=True)

        return axis_roster_starting_defense_df

    def get_axis_roster_starting_ST_df(self):
        madden_ST_position_abbrevs = ['K','P']
        Ks_df, Ps_df = [self.get_madden_position_df(position_abbrev) for position_abbrev in madden_ST_position_abbrevs]
        axis_roster_starting_ST_df=pd.concat([Ks_df.iloc[:1], Ps_df.iloc[:1]], axis=0)
        return axis_roster_starting_ST_df

    def get_axis_roster_starters_df(self):
        axis_roster_starters_df=pd.concat([self.axis_roster_starting_offense_df, self.axis_roster_starting_defense_df, self.axis_roster_starting_ST_df], axis=0)
        return axis_roster_starters_df

    def get_axis_roster_backups_df(self):
        unused_players_df = pd.concat([self.axis_roster_starters_df, self.madden_roster_df],axis=0).drop_duplicates(keep=False)
        QBs_df, RBs_df, FBs_df, WRs_df, TEs_df, LTs_df, LGs_df, Cs_df, RGs_df, RTs_df, \
        LEs_df, DTs_df, REs_df, LOLBs_df, MLBs_df, ROLBs_df, CBs_df, SSs_df, FSs_df, \
        Ks_df, Ps_df =\
            [unused_players_df[unused_players_df['position'] ==pos] for pos in self.madden_position_count_dict.keys()]

        axis_roster_backups_df=pd.concat([QBs_df.iloc[:4],
                                          RBs_df.iloc[:4], FBs_df.iloc[:1],
                                          WRs_df.iloc[:4], TEs_df.iloc[:2],
                                          LTs_df.iloc[:1], LGs_df.iloc[:1], Cs_df.iloc[:1], RGs_df.iloc[:1], RTs_df.iloc[:1],
                                          LEs_df.iloc[:2], DTs_df.iloc[:2], REs_df.iloc[:2],
                                          LOLBs_df.iloc[:3], MLBs_df.iloc[:3], ROLBs_df.iloc[:3],
                                          CBs_df.iloc[:4], SSs_df.iloc[:2], FSs_df.iloc[:2],
                                          Ks_df.iloc[:1], Ps_df.iloc[:1]],axis=0)

        axis_roster_backups_df.dropna(axis=0,how='any',inplace=True)
        axis_roster_backups_df=axis_roster_backups_df.iloc[:23]
        return axis_roster_backups_df


    def get_new_axis_roster_df(self):
        new_players_df = pd.concat([self.axis_roster_starters_df, self.axis_roster_backups_df], axis=0).reset_index()
        new_axis_roster_df = self.axis_roster_df.copy()
        file_path = "Mods/Team Mods/{}/ROSTER.CSV".format(self.team_name)

        try:
            for axis_attribute in new_axis_roster_df.columns:
                if axis_attribute in axis_to_madden_attributes_dict.keys():
                    madden_attribute = axis_to_madden_attributes_dict[axis_attribute]
                    if madden_attribute == 'position':
                        new_axis_roster_df[axis_attribute] = new_players_df[madden_attribute].apply(lambda pos: madden_to_axis_positions_dict[pos])
                    elif type(madden_attribute) == str:
                        new_axis_roster_df[axis_attribute] = new_players_df[madden_attribute]
                    elif type(madden_attribute) == list:
                        new_axis_roster_df[axis_attribute] = new_players_df[madden_attribute].mean(axis=1).apply(lambda x: int(x))

            new_axis_roster_df.dropna(how='any',axis=0,inplace=True)
            if len(new_axis_roster_df) != 53:
                new_axis_roster_df = self.axis_roster_df.copy()

            new_axis_roster_df.to_csv(file_path, index=False)
            return new_axis_roster_df

        except:
            print("FAILED TO CONVERT MADDEN WEEK {} ROSTER INTO AN AXIS ROSTER FOR {} !".format(self.week_num, self.team_name))
            self.axis_roster_df.to_csv(file_path,index=False)
            return self.axis_roster_df

























