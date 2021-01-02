import datetime

CONST_SAT = 5

def avoidWeekend(date, delta):
    if delta == -1:
        week = date
        week -= datetime.timedelta(days = 1)
        while week.weekday() >= CONST_SAT:
            week -= datetime.timedelta(days = 1)

    elif delta == 1:
        if datetime.datetime.now() < date + datetime.timedelta(days = 1):
            week = datetime.datetime.now()
        else:
            week = date + datetime.timedelta(days = 1)

        while week.weekday() >= CONST_SAT:
            week -= datetime.timedelta(days = 1)

    return week

def makeStockHTML(date):

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
    file.write('<span style="display: table-cell; font-size: 30px; vertical-align: middle; width: 30%%;">%s</span>\n' % date.strftime("%Y-%m-%d"))
    file.write('<form action="/stock" method="get" target="inner">\n')
    file.write('<input type="hidden" name="date" value="%s"/>\n' % (avoidWeekend(date, +1).strftime("%Y-%m-%d")))
    file.write('<button style="display: table-cell; width:0; height:0; border-style:solid; border-width:20px;border-color:transparent transparent transparent #555; background-color: rgba(0, 0, 0, 0); cursor: pointer;"></button>\n')
    file.write("</form>\n")
    file.write("</div>\n")
    file.write('<form method="post" action="stock" enctype="multipart/form-data">\n')
    file.write('<input type="file" name="test" accept="image/*">\n')
    file.write('<input type="submit">\n')
    file.write("</form>\n")
    file.write("</body>\n")
    file.write("</html>\n")
    file.close()
