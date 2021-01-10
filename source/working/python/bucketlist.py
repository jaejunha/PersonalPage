def getBucketlist():
    str = ""

    find = False # <div> 구분선 넣어주기 용
    num_ele = None

    str = ""
    file = open("config/bucketlist.csv", "r")
    for line in file.readlines():
        if len(line) > 0:
            list_line = line.split(",")
            if len(list_line) == 1:
                if find:
                    str += "</table>\n"
                    str += "</div>\n"
                    str += "<br>\n"
                find = True
                num_ele = 0

                str += '<div>\n'
                str += '<span style="font-size:20px;">%s</span>\n' % list_line[0]
                str += '<table style="border: 1px solid #bcbcbc; width: 100%;">\n'
    
            else:
                num_ele += 1
                if num_ele == 1:
                    str += '<tr style="font-weight: bold;">\n'
                    for ele in list_line:
                        str += '<td>%s</td>' % ele.strip()
                    str += '</tr>\n'
                else:
                    str += '<tr style="background-color: rgba(255, 255, 255, 0.6);">\n'
                    for i, ele in enumerate(list_line):
                        if i == 0:
                            str += '<td style="text-align: center;"><img src="img/%s"/></td>' % ele.strip()
                        else:
                            str += '<td>%s</td>' % ele.strip()
                    str += '</tr>\n'

    str += "</table>\n"
    str += "</div>\n"

    return str

def makeBucketHTML():

    file = open("html/bucketlist.html", "w")
    file.write('<meta charset="utf-8">\n')
    file.write("<html>")
    file.write('<link rel="stylesheet" type="text/css" href="css/no_drag.css">\n')
    file.write('<script src="js/logout.js"></script>\n')
    file.write('<body style="margin: 10px">\n')
    file.write('<span style="font-size: 30px;">Bucket List</span>')
    file.write(getBucketlist())
    file.write("</body>\n")
    file.write("</html>\n")
    file.close()
