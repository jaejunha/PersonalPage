import datetime
import os

CONST_MONTH = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] 
CONST_WEEK = ["월", "화", "수", "목", "금", "토", "일"]
NUM_WEEK = 7

def parseScheduleInput(raw_input):

    list_input = raw_input.split("&")
    date = int(list_input[0].split("=")[1].strip())
    content = list_input[1].split("=")[1].strip()
    ym = int(date / 100)
    day = date % 100

    return ym, day, content

def loadSchedule(ym, last):
    dic = {}
    str = ""

    folder_name = "schedule/%d" % ym
    if os.path.isdir(folder_name):
        for file_name in os.listdir(folder_name):
            content = ""
            file = open(folder_name + "/" + file_name, "r")
            for line in file.readlines():
                content += line
            dic[int(file_name.split(".")[0])] = content

    str += "<script>\n"
    str += 'for (var i = 0; i <= %d; ++i){\n' % last
    str += 'list_con[i] = "";\n'
    str += "}"
    for day in dic.keys():
        list_line = dic[day].split("\n")
        if len(list_line) == 1:
            str += 'list_con[%d] = "%s";\n' % (day, dic[day])
        else:
            for line in list_line:
                str += 'list_con[%d] += "%s\\n";\n' % (day, line)
    str += "</script>"

    return dic, str

def saveSchedule(ym, day, content):
        
        folder_name = str(ym)

        os.chdir("schedule")
        if os.path.isdir(folder_name) is False:
            os.system("mkdir %s" % folder_name)

        file_name = "%s/%d.txt" % (folder_name, day)
        file = open(file_name, "w")
        file.write(content)
        file.close()

        os.chdir("../")

def getOptionTD(height, year, month, day, row, col):
    str = 'style="overflow:hidden; text-overflow: ellipsis; white-space: nowrap; padding: 5px; height: %f%%; vertical-align: top; background-color: rgba(255, 255, 255, 0.6); cursor: pointer;" onclick="select(%d, %d, %d, %d, %d);"' % (height, year, month, day, row, col)
    return str
 

