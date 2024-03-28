import discord
from lxml import etree


async def assign_user_veteran_role(conflux_year_count: int, user: discord.Message.author) -> str:
    msg: str = ''
    max_veteran_role_count: int = 4

    server = user.guild
    tree = etree.parse('roles.xml')
    root = tree.getroot()
    role_ids: list = []
    for e in root:
        role_ids.append(int(e.attrib["id"]))

    # find the roles the user already has and exclude them, mainly to support potential role hierarchy holes
    matches = [x.id for x in user.roles if x.id in role_ids]
    for n in range(len(matches)):
        role_ids.remove(matches[n])

    # maximum existing veteran roles are 4
    n_roles_to_add = min(conflux_year_count, max_veteran_role_count) - (4 - len(role_ids))
    if len(role_ids) == 0:
        return 'The only thing beyond 4 roles is NON-EXISTENCE!'
    elif n_roles_to_add == 0:
        return 'You will be eligible for a new role next year!'


    msg = 'For playing Conflux during ' + str(
        conflux_year_count) + ' years, <@' + str(user.id) + '> has been awarded the following: '

    for n in range(n_roles_to_add):
        s_role = server.get_role(role_ids[n])
        await user.add_roles(s_role)
        msg += '<@&' + str(role_ids[n]) + '>'

    return msg
