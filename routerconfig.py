import paramiko
import time
import config


def connectSsh(self):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(
        config.HOST,
        username=config.USER,
        password=config.PASSWD,
        look_for_keys=False,
        allow_agent=False)
    return conn


circuit = ""
incir=inpir=outcir=outpir=linein=lineout= ""



class RouterConfig:

    def configRouter(self):
        conn = connectSsh("")
        
        output=""
        GE= ""
        stdin, stdout, stderr = conn.exec_command("display interface description | include "+self['CIRCUIT'])
        stdout=stdout.readlines()
        conn.close()
        
        for line in stdout:
            if 'GE' in line:
                GE = (line.split(" ")[0])[2:7]
                print(GE)
        
        conn = connectSsh("")    
        stdin, stdout, stderr = conn.exec_command("display current-configuration interface GigabitEthernet "+GE)
        stdout=stdout.readlines()
        conn.close()
            
        for line in stdout:
            if 'user-queue' in line:
                if 'inbound' in line:
                    incir = line.split(" ")[3]
                    inpir = line.split(" ")[5]
                    print(line)
                    
        
                if 'outbound' in line:
                    outcir = line.split(" ")[3]
                    outpir = line.split(" ")[5]
                    print(line) 
        if  incir ==  inpir == outcir == outpir:
            print("success")
            conn = connectSsh("")    
            remote_conn = conn.invoke_shell()
            remote_conn.send("system-view \n")
            remote_conn.send("interface GigabitEthernet "+GE+" \n")
            remote_conn.send("undo user-queue inbound \n")
            remote_conn.send("undo user-queue outbound \n")
            remote_conn.send("user-queue cir "+self['SPEED']+" pir "+self['SPEED']+" flow-queue 201 inbound \n")
            remote_conn.send("user-queue cir "+self['SPEED']+" pir "+self['SPEED']+" flow-queue 201 outbound \n")
            remote_conn.send("display this \n")
            time.sleep(2)
            output = remote_conn.recv(5000)
            print(output.decode("utf-8"))

        else: 
            print("invalid inbound Outbound values")
                
       
        
                        