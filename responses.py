from scrape import scrape_private_leagues
from league_count import get_league_count
from league_verification import append_league


def get_response(user_input: str, user_roles: list) -> str:
    prefix = user_input[0]
    if prefix == '§':
        # must follow the exact structure: §[command] [value]
        content_components = user_input.replace('§', '').split(' ', 1)
        if len(content_components) == 2:
            command = content_components[0]
            val = content_components[1]

            # -------- command handling --------
            match command:
                case 'requestrank':
                    # scrape data by verifying and using the account name in var: val
                    private_leagues: list = scrape_private_leagues(val)
                    if len(private_leagues) > 0:
                        private_league_count: int = get_league_count(private_leagues)
                        return 'You have participated in Conflux leagues during ' + str(
                        private_league_count) + ' unique years'
                    else:
                        return 'Error: No leagues found. Check your privacy settings.'
                case 'addleague':
                    for role in user_roles:
                        if role.name == 'League Staff':
                            return append_league(val)
                    return 'You do not have permission to use this command.'
                case _:
                    return 'Unknown command: "' + command + '", see pinned messages for instructions!'
            # -------- end command handling --------
        else:
            return 'Invalid command structure: "' + user_input + '", command must follow structure: §[command] [value]'
