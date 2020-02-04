

def main():
    person('zhangsan',18,city='beijing')
    extra={'city':'beijing','job':'student'}
    person('lisi',18,**extra)


def person(name,age,**kw):
    print('name',name,'age',age,'other',kw)




if __name__=='__main__':
    main()
