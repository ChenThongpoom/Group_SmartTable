from multiprocessing import Process , Pipe


msgs = [4,5,6,10,30,2,0]


def send(conn, msgs):
    for i in msgs:
        conn.send(i)
    conn.close()
    
    
def recv(conn):
    while True:
        msg = conn.recv()
        if msg >= 4 and msg <= 10:
            print('stop')
        elif msg < 4:
            print('up')
        elif msg > 10:
            print('down')
        else:
            break
        print(msg)
        send,

send_conn, recv_conn = Pipe()
p1 = Process(target = send, args=(send_conn, msgs))
p2 = Process(target = recv, args = (recv_conn,))

p1.start()
p2.start()

p1.join()
p2.join()