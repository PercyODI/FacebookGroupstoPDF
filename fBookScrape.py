from facepy import GraphAPI, exceptions
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class MCLine(Flowable):
    """
    Line flowable --- draws a line in a flowable

http://two.pairlist.net/pipermail/reportlab-users/2005-February/003695.html

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
	graph = GraphAPI("CAACEdEose0cBADyZBaPpNCCJpwTh8CpDNklFcG6UG54LWVpZCMIPL0RkKkOqAJw3hUcumTeRtStsPQfVmpgzWv7vUaP7x2lpaZBcqInsjgZBEoUo41z7YYbgoAvcfkZAYI9S7MtKwjxgeX7pOazqyGELTLUkx8xyroatuukbHVztqLqYvE02Xt06rGrNZCJINA7rr2OkaVxZBDnpnnHys5ZB")
	response = graph.get('/175579742455688/feed', page=True)
	return response


def hello_pdf(page):
 	def hello(c):
 		c.drawString(100,100,"Hello World")
 	c = canvas.Canvas("hello.pdf", pagesize=(612.0, 792.0))
 	hello(c)
 	c.showPage()
 	c.save()
 
def createCanvas():
	return SimpleDocTemplate("hello2.pdf", pagesize=letter,
							  rightMargin=72, leftMargin=72,
							  topMargin=72, bottomMargin=18), []

def draw_page(story, page):
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='comment', leftIndent=25, rightIndent=25, borderWidth=1, borderColor="black", borderPadding=2))
	styles.add(ParagraphStyle(name='commentName', leftIndent=15, rightIndent=25))
	line = MCLine(500)
	try:
		for i in page['data']:
			ptext = i['message'].encode('ascii', 'ignore').replace("\n", '<br />\n')
			story.append(Spacer(1, 12))
			story.append(Paragraph(ptext, styles["Normal"]))
			story.append(Spacer(1, 12))
			try:
				for j in i['comments']['data']:
					pname = j['from']['name'].encode('ascii', 'ignore')
					story.append(Paragraph(pname, styles["commentName"]))
					story.append(Spacer(1, 6))
					ptext = j['message'].encode('ascii', 'ignore').replace("\n", '<br />\n')
					story.append(Paragraph(ptext, styles["comment"]))
					story.append(Spacer(1, 12))
					
			except KeyError:
		 		print "Key Error in draw_page"
			story.append(line)
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
doc, Story = createCanvas()
pages = get_graphAPI()

# try:
#for page in pages:
for x in range(50):
	page = pages.next()
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