import cherrypy
import pprint
  

class MyWebService(object):

   @cherrypy.expose
   def index(self):
      return 'Hello There! Access /fizzbuzz to print fizzbuzz number sequence'

   @cherrypy.expose
   @cherrypy.tools.json_out()
   @cherrypy.tools.json_in()
   def fizzbuzz(self,start=1,end=100):
      def int_to_fizzbuzz(i):
           entry = ''
           if i%3 == 0:
               entry += "fizz"
           if i%5 == 0:
               entry += "buzz"
           if i%3 != 0 and i%5 != 0:
               entry = i
           return entry

      return [int_to_fizzbuzz(i) for i in range(int(start), int(end))]

if __name__ == "__main__":
   config = {'server.socket_host': '0.0.0.0'}
   cherrypy.config.update(config)
   cherrypy.quickstart(MyWebService())
