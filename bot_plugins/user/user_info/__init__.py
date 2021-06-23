import datetime
import json
import random
from bot_config import GROUP_USE
import requests
from jieba import posseg
from nonebot import (CommandSession, IntentCommand, NLPSession, get_bot, log,
                     on_command, on_natural_language)
from nonebot import permission as perm
from nonebot.permission import *
import aiocqhttp
from .db import *
from .level_info import *
bot = get_bot()


"""
💀❤️💛💚💙💜💔💕💞💓💗💖💘💝💟
💰💳💎🔨🗡⚔🛡☠💊🔖🏷✉️📦📕🔒🐵
🐵🙈🙉🙊🐒🐤🐣🐥🐺🐗🐴🦄🐍⚪🐮
🔘⚪️⚫️☑️🔴🔵🔶🔷◼️◻️⬛️⬜️♦️
"""


@on_command('user_info_new', aliases=('-个人信息'), only_to_me=False)
async def user_info_new(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    user_id = str(session.event.user_id)
    sql = "select * from user_info where user_id=" + user_id
    try:
        dta = sql_dql(sql)
    except IndexError:
        await session.send("语法错误")
    if dta == []:
        await session.send('错误，没有这组数据')
    else:
        user_name = dta[0][0]
        user_talk = dta[0][2]
        user_coin = dta[0][6]
        user_sage = dta[0][7]
        user_level = find_level_name(user_talk)
        msg = f"亲爱的{user_name}，你的基本信息如下~\n———————————————\n"
        msg += f"🔖:{user_level}\n🙊:{user_talk}\n💰:{user_coin}\n💗:{user_sage}"
        await session.send(msg)


@on_command('get_luck_num2', aliases=('-求签'), only_to_me=False)
async def get_luck_num2(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    user_id = str(session.event.user_id)
    msg = get_luck_num(user_id)
    await session.send(msg)


# 签到函数
def get_luck_num(user_id):
    user_id_sql = str(user_id)
    luck_num = random.randint(1,100)
    luck_animal = find_animal(luck_num)
    user_luck_today = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    sql = "select * from user_info where user_id=" + user_id
    sel = sql_dql(sql)
    if sel[0][5] == user_luck_today:
        luck_num = sel[0][4]
        luck_animal = find_animal(luck_num)
        return f"🐒你今天的运势如下🐒\n📕幸运数字：{luck_num}\n📕幸运动物：{luck_animal}"
    else:
        sql = f"""update user_info
                    set user_luck_today = '{user_luck_today}',user_luck_num = {luck_num}
                    where user_id = '{user_id_sql}';
                """
        sql_dml(sql)
        return f"🐒你今天的运势如下🐒\n📕幸运数字：{luck_num}\n📕幸运动物：{luck_animal}"



# 发言次数监听器
@bot.on_message('group')
async def handle_group_message(event: aiocqhttp.Event):
    user_id = str(event.user_id)

    # 查找该用户
    sql = "select * from user_info where user_id=" + user_id
    sel = sql_dql(sql)
    if sel:
        old_user_add(user_id)
    else:
        inf = await bot.get_stranger_info(user_id=event.user_id)
        user_name = inf['nickname']
        new_user_add(user_id,user_name)


# 新用户添加
def new_user_add(user_id,user_name):
    user_id_sql = str(user_id)
    user_speak_total = "0"
    user_speak_today = "False"
    user_luck_num = "50"
    user_luck_today = "False"
    user_coin = "0"
    user_sage = "0"

    sql = "insert into user_info (user_name,user_id,user_speak_total,"
    sql += "user_speak_today,user_luck_num,user_luck_today,user_coin,user_sage,sign_time)VALUES("
    sql += f"'{user_name}',{user_id_sql},{user_speak_total},{user_speak_today}"
    sql += f",{user_luck_num},{user_luck_today},{user_coin},{user_sage},'0')"
    sql_dml(sql)


# 老用户添加发言
def old_user_add(user_id):
    speak_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    user_id_sql = str(user_id)
    sql = f"""
    update user_info
    set user_speak_today = '{speak_time}',user_speak_total = user_speak_total + 1
    where user_id = '{user_id_sql}';
    """
    sql_dml(sql)



