
# 在python中，这两个是python中的可变参数，*arg表示任意多个无名参数，类型为tuple;**kwargs表示关键字参数，为dict。

# *允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。
def f(a,*args):
    print(args)

f(1,2,3,4)


# **,关键字参数允许你传入0个或任意个含参数名的参数,这些关键字参数在函数内部自动组装为一个dict。
def d(**kargs):
    print(kargs)

d(a=1, b=2)


#在函数混合使用*以及**。
def h(a,*args,**kargs):
    print(a,args,kargs)

h(1,2,3,x=4,y=5)


# 上面是在函数定义的时候写的*和**形式，那反过来，如果*和**语法出现在函数调用中又会如何呢？
# 他会解包参数的集合。例如，我们在调用函数时能够使用*语法，在这种情况下，它与函数定义的意思相反，他会解包参数的集合，而不是创建参数的集合。

#通过一个元组给一个函数传递四个参数，并且让python将它们解包成不同的参数。
def func(a,b,c,d):
    print(a,b,c,d)

a = (1,2,3,4)
func(*a)

def func(*a):
    print(a)

a = (1,2,3,4)
func(*a)

#如果已经有一个dict,在参数前面加**，函数会把dict中所有键值对转换为关键字参数传进去
def person(name,age,**kw):
    print('name:',name,'age:',age,'other:',kw)

extra = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', 24, **extra)