import discord

from scrape import scrape_private_leagues
from conflux_year_count import get_conflux_year_count
from league_verification import append_league
from assign_user_veteran_role import assign_user_veteran_role


async def get_response(user_input: str, user: discord.Message.author) -> str:
    prefix = user_input[0]
    if prefix == '!':
        # must follow the exact structure: ![command] [value]
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
                        conflux_year_count: int = get_conflux_year_count(private_leagues)
                        return await assign_user_veteran_role(conflux_year_count, user)
                    else:
                        return (f'<@{str(user.id)}> Error: No leagues found. '
                                f'Check your privacy settings, or pathofexile.com is down.')
                case 'addleague':
                    for role in user.roles:
                        if role.name == 'League Staff':
                            return append_league(val)
                    return f'<@{str(user.id)}> You do not have permission to use this command.'
                case _:
                    return f'<@{str(user.id)}> Unknown command: {command}, see pinned messages for instructions!'
            # -------- end command handling --------
        else:
            return (f'<@{str(user.id)}> Invalid command structure: {user_input}, '
                    f'command must follow structure: ![command] [value]')
