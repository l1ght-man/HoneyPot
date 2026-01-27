import socket
import datetime
import json
import time
import threading
from pathlib import Path
import docker
import select
LOG_DIR = Path("Honeypot_logs")
LOG_DIR.mkdir(exist_ok=True)



class Honeypot:
    def __init__(self, ports=[22,21,80,23]):
        self.ports = ports
        with open ('fake_website.html' , 'rb') as f:
            html_content = f.read()
        self.banners = {
    22: b"SSH-2.0-FakeSSH\r\n",
    21: b"220 Fake FTP Server ready\r\n",
    80: b"""HTTP/1.1 200 OK\r\n"""
        b"""Server: Apache/2.4.41 (Ubuntu)\r\n"""
        b"""Content-Type: text/html; charset=UTF-8\r\n"""
        b"""Connection: close\r\n\r\n""" + html_content,
    23: b""
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
            if port == 23 :
                self.log_activity(ip,port,"starting Docker proxy")
                self.start_docker_honeypot(client_sock,ip)
                return            
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
    def docker_output_reader(self, docker_sock, client_sock):
        """Thread: Reads from Docker, Sends to Hacker"""
        try :
            while True:
                data = docker_sock.recv(4096)
                if not data: break
                format_output = data.replace(b'\n',b'\n\r')
                client_sock.send(data)
        except Exception as e:
            print(f"Reader Thread ended: {e}") 
    def start_docker_honeypot(self, client_sock, ip):
        client_sock.settimeout(300)
        client = docker.from_env()
        print(f"[*] Spawning container for {ip}...")
        trap_path = Path.cwd()
        startup_cmd = "bash -c 'stty -echo; exec bash --noediting'"
        # container running
        container = client.containers.run(
            "ubuntu:latest", 
            startup_cmd,
            detach=True, 
            tty=True, 
            stdin_open=True,
            hostname="production-server",
            )
        try:
            docker_sock = container.attach_socket(params={'stdin': 1, 'stdout':1 , 'stream':1}) 
            client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) 
            client_sock.send(bytes([255,251,1]))
            client_sock.send(bytes([255, 251, 3]))
            client_sock.send(bytes([255,252,34]))
            client_sock.send(b"Connected to Ubuntu 22.04.4 LTS\r\n")
              
            t = threading.Thread(target=self.docker_output_reader, args=(docker_sock, client_sock))
            t.daemon = True
            t.start() 
            
            command_buffer = b""
            while True:
                        hacker_input = client_sock.recv(1024)
                        if not hacker_input : break
                        clean_input = b""
                        for byte in hacker_input :
                            if byte == 127 or byte == 8 :
                                if len(command_buffer) > 0:
                                    client_sock.send(b'\b \b')
                                    docker_sock.send(b'\x7f')
                                    command_buffer = command_buffer[:-1]
                                continue
                            if byte < 128:
                                    char = bytes([byte])
                                    if char == b'\n' or char == b'\r'  :
                                        client_sock.send(b'\r\n')
                                        docker_sock.send(b'\n')
                                        try:
                                             decoded_cmd = command_buffer.decode('utf-8', errors='ignore').strip()
                                             if decoded_cmd: 
                                                  self.log_activity(ip, 23, f"CMD: {decoded_cmd}")
                                        except:pass
                                        command_buffer = b""
                                    else:
                                        client_sock.send(char)
                                        docker_sock.send(char)
                                        command_buffer += char 

                        if clean_input:
                            
                            if b'\r' in clean_input or b'\n' in clean_input :
                                    client_sock.send(b'\r\n')
                                    docker_sock.send(b'\n')   
                            else:
                                    client_sock.send(clean_input)
                                    docker_sock.send(clean_input)   
                                        
                                    command_buffer += clean_input
                                    try:
                                       decoded_cmd = command_buffer.decode('utf-8',errors='ignore').strip()
                                       if decoded_cmd:
                                             self.log_activity(ip , 23 , f"CMD: {decoded_cmd}" )
                                    except : pass
                                    command_buffer = b""
        except Exception as e:
            print(f"Eroor: {e}")
        finally:
            print(f"[*] Killing container for {ip}")
            container.stop()
            container.remove()
            client_sock.close()
              


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