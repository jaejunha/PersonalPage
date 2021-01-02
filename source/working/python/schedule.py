import datetime

CONST_MONTH = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] 
CONST_WEEK = ["월", "화", "수", "목", "금", "토", "일"]
NUM_WEEK = 7

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
    file.write("var sel_row = -1;\n")
    file.write("var sel_col = -1;\n")
    file.write("function select(day, row, col){\n")
    file.write("if (sel_row != -1 && sel_col != -1)\n")
    file.write('$("table tr:nth-child(" + sel_row + ") td:nth-child(" + sel_col + ")").css("background-color", "rgba(255, 255, 255, 0.6)");\n')
    file.write("sel_row = row;\n")
    file.write("sel_col = col;\n")
    file.write('$("table tr:nth-child(" + row + ") td:nth-child(" + col + ")").css("background-color", "rgba(0, 0, 0, 0.3)");\n')
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
    file.write('<table style="width: 100%; height: calc(70% - 50px); border: 1px solid #bcbcbc; table-layout: fixed;">\n')
    start = datetime.date(date.year, date.month, 1)
    if date.month == 12:
        last = (datetime.date(date.year + 1, 1, 1) - datetime.timedelta(days = 1))
    else:
        last = (datetime.date(date.year, date.month + 1, 1) - datetime.timedelta(days = 1))
    file.write('<tr style="font-weight: bold; text-align: center; height: 30px;">\n')
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
    if (start.weekday() == 0) and (last.day == 28):
        for i in range(4):
            file.write('<tr>\n')
            for j in range(NUM_WEEK):
                if cur >= offset:
                    file.write('<td style="padding: 5px; vertical-align: top; background-color: rgba(255, 255, 255, 0.6); cursor: pointer;" onclick="select(%d, %d, %d);">%d</td>\n' % (day, i + 2, j + 1, day))
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
                    file.write('<td style="padding: 5px; vertical-align: top; background-color: rgba(255, 255, 255, 0.6); cursor: pointer; overflow:hidden;" onclick="select(%d, %d, %d);">%d</td>\n' % (day, i + 2, j + 1, day))
                    day += 1
                else:
                    file.write('<td style="padding: 5px; vertical-align: top;"></td>\n')
                cur += 1
            file.write('</tr>\n')
    file.write("</table>")
    file.write('<textarea style="margin-top: 10px; width: 100%; height: calc(30% - 50px); resize:none;"></textarea>')
    file.write("</body>")
    file.write("</html>")
