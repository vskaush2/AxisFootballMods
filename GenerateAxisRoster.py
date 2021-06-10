import pandas as pd
import requests


def convert_madden_position_to_axis_position(pos):
    if pos =='HB':
        pos='RB'
    elif pos in ['LG','LT','C','RG','RT']:
        pos='OL'
    elif pos in ['LE','DT','RE']:
        pos='DL'
    elif pos in ['LOLB','MLB','ROLB']:
        pos='LB'
    elif pos in ['CB','SS','FS']:
        pos='DB'
    return pos

class GenerateAxisRoster:

    def __init__(self,team):
        self.team=team
        self.madden_roster_df=self.get_madden_roster_df()
        self.axis_roster_df=self.get_axis_roster_df()
        self.madden_starters_backups_for_axis_dfs=self.get_madden_starters_backups_for_axis_dfs()
        self.new_axis_roster_df=self.convert_madden_roster_to_axis_roster_df()

    def get_madden_roster_df(self):
        try:
            madden_roster_URL='https://maddenratings.weebly.com/uploads/1/4/0/9/14097292/{}__madden_nfl_21_.xlsx'.format(self.team.lower().replace(" ",'_'))
            content = requests.get(madden_roster_URL).content
            madden_roster_df = pd.read_excel(content).drop(columns='Team')
            return madden_roster_df.sort_values(by='Overall Rating',ascending=False)
        except:
            return pd.DataFrame()

    def get_axis_roster_df(self):
        directory = 'Team Mods/' + self.team
        file_path = directory + "/ROSTER.csv"
        axis_roster_df = pd.read_csv(file_path)
        return axis_roster_df

    def convert_madden_to_axis_roster_attributes_df(self,roster_df):
        converted_axis_attributes = ['FIRST', 'LAST', 'NUMBER',
                                     'HEIGHT', 'WEIGHT', 'POS',
                                     'SPEED', 'TLK BRK', 'FUMBLE',
                                     'CATCH', 'BLKING', 'THR ACC',
                                     'KCK PWR', 'KCK ACC', 'BLK BRK',
                                     'TACKLE', 'THR PWR', 'FITNESS',
                                     'AWARE', 'AGIL', 'COVER',
                                     'HIT PWR', 'ENDUR', 'AGE']
        convert_madden_to_axis_roster_attributes_df = pd.DataFrame(columns=converted_axis_attributes)

        convert_madden_to_axis_roster_attributes_df['FIRST'] = roster_df['Full Name'].apply(lambda name: name.split(" ")[0])
        convert_madden_to_axis_roster_attributes_df['LAST'] = roster_df['Full Name'].apply(lambda name: name.split(" ")[1])
        convert_madden_to_axis_roster_attributes_df['NUMBER'] = roster_df['Jersey Number']
        convert_madden_to_axis_roster_attributes_df['HEIGHT'] = roster_df['Height']
        convert_madden_to_axis_roster_attributes_df['WEIGHT'] = roster_df['Weight']
        convert_madden_to_axis_roster_attributes_df['POS'] = roster_df['Position'].apply(
            lambda pos: convert_madden_position_to_axis_position(pos))
        convert_madden_to_axis_roster_attributes_df['SPEED'] = roster_df['Speed']
        convert_madden_to_axis_roster_attributes_df['TLK BRK'] = roster_df['Break Tackle']
        convert_madden_to_axis_roster_attributes_df['FUMBLE'] = roster_df['Carrying']
        convert_madden_to_axis_roster_attributes_df['CATCH'] = roster_df['Catching']
        convert_madden_to_axis_roster_attributes_df['BLKING'] = roster_df[['Lead Blocking', 'Run Blocking', 'Pass Blocking']].mean(
            axis=1).apply(lambda x: int(x))
        convert_madden_to_axis_roster_attributes_df['THR ACC'] = roster_df[['Throw Accuracy Short',
                                                                'Throw Accuracy Mid',
                                                                'Throw Accuracy Deep']].mean(axis=1).apply(
            lambda x: int(x))
        convert_madden_to_axis_roster_attributes_df['KCK PWR'] = roster_df['Kick Power']
        convert_madden_to_axis_roster_attributes_df['KCK ACC'] = roster_df['Kick Accuracy']
        convert_madden_to_axis_roster_attributes_df['BLK BRK'] = roster_df['Block Shedding']
        convert_madden_to_axis_roster_attributes_df['TACKLE'] = roster_df['Tackle']
        convert_madden_to_axis_roster_attributes_df['THR PWR'] = roster_df['Throw Power']
        convert_madden_to_axis_roster_attributes_df['FITNESS'] = roster_df['Injury']
        convert_madden_to_axis_roster_attributes_df['AWARE'] = roster_df['Awareness']
        convert_madden_to_axis_roster_attributes_df['AGIL'] = roster_df['Agility']
        convert_madden_to_axis_roster_attributes_df['COVER'] = roster_df[['Zone Coverage', 'Man Coverage']].mean(axis=1).apply(
            lambda x: int(x))
        convert_madden_to_axis_roster_attributes_df['HIT PWR'] = roster_df['Hit Power']
        convert_madden_to_axis_roster_attributes_df['ENDUR'] = roster_df['Stamina']
        convert_madden_to_axis_roster_attributes_df['AGE'] = roster_df['Age']
        return convert_madden_to_axis_roster_attributes_df.dropna(axis=1)

    def get_madden_starters_backups_for_axis_dfs(self):
        madden_roster_df=self.madden_roster_df
        QBs_df = madden_roster_df[madden_roster_df['Position'] == 'QB']
        RBs_df = madden_roster_df[madden_roster_df['Position'] == 'HB']
        WRs_df = madden_roster_df[madden_roster_df['Position'] == 'WR']
        TEs_df = madden_roster_df[madden_roster_df['Position'] == 'TE']
        LTs_df = madden_roster_df[madden_roster_df['Position'] == 'LT']
        LGs_df = madden_roster_df[madden_roster_df['Position'] == 'LG']
        Cs_df = madden_roster_df[madden_roster_df['Position'] == 'C']
        RGs_df = madden_roster_df[madden_roster_df['Position'] == 'RG']
        RTs_df = madden_roster_df[madden_roster_df['Position'] == 'RT']
        LEs_df = madden_roster_df[madden_roster_df['Position'] == 'LE']
        DTs_df = madden_roster_df[madden_roster_df['Position'] == 'DT']
        REs_df = madden_roster_df[madden_roster_df['Position'] == 'RE']
        LOLBs_df = madden_roster_df[madden_roster_df['Position'] == 'LOLB']
        MLBs_df = madden_roster_df[madden_roster_df['Position'] == 'MLB']
        ROLBs_df = madden_roster_df[madden_roster_df['Position'] == 'ROLB']
        CBs_df = madden_roster_df[madden_roster_df['Position'] == 'CB']
        SSs_df = madden_roster_df[madden_roster_df['Position'] == 'SS']
        FSs_df = madden_roster_df[madden_roster_df['Position'] == 'FS']
        Ks_df = madden_roster_df[madden_roster_df['Position'] == 'K']
        Ps_df = madden_roster_df[madden_roster_df['Position'] == 'P']

        starters_df = pd.concat([QBs_df.iloc[:1],
                                 RBs_df.iloc[:2],
                                 WRs_df.iloc[:5],
                                 TEs_df.iloc[:1],
                                 LTs_df.iloc[:1],
                                 LGs_df.iloc[:1],
                                 Cs_df.iloc[:1],
                                 RGs_df.iloc[:1],
                                 RTs_df.iloc[:1]], axis=0)

        DT_used, LE_used, RE_used=2,1,1
        if len(DTs_df) < 2 and len(LEs_df) < 2 and len(REs_df) >= 2:
            DT_used, LE_used, RE_used= 1,1,2
        if len(DTs_df) < 2 and len(LEs_df) >= 2 and len(REs_df) >= 2:
            DT_used, LE_used, RE_used = 1, 2, 1
        if len(DTs_df) < 2 and len(LEs_df) >= 2 and len(REs_df) < 2:
            DT_used, LE_used, RE_used = 1, 2, 1
        starters_df = pd.concat([starters_df, LEs_df.iloc[:LE_used], DTs_df.iloc[:DT_used], REs_df.iloc[:RE_used]], axis=0)

        MLB_used, LOLB_used, ROLB_used = 2,1,1
        if len(MLBs_df) < 2 and len(LOLBs_df) < 2 and len(ROLBs_df) >= 2:
            MLB_used, LOLB_used, ROLB_used = 1,1,2
        if len(MLBs_df) < 2 and len(LEs_df) >= 2 and len(REs_df) < 2:
            MLB_used, LOLB_used, ROLB_used = 1,2,1
        if len(MLBs_df) < 2 and len(LEs_df) >= 2 and len(REs_df) >= 2:
            MLB_used, LOLB_used, ROLB_used = 1,2,1

        starters_df = pd.concat([starters_df, LOLBs_df.iloc[: LOLB_used], MLBs_df.iloc[:MLB_used], ROLBs_df.iloc[:ROLB_used]],
                                axis=0)

        starters_df = pd.concat([starters_df, CBs_df.iloc[:2], SSs_df.iloc[:1], FSs_df.iloc[:1], CBs_df.iloc[2:4]],
                                axis=0)
        starters_df = pd.concat([starters_df, Ks_df.iloc[:1], Ps_df.iloc[:1]])

        backups_df = pd.concat([QBs_df.iloc[1:4],
                                RBs_df.iloc[2:4],
                                WRs_df.iloc[5:7],
                                TEs_df.iloc[1:3],
                                LTs_df.iloc[1:2],
                                LGs_df.iloc[1:2],
                                Cs_df.iloc[1:2],
                                RGs_df.iloc[1:2],
                                RTs_df.iloc[1:2],
                                LEs_df.iloc[LE_used:LE_used+1],
                                DTs_df.iloc[DT_used:DT_used+1],
                                REs_df.iloc[RE_used:RE_used+1],
                                LOLBs_df.iloc[LOLB_used:LOLB_used+1],
                                MLBs_df.iloc[MLB_used:MLB_used+1],
                                ROLBs_df.iloc[ROLB_used:ROLB_used+1],
                                CBs_df.iloc[4:],
                                SSs_df.iloc[1:],
                                FSs_df.iloc[1:],
                                Ks_df.iloc[1:2],
                                Ps_df.iloc[1:2]], axis=0)

        return starters_df, backups_df

    def convert_madden_roster_to_axis_roster_df(self):
        directory = 'Team Mods/' + self.team
        file_path = directory + "/ROSTER.csv"
        old_axis_roster_df = self.axis_roster_df

        try:
            starters_df, backups_df = self.madden_starters_backups_for_axis_dfs
            converted_attributes_df = self.convert_madden_to_axis_roster_attributes_df(pd.concat([starters_df, backups_df],axis=0))
            converted_attributes_df = converted_attributes_df.reset_index().drop(columns='index')
            new_axis_roster_df = pd.DataFrame(columns=old_axis_roster_df.columns)
            for col in new_axis_roster_df.columns:
                if col in converted_attributes_df.columns:
                    new_axis_roster_df[col] = converted_attributes_df[col]
                else:
                    new_axis_roster_df[col] = old_axis_roster_df[col]

            new_axis_roster_df=new_axis_roster_df.iloc[:53].dropna(how='any',axis=0)
            if len(new_axis_roster_df) == 53:
                print("SUCCESSFULLY CONVERTED "+self.team)
                new_axis_roster_df.to_csv(file_path, index=False)
            else:
                print("FAILED TO CONVERT {} DUE TO SHORTAGE OF PLAYERS (ONLY {} Players)".format(self.team,len(new_axis_roster_df)))
            return new_axis_roster_df
        except:
            print("FAILED TO CONVERT " + self.team)
            return pd.DataFrame()

