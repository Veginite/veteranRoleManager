from scrape import scrape_private_leagues
from league_count import get_league_count

def get_response(user_input: str) -> str:
    prefix = user_input[0]
    if prefix == '§':
        # content must consist of exactly two components, separated by a white space, following structure §[command] [value]
        content_components = user_input.replace('§', '').split(' ')
        if len(content_components) == 2:
            command = content_components[0]
            val = content_components[1]

            # -------- command handling --------
            match command:
                case 'requestrank':
                    # scrape data by verifying and using the link in var: val
                    private_leagues: list = scrape_private_leagues(val)
                    private_league_count: int = get_league_count(private_leagues)
                    return 'You have participated in Conflux leagues during ' + str(private_league_count) + ' unique years'
                case _:
                    return 'Unknown command: "' + command + '", see pinned messages for instructions!'
            #-------- end command handling --------
        else:
            return 'Invalid command structure: "' + user_input + '", command must follow structure: §[command] [value]'