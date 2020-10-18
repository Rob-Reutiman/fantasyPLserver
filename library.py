import pprint
import requests

class _fpl_database:

  def __init__(self):
    self.players = []
    self.teams = []
    self.fixtures = []

  def loadTemplate(self):

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
          "position": player["element_type"]
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
    pass

if __name__ == "__main__":
  fplDB = _fpl_database()