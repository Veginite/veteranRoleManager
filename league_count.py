def get_league_count(private_leagues: list) -> int:
    league_years: list = []
    if len(private_leagues) > 0:
        for x in private_leagues:
            league_name = x[0][0][0].text  # div/h3/a
            year = ''
            try:
                year = x[2][0][1].text.split(', ')[1]  # div/div/span (splits and chooses only the league's start year)
            except IndexError:
                year = 'Incorrect Format'

            #verify league name here

            try:
                league_years.append(int(year))
            except ValueError:
                print('ERROR: Invalid year, possibly due to end of the league')
    else:
        return 0

    return len(set(league_years))