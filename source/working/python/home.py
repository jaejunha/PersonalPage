def parseHomeInput(dic_input):
	memo = dic_input["home"]

	return memo 

def saveMemo(content):
	file = open("memo.txt", "w")
	file.write(content)
	file.close()

def loadMemo():
	content = ""

	file = open("memo.txt", "r")
	for line in file.readlines():
		content += line
	file.close()

	return content

def makeHomeHTML():
    content = loadMemo()
	
    file = open("html/home.html", "w")
    file.write('<html style="overflow-x: hidden;">\n')
    file.write('<link rel="stylesheet" type="text/css" href="css/no_drag.css">\n')
    file.write('<script src="js/logout.js"></script>\n')
    file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n')
    file.write("<script>\n")
    file.write('function adjustImage(){\n')
    file.write('var text = $("div:nth-of-type(1) div");\n')
    file.write('var width = $("div").width();\n')
    file.write('var height = $("div:nth-of-type(1)").height() - $("div:nth-of-type(1) span").height() - text.height() - 10;\n')
    file.write('var img = $("img");\n')
    file.write('if (width > height) {\n')
    file.write('img.width(height);\n')
    file.write('img.height(height);\n')
    file.write('text.css("margin", 0);\n')
    file.write('text.css("margin-left", 10);\n')
    file.write('}else{\n')
    file.write('img.width(width);\n')
    file.write('img.height(width);\n')
    file.write('text.css("margin", 0);\n')
    file.write('text.css("margin-top", 10);\n')
    file.write('}\n')
    file.write("}\n")
    file.write('$(document).ready(function(){\n')
    file.write('adjustImage();\n')
    file.write("});\n")
    file.write('$(window).resize(function(){\n')
    file.write('adjustImage();\n')
    file.write('});\n')
    file.write("</script>")
    file.write('<body style="margin: 10px;">\n')
    file.write('<meta charset="utf-8">\n')
    file.write('<div style="width: 100%; height: 60%; float: left;">\n')
    file.write('<span style="font-size: 30px;">My Story</span><br>\n')
    file.write('<img src="img/main.gif" style="float: left;"/>\n')
    file.write('<div style="float: left;">임시 텍스트</div>\n')
    file.write('</div>')
    file.write('<form action="/home" method="post" target="inner" style="margin-top: 10px; margin-bottom: 0; width: 100%; height: 40%;">\n')
    file.write('<span style="font-size:30px;">Memo</span>')
    file.write('<textarea name="home" rows="10" style="width: 100%%; height: calc(100%% - 90px); resize: none;">%s</textarea>' % content)
    file.write('<div style="width: 100%; text-align: right; margin-top: 10px;">\n')
    file.write('<button type="submit">적용하기</button>\n')
    file.write("</div>\n")
    file.write("</form>\n")
    file.write("</body>\n")
    file.write("</html>")
    file.close()
	
