import sys
import getopt
import os
import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
'''
class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=False, sackMode=False):
        super(Sender, self).__init__(dest, port, filename, debug)
        self.sackMode = sackMode
        self.debug = debug


    # Main sending loop.
    def start(self):

        initilize = self.make_packet("syn",0,"")
      #  print("self",self.infile)
        self.send(initilize)
        rec_init = self.receive(0.5)
        seq_num = 0
        sack_mode = False
        if(rec_init != None):
            rec_init_list = rec_init.split("|")
            rec_type = rec_init_list[0]
            if(rec_type !="sack"):

              seq_num = int(rec_init_list[1])
            else:
                sack_mode = True
                seq_num = 1


        while(seq_num == 0):
            initilize = self.make_packet("syn", 0, "")
            #  print("self",self.infile)
            self.send(initilize)

            rec_init = self.receive(0.5)
            if(rec_init != None):

                rec_init_list = rec_init.split("|")
                if( rec_init_list[0]!="sack"):


                    seq_num = int(rec_init_list[1])
                else:
                    sack_mode = True
                    semicollon = rec_init_list[1].find(';')

                    seq_num = int(rec_init_list[1][:semicollon])



        packets = [0]
        while True:
            data = self.infile.read(1450)
            packets.append( data)
            if(len(data) < 1450):
                break





        while True:
            data = packets[seq_num]
         #   print("data",data)
     #       print("seq",seq_num)
            if(len(data) < 1450):

                end = self.make_packet("fin", seq_num, data)
                self.send(end)
                end_ack = self.receive(0.5)
                if(end_ack!=None):
                    rec_end_list = end_ack.split("|")
                    if(not sack_mode):


                        seq_num = int(rec_end_list[1])
                        break
                    else:

                        semicollon = rec_end_list[1].find(';')

                        seq_num = int(rec_end_list[1][:semicollon])
                        break
               # dat2 = self.receive()

            else:
                dat = self.make_packet("dat", seq_num, packets[seq_num])
                self.send(dat)
                data_ack = self.receive(0.5)

                if(data_ack !=None):
                    rec_data_list = data_ack.split("|")
                    if(not sack_mode):

                        seq_num = int(rec_data_list[1])
                    else:
                        semicollon = rec_data_list[1].find(';')

                        seq_num = int(rec_data_list[1][:semicollon])









'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print "BEARS-TP Sender"
        print "-f FILE | --file=FILE The file to transfer; if empty reads from STDIN"
        print "-p PORT | --port=PORT The destination port, defaults to 33122"
        print "-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost"
        print "-d | --debug Print debug messages"
        print "-h | --help Print this usage message"
        print "-k | --sack Enable selective acknowledgement mode"


    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:dk", ["file=", "port=", "address=", "debug=", "sack="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False
    sackMode = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):

            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True
        elif o in ("-k", "--sack="):
            sackMode = True

    s = Sender(dest,port,filename,debug, sackMode)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()