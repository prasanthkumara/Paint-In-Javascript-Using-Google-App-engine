import wsgiref.handlers
import json
import pickle
import jinja2
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import Request
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class data(db.Model):
	filename=db.StringProperty()
	image=db.StringListProperty()
	
	
class mainh(webapp.RequestHandler):

	def get(self):
		lis=[]
		imagelist=[]
		for i in data.all():
			lis.append(i.filename)
	
		filename=self.request.path[1:]
		
		self.response.out.write('<font size="5">'+self.request.path[1:]+'</font>')	
		
		
		if filename!="":
			for i in data.all():
				if json.loads(i.filename)==filename:
					for j in i.image:
						imagelist.append(pickle.loads(j))
			#self.response.out.write(json.dumps(imagelist))
			self.response.out.write('<script>lis='+json.dumps(lis)+';fill=0; wholedata=new Array();imagedata='+json.dumps(imagelist)+'; data= new Array(); </script>')
		else:
			self.response.out.write('<script>lis='+json.dumps(lis)+';fill=0; wholedata=new Array();imagedata='+json.dumps("")+' ;data= new Array(); </script>') 		 
		
		 
		self.response.out.write(template.render("paint.html",{}))
	         #self.reeponse.out.write(""" <html><body><form><input type="button" name="b"></form></body></html>""")

	def post(self):
		#self.response.headers['content-Type'] = 'html'

		data1=json.loads(self.request.get('parameter'))
		filename=self.request.get('f')
		a=pickle.dumps(data1[0])
		self.response.out.write(pickle.loads(a))
		self.response.out.write(data1[0])
		self.response.out.write(filename)
		datastore=data(parent=db.Key.from_path('filename',filename))
		datastore.filename=filename
		for i in data1:
			datastore.image.append(pickle.dumps(i))
		datafile=db.GqlQuery("SELECT * FROM data WHERE ANCESTOR IS :c",c=db.Key.from_path('filename',filename))
		count=0
		for i in datafile:
			count=count+1
			i.image=[]
			for j in data1:
				i.image.append(pickle.dumps(j))
			db.put(i)
		if count==0:
			datastore.put()

		self.redirect("")
		for i in datafile:
			for j in i.image:
				self.response.out.write(pickle.loads(j))
		

		#retrieve and edit
	         	
		
def main():
    app = webapp.WSGIApplication([
        ('/.*',mainh)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)


if __name__ == "__main__":
    main()


