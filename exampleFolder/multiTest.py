from multiprocessing import Process , Pipe
import time
        
            
def main():
    
    
    pipeSend, pipeRecv = Pipe()
    p1 = Process(target=sender, args=(pipeSend,))
    p2 = Process(target = receiver, args= (pipeRecv,))
    
#     p2.daemon = True
    
    while not p1.is_alive() and not p2.is_alive():
        
        p1 = Process(target=sender, args=(pipeSend,))
        p2 = Process(target = receiver, args= (pipeRecv,))

        p1.start()
        p2.start()
        p1.join()
        p2.join()
        
        
        time.sleep(0.1)
        
        p1.terminate()
        p2.terminate()
        
        time.sleep(0.1)
        
#         p1.start()
#         p2.start()
        
#         p1.join()
#         p2.join()
#         
        
#         p1.terminate()
#         p2.terminate()
        
        
        


    
def sender(pipeS):
    while True:
        for i in range(1,11):
            pipeS.send(i)
#         return
#         print(i)
        
    
def receiver(pipeR):
    
    while True:
        num = pipeR.recv()
        print(num)
#         return 'done'
    
    
    
if __name__ == '__main__':
    
    
    main()
#     pipeSend, pipeRecv = Pipe()
#     p1 = Process(target=sender, args=(pipeSend,))
#     p2 = Process(target = receiver, args= (pipeRecv,))
#     
#     
#     p1.start()
#     p2.start()
#     
#     p1.terminate()
#     p2.terminate()
#     
#     p1.join()
#     p2.join()
#     p1.join()
#     p2.join()
#     time.sleep(0.3)
    
#     while p1.is_alive()==False and p2.is_alive()==False:
#         
#         p1 = Process(target=sender, args=(pipeSend,))
#         p2 = Process(target = receiver, args= (pipeRecv,))
#         
#         p1.start()
#         p2.start()
#         time.sleep(0.1)
#     main(p1,p2)
    
# #     p3 = Process(target = main, args = (pipeSend2,pipeRecv))
#     p1.start()
#     p2.start()
# #     p3.start()
#     p1.join()
#     p2.join()
# #     p3.join()