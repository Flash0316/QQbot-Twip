import datetime
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from bot_config import GROUP_USE
import requests
from jieba import posseg
from nonebot import (CommandSession, IntentCommand, NLPSession, get_bot, log,
                     on_command, on_natural_language)
from nonebot import permission as perm
from nonebot.permission import *
bot = get_bot()
from .db import *


# select * from user_info order by user_speak_total desc limit 10;


@on_command('speak_rank_top10', aliases=('查看水群排行',), only_to_me=False)
async def _(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    msg = speak_rank_top_10()
    await session.finish(msg)


@on_command('speak_rank_me', aliases=('个人水群排行',), only_to_me=False)
async def _(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    user_id = str(session.event.user_id)
    msg = speak_rank_me(user_id)
    await session.finish(msg)


# 获取发言前十的记录
def speak_rank_top_10():
    sql = """
        select * 
        from(select row_number() over(order by user_speak_total desc) as row_number,* from user_info)
        where row_number <= 10
    """
    data = sql_dql(sql)
    msg = f"🙈发言光荣榜🙈\n__________________\n"
    for item in data:
        rank = item[0]
        name = item[1]
        id = item[2]
        num = item[3]
        num_emoji = rank_emoji(rank)
        # 0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟🥇🥈🥉
        msg += f"{num_emoji}{name}({id})🗣️:{num}\n"
    msg += f"这些👨都4️⃣大💦👾"
    return msg


def speak_rank_me(user_id):
    user_id_sql = str(user_id)
    sql = f"""
        select *
        from(
        select row_number() over(order by user_speak_total desc) as row_number,* from user_info
        )
        where user_id = '{user_id_sql}'
    """
    data = sql_dql(sql)
    rank = data[0][0]
    sql = "select count(*) from user_info"
    data = sql_dql(sql)
    total = data[0][0]
    msg = f"🙈你的发言情况🙈\n__________________\n"
    msg += f"在{total}位用户中，排名第{rank}"
    return msg


def rank_emoji(num):
    emoji_list = ['0️⃣','🥇','🥈','🥉','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
    emoji = emoji_list[num]
    return emoji