def makeScheduleHTML(date):

    list_week = []
    for i in range(NUM_WEEK):
        list_week.append([])

    file = open("html/schedule.html", "w")
    file.write('<meta charset="utf-8">\n')
    file.write("<html>\n")
    file.write("<head>\n")
    file.write('<link rel="stylesheet" type="text/css" href="css/no_drag.css">\n')
    file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n')
    file.write("<script>\n")
    file.write("var list_con = new Array();\n")
    file.write("var sel_row = -1;\n")
    file.write("var sel_col = -1;\n")
    file.write("function select(year, month, day, row, col){\n")
    file.write("if (sel_row != -1 && sel_col != -1)\n")
    file.write('$("table tr:nth-child(" + sel_row + ") td:nth-child(" + sel_col + ")").css("background-color", "rgba(255, 255, 255, 0.6)");\n')
    file.write("sel_row = row;\n")
    file.write("sel_col = col;\n")
    file.write('$("table tr:nth-child(" + row + ") td:nth-child(" + col + ")").css("background-color", "rgba(0, 0, 0, 0.3)");\n')
    file.write('$("input[name=ymday]").val(year * 10000 + month * 100 + day);\n')
    file.write('$("textarea").text(list_con[day]);\n')
    file.write('$("button").attr("disabled", false);\n')
    file.write("}\n")
    file.write("</script>\n")
    file.write("</head>\n")
    file.write('<body style="margin: 10px">\n')
    file.write('<div style="display: table; text-align: center; width: 100%;">\n')
    file.write('<form action="/schedule" method="get" target="inner">\n')
    if date.month == 1:
        file.write('<input type="hidden" name="date" value="%s"/>\n' % (datetime.date(date.year - 1, 12, 1).strftime("%Y-%m-%d")))
    else:
        file.write('<input type="hidden" name="date" value="%s"/>\n' % (datetime.date(date.year, date.month - 1, 1).strftime("%Y-%m-%d")))
    file.write('<button style="display: table-cell; width:0; height:0; border-style:solid; border-width:20px;border-color:transparent #555 transparent transparent; background-color: rgba(0, 0, 0, 0); cursor: pointer;"></button>\n')
    file.write("</form>\n")
    file.write('<span style="display: table-cell; font-size: 30px; vertical-align: middle; width: 30%%;">%s %4d</span>\n' % (CONST_MONTH[date.month - 1], date.year))
    file.write('<form action="/schedule" method="get" target="inner">\n')
    if date.month == 12:
        file.write('<input type="hidden" name="date" value="%s"/>\n' % (datetime.date(date.year + 1, 1, 1).strftime("%Y-%m-%d")))
    else:
        file.write('<input type="hidden" name="date" value="%s"/>\n' % (datetime.date(date.year, date.month + 1, 1).strftime("%Y-%m-%d")))
    file.write('<button style="display: table-cell; width:0; height:0; border-style:solid; border-width:20px;border-color:transparent transparent transparent #555; background-color: rgba(0, 0, 0, 0); cursor: pointer;"></button>\n')
    file.write("</form>\n")
    file.write("</div>\n")
    file.write('<table style="width: 100%; height: calc(70% - 55px); border: 1px solid #bcbcbc; table-layout: fixed;">\n')
    start = datetime.date(date.year, date.month, 1)
    if date.month == 12:
        last = (datetime.date(date.year + 1, 1, 1) - datetime.timedelta(days = 1))
    else:
        last = (datetime.date(date.year, date.month + 1, 1) - datetime.timedelta(days = 1))
    file.write('<tr style="font-weight: bold; text-align: center; height: 10%;">\n')
    for i in range(NUM_WEEK):
        if i < 5:
            file.write('<td>%s</td>\n' % CONST_WEEK[i])
        elif i == 5:
            file.write('<td style="color: #88f;">%s</td>\n' % CONST_WEEK[i])
        else:
            file.write('<td style="color: #f88;">%s</td>\n' % CONST_WEEK[i])
    file.write('</tr>\n')
    offset = start.weekday()
    cur = 0
    day = 1
    dic_content, str_script = loadSchedule(start.year * 100 + start.month, last.day)
    file.write(str_script)
    if (start.weekday() == 0) and (last.day == 28):
        for i in range(4):
            file.write('<tr">\n')
            for j in range(NUM_WEEK):
                if cur >= offset:
                    if day in dic_content.keys():
                        file.write('<td %s>%d<div style="overflow:hidden; text-overflow: ellipsis;">%s</div></td>\n' % (getOptionTD((90 / 4), start.year, start.month, day, i + 3, j + 1), day, dic_content[day]))
                    else:
                        file.write('<td %s>%d</td>\n' % (getOptionTD((90 / 4), start.year, start.month, day, i + 3, j + 1), day))
                    day += 1
                else:
                    file.write('<td style="padding: 5px; vertical-align: top;"></td>\n')
                cur += 1
            file.write('</tr>\n')
    else:
        for i in range(5):
            file.write('<tr>\n')
            for j in range(NUM_WEEK):
                if cur >= offset:
                    if day in dic_content.keys():
                        file.write('<td %s>%d<div style="overflow:hidden; text-overflow: ellipsis;">%s</div></td>\n' % (getOptionTD((90 / 5), start.year, start.month, day, i + 3, j + 1), day, dic_content[day]))
                    else:
                        file.write('<td %s>%d</td>\n' % (getOptionTD((90 / 5), start.year, start.month, day, i + 3, j + 1), day))
                    day += 1
                else:
                    file.write('<td style="padding: 5px; vertical-align: top;"></td>\n')
                cur += 1
            file.write('</tr>\n')
    file.write("</table>")
    file.write('<form action="/schedule" method="post" target="inner">\n')
    file.write('<input name="ymday" style="display: none;"></input>\n')
    file.write('<textarea name="schedule" style="margin-top: 10px; width: 100%; height: calc(30% - 55px); resize:none;"></textarea>\n')
    file.write('<div style="width: 100%; text-align: right; margin-top: 10px">')
    file.write('<button type="submit" disabled>적용하기</button>\n')
    file.write('</div>\n')
    file.write("</form>")
    file.write("</body>")
    file.write("</html>")
