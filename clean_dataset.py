"""Cleans the dataset into a format for the ANN to predict"""
import pandas as pd
import datetime

def bdate_to_age(date:str) -> int:
    """
    Calculates the age of a person based on their birth date.
    
    Args:
        date: date string in standard iso format
    
    Returns:
        Current age of the player.
    """
    today = datetime.datetime.now()
    bdate = datetime.datetime.strptime(date, '%Y-%m-%d')
    return today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))

def height_in_inches(height:str) -> float:
    """
    Converts the height to inches.
    
    Args: 
        height: String in the format 'ft-in'
    
    Returns:
        Height in inches of the player.
    """
    if height:
        list_height = [float(i) for i in height.split("-")]
        return (list_height[0] * 12) + list_height[1]
    return height

def age_str_to_float(age:str) -> float:
    """
    Converts the age to a numeric value.
    
    Args:
        age: String in the format 'age-days'.
    
    Returns: 
        Age of the player for that game.
    """
    if age:
        list_age = [float(i) for i in age.split("-")]
        
        if len(list_age) > 1:
            days = (list_age[1]/365)
        else:
            days = 0
            
        return list_age[0] + days
    return age

def clean_data(games:pd.DataFrame, profiles:pd.DataFrame):
    """
    Preparing and cleaning the data for training.

    Args: 
        games: Football game metadata
        profiles: Football players metadata
    """
    print("\tMerging datasets...")
    games_played = games.merge(profiles)

    print("\tTransforming variables...")
    # Adding and transforming features
    games_played['current_age'] = games_played.birth_date.apply(bdate_to_age)
    games_played['height'] = games_played.height.apply(height_in_inches)
    games_played['age'] = games_played.age.apply(age_str_to_float)
    games_played['win'] = games_played.player_team_score > games_played.opponent_score
    games_played['score_diff'] = games_played.player_team_score - games_played.opponent_score

    # Deleting data on players that have passed away
    games_played = games_played.loc[games_played.death_date.isna(), :]

    print("\tRemoving unnecessary features...")
    games_played.drop(['hof_induction_year', 'birth_date', 'death_date', 'player_id'],
                      axis = 1, inplace = True)

    print("\tWriting to csv...")
    games_played.to_csv('nfl-football-player-stats/training_data.csv')


if __name__ == '__main__':
    print("Starting to clean data...")
    clean_data(pd.read_json('nfl-football-player-stats/games_1512362753.8735218.json'),
               profiles = pd.read_json('nfl-football-player-stats/profiles_1512362725.022629.json'))
    print("Finished cleaning data...")
