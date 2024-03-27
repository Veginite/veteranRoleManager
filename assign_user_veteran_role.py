import discord
from lxml import etree


async def assign_user_veteran_role(conflux_year_count: int, user: discord.Message.author) -> str:
    msg: str = 'For playing Conflux during ' + str(
        conflux_year_count) + ' years, <@' + str(user.id) + '> has been awarded the following: '

    server = user.guild
    tree = etree.parse('roles.xml')
    root = tree.getroot()
    role_ids: list = []
    for e in root:
        role_ids.append(int(e.attrib["id"]))

    matches: int = 0
    for role in user.roles:
        if role.id in role_ids:
            matches += 1

    # maximum existing veteran roles are 4
    n_roles_to_add = min(conflux_year_count, 4) - matches

    for n in range(n_roles_to_add):
        s_role = server.get_role(role_ids[matches + n])
        await user.add_roles(s_role)
        msg += '<@&' + str(role_ids[matches + n]) + '>'

    return msg
