from collections import OrderedDict
import net.mapserv as mapserv
import net.stats as st
import itemdb
from utils import encode_str
import mapnames


def stats_repr(*stat_types):
    ps = mapserv.player_stats
    sd = OrderedDict()

    if 'stats' in stat_types:
        sd['stats'] = 'STR:{} AGI:{} VIT:{} INT:{} DEX:{} LUK:{}'.format(
            ps[st.STR], ps[st.AGI], ps[st.VIT], ps[st.INT],
            ps[st.DEX], ps[st.LUK])

    if 'hpmp' in stat_types:
        sd['hpmp'] = 'HP:{}/{} MP:{}/{}'.format(ps[st.HP], ps[st.MAX_HP],
                                                ps[st.MP], ps[st.MAX_MP])

    if 'weight' in stat_types:
        sd['weight'] = 'WG: {}/{}'.format(ps[st.TOTAL_WEIGHT],
                                          ps[st.MAX_WEIGHT])

    if 'points' in stat_types:
        sd['points'] = 'LVL: {} EXP:{}/{} CP:{} SP:{}'.format(
            ps[st.LEVEL], ps[st.EXP], ps[st.EXP_NEEDED],
            ps[st.CHAR_POINTS], ps[st.SKILL_POINTS])

    if 'zeny' in stat_types:
        sd['zeny'] = 'GP:{}'.format(ps[st.MONEY])

    if 'attack' in stat_types:
        sd['attack'] = 'ATK:{} DEF:{} MATK:{} MDEF:{}'.format(
            ps[st.ATK], ps[st.DEF], ps[st.MATK], ps[st.MDEF])

    if 'skills' in stat_types:
        sl = []
        ps = mapserv.player_skills
        skill_names = {339: 'focusing', 45: 'mallard', 350: 'brawling',
                       352: 'speed', 353: 'resist', 354: 'astral',
                       355: 'raging'}

        for s_id, s_v in ps.items():
            if s_v > 0:
                sl.append('{}:{}'.format(skill_names.get(s_id,
                                                         str(s_id)), s_v))

        sd['skills'] = ' '.join(sl)

    return sd


def invlists(max_items=1000):
    inventory = OrderedDict()

    for id_, amount in mapserv.player_inventory.values():
        inventory[id_] = inventory.setdefault(id_, 0) + amount

    lists = []
    data = '\302\202B1'
    i = 0
    for id_, amount in inventory.items():
        i += 1
        if i > max_items:
            i = 0
            lists.append(data)
            data = '\302\202B1'
        data += encode_str(id_, 2)
        data += encode_str(1, 4)
        data += encode_str(amount, 3)

    lists.append(data)
    return lists


def invlists2(max_length=255, source='inventory'):
    inventory = OrderedDict()

    if source == 'inventory':
        source = mapserv.player_inventory
    elif source == 'storage':
        source = mapserv.player_storage
    else:
        return []

    for id_, amount in source.values():
        inventory[id_] = inventory.setdefault(id_, 0) + amount

    lists = []
    data = ''
    for id_, amount in inventory.items():
        s = itemdb.item_name(id_, True) + ', '
        if amount > 1:
            s = str(amount) + ' ' + s
        if len(data + s) > max_length:
            lists.append(data)
            data = ''
        data += s

    lists.append(data[:-2])
    return lists


def player_position():
    pp = mapserv.player_pos
    map_name = mapnames.map_names.get(pp['map'], 'Unknown')
    s = "Map: {} ({}), coor: {}, {}".format(
        map_name, pp['map'], pp['x'], pp['y'])
    return s
