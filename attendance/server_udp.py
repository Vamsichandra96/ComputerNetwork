import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
portNumber = 2020
s.bind(('10.10.10.160',portNumber))
print('server created')
allStudents = {"2019501001","2019501003","2019501004","2019501012","2019501027","2019501029","2019501032","2019501051","2019501103","2019501109"}
uniqueIps = {'':["2019501001",False],'':["2019501003",False],'10.10.8.136':["2019501004",False],'10.10.10.160':["2019501012",False],'10.10.10.149':["2019501027",False],'10.10.10.168':["2019501029",False],'10.10.10.134':["2019501032",False],'10.10.11.66':["2019501043",False],'10.10.8.63':["2019501051",False],'10.2.138.175':["2019501103",False],'10.10.11.129':["2019501109",False]}
ipsObtained = []
s.settimeout(10)
while 1:
    try:
        print("uniqueIps",uniqueIps)
        print("ipsObtained: ",ipsObtained)
        data,conn = s.recvfrom(1024)
        print("connection is: " , conn)
        ipAddr,port = conn
        data = data.decode()
        if(ipAddr in uniqueIps.keys()):
            if(ipAddr not in ipsObtained):
                ipsObtained.append(ipAddr)
            if(data == uniqueIps[ipAddr][0]):
                uniqueIps[ipAddr][1] = True
                data = "Accepted"
            elif(data not in allStudents):
                data = "student not in class"
                s.sendto(data.encode(),conn)
                data = "try again."
            else:
                data = "Roll number is not matching."
                s.sendto(data.encode(),conn)
                data = "try again."
        else:
            data = "not a valid user."
        s.sendto(data.encode(),conn)
    except socket.timeout:
        data = "absenties are: " + "\n"
        for i in uniqueIps.keys():
            if(not uniqueIps[i][1]):
                data += uniqueIps[i][0] + "\n"
        for i in ipsObtained:
            s.sendto(data.encode(),(i,portNumber))
        break
s.close()