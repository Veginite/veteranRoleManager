from league_verification import get_league_verification


def get_conflux_year_count(private_leagues: list) -> int:
    league_years: list = []
    if len(private_leagues) > 0:
        for x in private_leagues:
            league_name = x[0][0][0].text  # div/h3/a
            if get_league_verification(league_name):
                year: int = 0
                try:
                    year = int(x[2][0][1].text.split(', ')[1])  # div/div/span (splits and chooses only the league's start year)
                except (IndexError, ValueError) as e:
                    print(e)
                    print('ERROR: Invalid year, possibly due to end of the league')
                else:
                    league_years.append(year)

    else:
        return 0

    return len(set(league_years))
