res= []
def test(n):
    for i in range(n):
        res.append(i)
    print(res)

def remove():
    print (res.pop())
    
test(5)
remove()