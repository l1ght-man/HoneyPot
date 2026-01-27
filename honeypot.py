import socket
import datetime
import json
import time
import threading
from pathlib import Path


LOG_DIR = Path("Honeypot_logs")
LOG_DIR.mkdir(exist_ok=True)

class Virtual

class Honeypot:
    def __init__(self, ports=[22,21,80]):
        self.ports = ports
        with open ('fake_website.html' , 'rb') as f:
            html_content = f.read()
        self.banners = {
    22: b"SSH-2.0-FakeSSH\r\n",
    21: b"220 Fake FTP Server ready\r\n",
    80: b"""HTTP/1.1 200 OK\r\n"""
        b"""Server: Apache/2.4.41 (Ubuntu)\r\n"""
        b"""Content-Type: text/html; charset=UTF-8\r\n"""
        b"""Connection: close\r\n\r\n""" + html_content
}
 
    def log_activity(self, ip , port , data=""):
        timestamp = datetime.datetime.now().isoformat()
        activity = {
            "timestamp": timestamp,
            "ip": ip,
            "port": port,
            "data": data
        }
        log_file = LOG_DIR / f"honeypot_{datetime.date.today()}.jsonl"
        with open(log_file, "a") as f :
            f.write(json.dumps(activity)+ "\n")
    def handle_client(self, client_sock, addr, port):
        ip = addr[0]
        try:
            client_sock.settimeout(10)
            banner = self.banners.get(port, b"Unknown service\r\n")
            client_sock.send(banner)
            self.log_activity(ip,port, "banner sent")
            if port == 80:
                        raw_data = client_sock.recv(1024)
                        http_request = raw_data.decode('utf-8', errors='ignore')
                        lines = http_request.split('\r\n')
                        if lines:
                            first_line = lines[0]
                            method, path, protocol = first_line.split(' ', 2)
                            self.log_activity(ip, port, f"HTTP {method} {path}")

                            headers = {}
                            for line in lines[1:]:
                                if ': ' in line:
                                    key, value = line.split(': ', 1)
                                    headers[key] = value.strip()
                            if 'User-Agent' in headers:
                                self.log_activity(ip, port, f"User-Agent: {headers['User-Agent']}...")
                            else:
                                self.log_activity(ip, port, "Empty HTTP request")
            else:
                data= client_sock.recv(1024).decode('utf-8', errors='ignore')
                self.log_activity(ip,port,f"Received: {data}")
        except Exception as e:
            self.log_activity(ip, port, f"Error : {str(e)}")
        finally:
            client_sock.close()
        
    def listen_port(self, port):
        sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', port))
        sock.listen(5)
        print(f"[*] Listening on port {port}")
        while True:
            client_sock , addr = sock.accept()
            client_thread = threading.Thread(target=self.handle_client,args=(client_sock, addr, port))
            client_thread.start()
        sock.close()


if __name__ == '__main__':
    hp = Honeypot()
    for port in hp.ports :
        thread= threading.Thread(target=hp.listen_port, args=(port,))
        thread.daemon = True
        thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Stopping HoneyPot...")