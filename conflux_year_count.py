from league_verification import get_league_verification


def get_conflux_year_count(private_leagues: list) -> int:
    league_years: list = []
    invalid_year_found = False
    if len(private_leagues) > 0:
        for x in private_leagues:
            league_name = x[0][0][0].text  # div/h3/a
            if get_league_verification(league_name):
                year: int = 0
                start_date = x[2][0][1].text
                if ", " in start_date:
                    try:
                        year = int(start_date.split(', ')[1])  # div/div/span (splits and chooses only the league's start year)
                    except (IndexError, ValueError) as e:
                        print(e)
                        print(f'ERROR: Invalid year found in text: "{start_date}"')
                        invalid_year_found = True
                        break
                    else:
                        league_years.append(year)
                else:
                    print(f'ERROR: Delimiter ", " not found in "{start_date}"')
                    invalid_year_found = True
                    break

    if invalid_year_found:
        return -1
    else:
        return len(set(league_years))
