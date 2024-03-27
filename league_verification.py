from lxml import etree


def get_league_verification(league_name: str) -> bool:
    tree = etree.parse('leagues.xml')
    root = tree.getroot()
    for x in root:
        if x.text == league_name:
            return True

    return False


def append_league(league_name: str) -> str:

    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    tree = etree.parse('leagues.xml', parser=parser)
    root = tree.getroot()
    e: etree.Element = etree.Element('league')
    e.text = league_name
    root.append(e)
    etree.indent(root, '\t')
    tree.write('leagues.xml', encoding='utf-8', xml_declaration=True)

    return 'Added league: ' + league_name
