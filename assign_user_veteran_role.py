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

    # highest role based on conflux_year_count may never exceed max_veteran_role_count
    highest_role_to_assign = min(conflux_year_count, max_veteran_role_count)

    # get the current role IDs and put them in a list
    user_veteran_roles = [role.id for role in user.roles if role.id in role_ids]

    # if the top role has already been awarded, sass
    if highest_role_to_assign == max_veteran_role_count and role_ids[max_veteran_role_count - 1] in user_veteran_roles:
        msg = f'<@{str(user.id)}> The only thing beyond {role_names[max_veteran_role_count - 1]} roles is NON-EXISTENCE!'
    # if the eligible role has already been awarded, be kind
    elif role_ids[highest_role_to_assign - 1] in user_veteran_roles:
        msg = f'<@{str(user.id)}> You will be eligible for a new role next year!'
    # the user is eligible for the relevant role, award it and remove all other roles
    else:
        # remove prior roles
        for n in range(len(user_veteran_roles)):
            await user.remove_roles(server.get_role(user_veteran_roles[n]))

        msg = (f'For playing Conflux during {str(highest_role_to_assign)} years, '
               f'<@{str(user.id)}> has been awarded the following: ')
        msg += f'<@&{str(role_ids[highest_role_to_assign - 1])}>'

        await user.add_roles(server.get_role(role_ids[highest_role_to_assign - 1]))

    return msg
