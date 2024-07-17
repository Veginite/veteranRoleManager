import discord
from lxml import etree


async def assign_user_veteran_role(conflux_year_count: int, user: discord.Message.author) -> str:
    msg: str = ''

    server = user.guild
    tree = etree.parse('roles.xml')
    root = tree.getroot()
    role_ids: list = []
    role_names: list = []
    for e in root:
        role_ids.append(int(e.attrib["id"]))
        role_names.append(str(e.attrib["name"]))

    # the number of roles present in roles.xml
    max_veteran_role_count: int = len(role_ids)

    # conflux_year_count may never exceed max_veteran_role_count
    conflux_year_count = min(conflux_year_count, max_veteran_role_count)

    # if the top role has already been awarded, sass
    if role_ids[max_veteran_role_count - 1] in user.roles:
        return f'The only thing beyond {role_names[max_veteran_role_count - 1]} roles is NON-EXISTENCE!'
    # if the eligible role has already been awarded, be kind
    elif role_ids[conflux_year_count - 1] in user.roles:
        return 'You will be eligible for a new role next year!'
    # the user is eligible for the relevant role, award it and remove all other roles
    else:
        # remove a prior role if they have it
        for n in range(conflux_year_count - 1):
            if role_ids[n] in user.roles:
                await user.remove_roles(server.get_role(role_ids[n]))

        msg = (f'For playing Conflux during {str(conflux_year_count)} years, '
               f'<@{str(user.id)}> has been awarded the following: ')

        await user.add_roles(server.get_role(role_ids[conflux_year_count - 1]))
        msg += f'<@&{str(role_ids[conflux_year_count - 1])}>'

    return msg
