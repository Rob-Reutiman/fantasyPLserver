import requests

class _fpl_database:

  def __init__(self):
    self.players = []
    self.teams = []
    self.fixtures = []

  def loadTemplate(self):
    ''' Load basic player, team, fixture data '''

    rGeneral = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    rFixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/")

    generalData = rGeneral.json()
    fixtureData = rFixtures.json()

    # Load teams
    for team in generalData["teams"]:
      self.teams.append(
        {
          "name": team["name"],
          "abbr": team["short_name"]
        }
      )

    # Load players
    for player in generalData["elements"]:
      self.players.append(
        {
          "firstName": player["first_name"],
          "lastName": player["second_name"],
          "teamID" : player["team"],
          "position": player["element_type"],
          "ict": player["ict_index"],
          "ict_position_rank": player["ict_index_rank_type"],
          "goals": player["goals_scored"],
          "assists": player["assists"],
          "ppg": player["points_per_game"],
          "form": player["form"],
          "clean_sheets": player["clean_sheets"],
          "price": float(player["now_cost"]) / 10
        }
      )
    
    # Load fixtures
    for fixture in fixtureData:
      self.fixtures.append(
        {
          "home": fixture["team_h"],
          "homeGoals": fixture["team_h_score"],
          "away": fixture["team_a"],
          "awayGoals": fixture["team_a_score"],
          "date": fixture["kickoff_time"],
        }
      )

  def updateStats(self):
    ''' Update player, team, fixture data '''
    pass

  def getFeaturedPlayers(self):
    pass

if __name__ == "__main__":
  fplDB = _fpl_database()