import datetime
import json
import random
from bot_config import GROUP_USE,ABSOLUTE_PATH
import requests
from jieba import posseg
from nonebot import (CommandSession, IntentCommand, NLPSession, get_bot, log,
                     on_command, on_natural_language)
from nonebot import permission as perm
from nonebot.permission import *
import aiocqhttp
from .db import *


# ABSOLUTE_PATH = f"{ABSOLUTE_PATH}"


@on_command('sign_in', aliases=('-群签到','-签到'), only_to_me=False)
async def sign_in(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    user_id = str(session.event.user_id)
    msg = sign_in(user_id)
    await session.finish(msg)


# 签到函数
def sign_in(user_id):
    user_id_sql = str(user_id)
    get_coin = random.randint(1,100)
    get_sage = random.randint(1,4)

    sign_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    sql = "select * from user_info where user_id=" + user_id
    sel = sql_dql(sql)
    if sel[0][8] == sign_time:
        return f"你今天签过到了噢"
    else:
        sql = f"""update user_info
                    set sign_time = '{sign_time}',user_coin = user_coin + {get_coin},user_sage = user_sage + {get_sage}
                    where user_id = '{user_id_sql}';
                """
        sql_dml(sql)
        return f"🐒签到成功并获得了🐒\n金币💰：{get_coin}\n贤者之心💗：{get_sage}"
