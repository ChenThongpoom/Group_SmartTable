from multiprocessing import Pipe, Process
import time

def Send():
    count = 0

    pipeSend, pipeRecv = Pipe()

    p1 = Process(target=Recv, args=(pipeRecv,))

    p1.start()
    while True:
        count += 1
        pipeSend.send('hello')
        time.sleep(1)
        if count == 10 :
            pipeSend.close()
            p1.terminate()

            time.sleep(0.1)

            
            return 'Done'



def Recv(valrecv):
    while True:
        get = valrecv.recv()
        print(get)



if __name__ == '__main__':
    
    x = Send()
    while True:
        if x == 'Done':
            print(x)
            x = None
            x = Send()
    