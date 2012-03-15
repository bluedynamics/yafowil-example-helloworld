from yafowil import loader
import yafowil.webob
from yafowil.base import factory
from yafowil.controller import Controller
from webob import Request, Response

address, port = '127.0.0.1', 8080 
url = 'http://%s:%s/' % (address, port)

def store(widget, data):
    with open('helloworld.txt', 'a') as storage:
        storage.write(data.fetch('helloworld.hello').extracted + '\n')    
    
def readall():
    try:
        with open('helloworld.txt', 'r') as storage:
            return reversed(storage.readlines())
    except IOError:
        return ['Empty storage!']

def next(request):
    return url

def application(environ, start_response):
    request = Request(environ)
    response = Response()
    response.write('<html><body><h1>YAFOWIL Demo</h1>')
    form = factory(u'form', name='helloworld', props={
        'action': url})
    form['hello'] = factory('field:label:error:text', props={
        'label': 'Enter some text',
        'value': '',
        'required': True})
    form['submit'] = factory('field:submit', props={        
        'label': 'store value',
        'action': 'save',
        'handler': store,
        'next': next})
    controller = Controller(form, request)
    response.write(controller.rendered)
    response.write('<hr />%s</html></body>' % '<br />'.join(readall()))
    return response(environ, start_response)
    
def run():
    from wsgiref.simple_server import make_server
    server = make_server(address, port, application)
    server.serve_forever()