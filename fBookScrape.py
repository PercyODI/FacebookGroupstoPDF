from facepy import GraphAPI, exceptions
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import CondPageBreak, PageBreak, Flowable, Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from datetime import datetime
import time

class MCLine(Flowable):
    """
    Line flowable --- draws a line in a flowable

	http://two.pairlisdata.net/pipermail/reportlab-users/2005-February/003695.html

    """
 
    #----------------------------------------------------------------------
    def __init__(self, width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height
 
    #----------------------------------------------------------------------
    def __repr__(self):
        return "Line(w=%s)" % self.width
 
    #----------------------------------------------------------------------
    def draw(self):
        """
        draw the line
        """
        self.canv.line(0, self.height, self.width, self.height)

def get_graphAPI():
	graph = GraphAPI("CAACEdEose0cBAEQn5MiL537sBMILYu9ItT9ImPoc6JgGY4LYfvalNPN3fx8jAO66ncaNNZCvOyApv4ySQWoJsWQ0zRY8wKcbPo6EZBgcS5D1UWqTGzR09jZChmoq4TK2HZBWcrT7m1Ga2K10hjzZB8pCkjNpZA2DC9CteZClm3iYzpOexlvn07dx4nZCSqEXPmOeJ2SZBWKZC4vTjhZAFM6dT1y")
	# response = graph.get('/175579742455688/feed', page=True)
	response = graph.get('175579742455688/feed?since=2011-01-01T01:00:00&until=2012-01-01T01:00:00', page=True)
	return response

def get_title_desc():
	graph = GraphAPI("CAACEdEose0cBAEQn5MiL537sBMILYu9ItT9ImPoc6JgGY4LYfvalNPN3fx8jAO66ncaNNZCvOyApv4ySQWoJsWQ0zRY8wKcbPo6EZBgcS5D1UWqTGzR09jZChmoq4TK2HZBWcrT7m1Ga2K10hjzZB8pCkjNpZA2DC9CteZClm3iYzpOexlvn07dx4nZCSqEXPmOeJ2SZBWKZC4vTjhZAFM6dT1y")
	response = graph.get('/175579742455688')
	return response

def hello_pdf(page):
 	def hello(c):
 		c.drawString(100,100,"Hello World")
 	c = canvas.Canvas("hello.pdf", pagesize=(612.0, 792.0))
 	hello(c)
 	c.showPage()
 	c.save()
 
def createCanvas(title, description):
	doc, story = SimpleDocTemplate("hello2.pdf", pagesize=letter,
							  rightMargin=72, leftMargin=72,
							  topMargin=72, bottomMargin=72), []
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='titler', fontSize=24, leading=26, alignment=TA_CENTER))
	styles.add(ParagraphStyle(name='description', alignment=TA_JUSTIFY, borderWidth=1, borderColor="black", borderPadding=2, borderRadius=10))
	story.append(Paragraph(title, styles['titler']))
	story.append(Spacer(1, 12))
	story.append(Paragraph(description, styles['description']))
	story.append(Spacer(1, 12))
	return doc, story

def draw_page(story, page):
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='post', leftIndent=10, allowWidows=0, borderWidth=1, borderColor="black", borderPadding=2))
	styles.add(ParagraphStyle(name='postName', allowWidows=0, borderWidth=1, borderColor="black", borderPadding=2))
	styles.add(ParagraphStyle(name='comment', leftIndent=25, rightIndent=25, borderWidth=1, borderColor="black", borderPadding=2))
	styles.add(ParagraphStyle(name='commentName', leftIndent=15, rightIndent=25, borderWidth=1, borderColor="black", borderPadding=2, borderRadius=2))
	line = MCLine(500)
	try:
		for i in page['data']:
			pname = i['from']['name'].encode('ascii', 'ignore')
			ptext = i['message'].encode('ascii', 'ignore').replace("\n", '<br />\n')
			ptime = datetime.strptime(i['created_time'], "%Y-%m-%dT%H:%M:%S+0000")
			pname = pname + " on " + str(ptime.date())
			story.append(Paragraph(pname, styles["postName"]))
			story.append(Spacer(1, 4.5))
			story.append(Paragraph(ptext, styles["post"]))
			story.append(Spacer(1, 4.5))
			try:
				for j in i['comments']['data']:
					pname = j['from']['name'].encode('ascii', 'ignore')
					ptext = j['message'].encode('ascii', 'ignore').replace("\n", '<br />\n')
					story.append(Paragraph(pname, styles["commentName"]))
					story.append(Spacer(1, 4.5))
					story.append(Paragraph(ptext, styles["comment"]))
					story.append(Spacer(1, 4.5))
					
			except KeyError:
		 		print "Key Error in draw_page"
			story.append(Spacer(1, 12))
			
			# story.append(line)
	except KeyError:
		print "Invalid Message"

# def draw_page(canv, page, counter):
# 	width, height = letter
# 	styleSheet = getSampleStyleSheet()
# 	style = styleSheet['BodyText']
#  	aW = 412
#  	aH = 692
#  	for i in page['data']:
#  		p=Paragraph(i['message'].encode('ascii', 'ignore').replace("\n", '<br />\n'), style)
#  		w, h = p.wrap(aW, aH)
#  		p.drawOn(canv, 100, aH)
#  		aH = aH - h
#  	canv.showPage()



# messages are in response['data'][0]['message']
# comments are in response['data'][0]['comments']['data'][0]['message']
# 	to find number of comments, use len(response['data'][0]['comments']['data'][0])

pages = get_graphAPI()
title_desc = get_title_desc()
doc, Story = createCanvas(title_desc['name'], title_desc['description'])
# try:
#for page in pages:
for page in pages:
	# page = pages.next()
	draw_page(Story, page)
	try:
		for i in page['data']:
			print i['message']
	except KeyError:
		pass
# except exceptions.OAuthError, error, StopIteration:
# 	if error.code == 803:
# 		print "Page does not exist"
# 	elif error.code == 2:
# 		print "Unexpected error occured"
# 	elif StopIteration:

doc.build(Story)


# for x in range(1):
# 	page = pages.next()
# 	try:
# 		for j in range(len(page['data'])):
# 			print "****************************************************"
# 			print "(" + page['data'][j]['created_time'] + ")"
# 			print page['data'][j]['message']
# 			for i in range(len(page['data'][j]['comments']['data'])):
# 				print "\t" + page['data'][j]['comments']['data'][i]['message'] + "\n\n"
# 	except KeyError:
# 		pass