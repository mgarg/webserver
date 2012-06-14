import http.server
import socketserver


def readFile(filename):
    part = {}
    with open(filename,'r') as f:
        file = f.read()
        lst1 = file.split('<?python')
        part['head'] = lst1[0]
        part['body'], part['tail'], *_ = lst1[1].split('?>')
    return part

def expr(head,body,tail):
    stb = [head]
    
    def echo(x):
        stb.append(str(x))
    exec(body)    
    stb.append(tail)
    return '\n'.join(stb)



            

class MyServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("." + self.path)
        x = readFile("." + self.path)
        res = expr(x['head'],x['body'],x['tail'])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(res))
        self.end_headers()
        self.wfile.write(res.encode('utf-8'))

    def __init__(self,req,client_addr,server):
        http.server.BaseHTTPRequestHandler.__init__(self,req,client_addr,server)
        
        
PORT = 8080
httpd = socketserver.TCPServer(("", PORT), MyServer)
print("serving at port", PORT)
httpd.serve_forever()
