import datetime



# 获取机器人诞生时间间隔
def Q7_get_time_lr_botmade():
    nowTime = datetime.datetime.now()

    oldTime = datetime.datetime.strptime('2021-01-21 21:48:00','%Y-%m-%d %H:%M:%S')
    time_lr = nowTime-oldTime

    msg = f'{time_lr.days}天{int(time_lr.seconds/3600)}小时{int(time_lr.seconds/60%60)}分钟{int(time_lr.seconds%60)}秒'
    return msg


# 获取发言统计时间间隔
def Q7_get_time_lr_talk():
    nowTime = datetime.datetime.now()

    oldTime = datetime.datetime.strptime('2021-02-12 00:00:00','%Y-%m-%d %H:%M:%S')
    time_lr = nowTime-oldTime

    msg = f'{time_lr.days}天{int(time_lr.seconds/3600)}小时{int(time_lr.seconds/60%60)}分钟{int(time_lr.seconds%60)}秒'
    return msg
