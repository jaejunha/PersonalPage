import datetime
import os

CONST_SAT = 5

def saveStockDic(dic):
    
    try:
        loss = int(dic["loss"].replace(",", ""))
    except:
        loss = 0
    try:
        gain = int(dic["gain"].replace(",", ""))
    except:
        gain = 0
    try:
        withdraw = int(dic["withdraw"].replace(",", ""))
    except:
        withdraw = 0
    try:
        available = int(dic["available"].replace(",", ""))
    except:
        available = 0
    
    file = open("output/stock/result/" + dic["date"] + ".csv", "w")
    file.write("%d, %d, %d, %d" % (loss, gain, withdraw, available))
    file.close()

    return dic["date"]

def avoidWeekend(date, delta):
    if delta == 0:
        week = date
        while week.weekday() >= CONST_SAT:
            week -= datetime.timedelta(days = 1)

    elif delta == -1:
        week = date
        week -= datetime.timedelta(days = 1)
        while week.weekday() >= CONST_SAT:
            week -= datetime.timedelta(days = 1)

    elif delta == 1:
        if date.weekday() >= CONST_SAT - 1:
            date += datetime.timedelta(days = (7 - date.weekday()))
        else:
            date += datetime.timedelta(days = 1)


        if datetime.datetime.now().day < date.day:
            week = datetime.datetime.now()
        else:
            week = date

        week = avoidWeekend(week, 0)

    return week

def loadScreenshot(date):
    path = "output/stock/screenshot/"

    for file in os.listdir("output/stock/screenshot"):
        if file.startswith(date):
            path += file
            break

    return path

def getResult(date):

    dic = {}
    try:
        file = open("output/stock/result/%s.csv" % date)
        list_data = file.readlines()[0].split(",")

        dic["loss"] = int(list_data[0].strip())
        dic["gain"] = int(list_data[1].strip())
        dic["withdraw"] = int(list_data[2].strip())
        dic["available"] = int(list_data[3].strip())
        dic["total"] = dic["loss"] + dic["gain"]

    except FileNotFoundError:
        dic["total"] = 0
        dic["loss"] = 0
        dic["gain"] = 0
        dic["withdraw"] = 0
        dic["available"] = 0

    return dic

def makeStockHTML(date):
    
    date = avoidWeekend(date, 0)
    str_date = date.strftime("%Y-%m-%d") 

    file = open("html/stock.html", "w")
    file.write('<meta charset="utf-8">\n')
    file.write("<html>")
    file.write('<link rel="stylesheet" type="text/css" href="css/no_drag.css">\n')
    file.write('<body style="margin: 10px">\n')
    file.write('<div style="display: table; text-align: center; width: 100%;">\n')
    file.write('<form action="/stock" method="get" target="inner">\n')
    file.write('<input type="hidden" name="date" value="%s"/>\n' % (avoidWeekend(date, -1).strftime("%Y-%m-%d")))
    file.write('<button style="display: table-cell; width:0; height:0; border-style:solid; border-width:20px;border-color:transparent #555 transparent transparent; background-color: rgba(0, 0, 0, 0); cursor: pointer;"></button>\n')
    file.write("</form>\n")
    file.write('<span style="display: table-cell; font-size: 30px; vertical-align: middle; width: 30%%;">%s</span>\n' % str_date)
    file.write('<form action="/stock" method="get" target="inner">\n')
    file.write('<input type="hidden" name="date" value="%s"/>\n' % (avoidWeekend(date, +1).strftime("%Y-%m-%d")))
    file.write('<button style="display: table-cell; width:0; height:0; border-style:solid; border-width:20px;border-color:transparent transparent transparent #555; background-color: rgba(0, 0, 0, 0); cursor: pointer;"></button>\n')
    file.write("</form>\n")
    file.write("</div>\n")
    file.write('<div style="height: calc(60% - 80px);">\n')
    file.write('<img style="width: 100%%; height: 100%%; object-fit: contain;" src="%s"/>\n' % loadScreenshot(str_date))
    file.write("</div>\n")
    file.write('<form method="post" action="stock" style="text-align: center; margin-top: 5px;" enctype="multipart/form-data">\n')
    file.write('<input type="file" name="test" accept="image/*">\n')
    file.write('<input type="hidden" name="date" value="%s">\n' % str_date)
    file.write('<input type="submit">\n')
    file.write("</form>\n")
    dic_res = getResult(str_date)
    file.write('<form action="/stock" method="post" target="inner" style="width: 100%; height: calc(40% - 80px);">\n')
    file.write('<div style="width: 100%; height: 100%; border: 1px solid #bcbcbc; background-color: rgba(255, 255, 255, 0.6); border-radius: 2px;">\n')
    if dic_res["total"] != 0:
        file.write('<span style="display: inline-block; width: 100px;">하루 수익</span><span>%s (%.2f%%)</span><br>\n' % (format(dic_res["total"], ","), (dic_res["total"] / dic_res["available"] * 100.0)))
        file.write('<span style="display: inline-block; width: 100px;">하루 순손익</span><span>%s (%.2f%%)</span><br>\n' % (format(dic_res["gain"], ","), (dic_res["gain"] / dic_res["available"] * 100.0)))
    else:
        file.write('<span style="display: inline-block;">하루 수익</span><br>\n')
        file.write('<span style="display: inline-block;">하루 순손익</span><br>\n')
    file.write("<hr>\n")
    file.write("<div>\n")
    file.write('<span style="display: inline-block; width: 100px;">손절</span>\n')
    file.write('<input style="width: 100px; text-align: right;" name="loss" type="text" value="%s">\n' % format(dic_res["loss"], ","))
    if dic_res["total"] != 0:
        file.write('<span style="display: inline-block; width: 60px; text-align: right">%.2f%%</span>\n' % (dic_res["loss"] / dic_res["total"] * 100))
    file.write("</div>\n")
    file.write('<div style="width: 100%;">\n')
    file.write('<span style="display: inline-block; width: 100px;">실현손익</span>\n')
    file.write('<input style="width: 100px; text-align: right;" name="gain" type="text" value="%s">\n' % format(dic_res["gain"], ","))
    if dic_res["total"] != 0:
        file.write('<span style="display: inline-block; width: 60px; text-align: right">%.2f%%</span>\n' % ((dic_res["gain"] - dic_res["withdraw"]) / dic_res["total"] * 100))
    file.write("</div>\n")
    file.write('<div style="width: 100%;">\n')
    file.write('<span style="display: inline-block; width: 100px;">인출</span>\n')
    file.write('<input style="width: 100px; text-align: right;" name="withdraw" type="text" value="%s">\n' % format(dic_res["withdraw"], ","))
    if dic_res["total"] != 0:
        file.write('<span style="display: inline-block; width: 60px; text-align: right">%.2f%%</span>\n' % (dic_res["withdraw"] / dic_res["total"] * 100))
    file.write("</div>\n")
    file.write('<div style="width: 100%;">\n')
    file.write('<span style="display: inline-block; width: 100px;">예수금</span>\n')
    file.write('<input style="width: 100px; text-align: right;" name="available" type="text" value="%s">\n' % format(dic_res["available"], ","))
    file.write("</div>\n")
    file.write('<input type="hidden" name="date" value="%s">\n' % str_date)
    file.write("</div>\n")
    file.write('<div style="width: 100%; text-align: right; margin-top: 10px">\n')
    file.write('<button type="submit">적용하기</button>\n')
    file.write("</div>\n")
    file.write("</form>\n")
    file.write("</body>\n")
    file.write("</html>\n")
    file.close()
