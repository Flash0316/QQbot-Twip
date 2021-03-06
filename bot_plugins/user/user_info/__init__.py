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
๐โค๏ธ๐๐๐๐๐๐๐๐๐๐๐๐๐
๐ฐ๐ณ๐๐จ๐กโ๐กโ ๐๐๐ทโ๏ธ๐ฆ๐๐๐ต
๐ต๐๐๐๐๐ค๐ฃ๐ฅ๐บ๐๐ด๐ฆ๐โช๐ฎ
๐โช๏ธโซ๏ธโ๏ธ๐ด๐ต๐ถ๐ทโผ๏ธโป๏ธโฌ๏ธโฌ๏ธโฆ๏ธ
"""


@on_command('user_info_new', aliases=('-ไธชไบบไฟกๆฏ'), only_to_me=False)
async def user_info_new(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    user_id = str(session.event.user_id)
    sql = "select * from user_info where user_id=" + user_id
    try:
        dta = sql_dql(sql)
    except IndexError:
        await session.send("่ฏญๆณ้่ฏฏ")
    if dta == []:
        await session.send('้่ฏฏ๏ผๆฒกๆ่ฟ็ปๆฐๆฎ')
    else:
        user_name = dta[0][0]
        user_talk = dta[0][2]
        user_coin = dta[0][6]
        user_sage = dta[0][7]
        user_level = find_level_name(user_talk)
        msg = f"ไบฒ็ฑ็{user_name}๏ผไฝ ็ๅบๆฌไฟกๆฏๅฆไธ~\nโโโโโโโโโโโโโโโ\n"
        msg += f"๐:{user_level}\n๐:{user_talk}\n๐ฐ:{user_coin}\n๐:{user_sage}"
        await session.send(msg)


@on_command('get_luck_num2', aliases=('-ๆฑ็ญพ'), only_to_me=False)
async def get_luck_num2(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    user_id = str(session.event.user_id)
    msg = get_luck_num(user_id)
    await session.send(msg)


# ็ญพๅฐๅฝๆฐ
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
        return f"๐ไฝ ไปๅคฉ็่ฟๅฟๅฆไธ๐\n๐ๅนธ่ฟๆฐๅญ๏ผ{luck_num}\n๐ๅนธ่ฟๅจ็ฉ๏ผ{luck_animal}"
    else:
        sql = f"""update user_info
                    set user_luck_today = '{user_luck_today}',user_luck_num = {luck_num}
                    where user_id = '{user_id_sql}';
                """
        sql_dml(sql)
        return f"๐ไฝ ไปๅคฉ็่ฟๅฟๅฆไธ๐\n๐ๅนธ่ฟๆฐๅญ๏ผ{luck_num}\n๐ๅนธ่ฟๅจ็ฉ๏ผ{luck_animal}"



# ๅ่จๆฌกๆฐ็ๅฌๅจ
@bot.on_message('group')
async def handle_group_message(event: aiocqhttp.Event):
    user_id = str(event.user_id)

    # ๆฅๆพ่ฏฅ็จๆท
    sql = "select * from user_info where user_id=" + user_id
    sel = sql_dql(sql)
    if sel:
        old_user_add(user_id)
    else:
        inf = await bot.get_stranger_info(user_id=event.user_id)
        user_name = inf['nickname']
        new_user_add(user_id,user_name)


# ๆฐ็จๆทๆทปๅ 
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


# ่็จๆทๆทปๅ ๅ่จ
def old_user_add(user_id):
    speak_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    user_id_sql = str(user_id)
    sql = f"""
    update user_info
    set user_speak_today = '{speak_time}',user_speak_total = user_speak_total + 1
    where user_id = '{user_id_sql}';
    """
    sql_dml(sql)



