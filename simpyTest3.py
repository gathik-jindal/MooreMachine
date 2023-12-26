import simpy

class Run():
           lst=[]
           def __init__(self):
                      for i in Run.lst:
                                 print(i)
                                 i.run()

class Input(Run):
           
           def __init__(self,lst,env):

                      self.env=env
                      self.input=lst
                      
                      self.fanoutCount=0
                      self.output=[0]

                      Run.lst.append(self)
                      
           def __le__(self):
                      print("Invaid connection")

           def go(self):
                      for i in self.input:
                                 yield self.env.timeout(i[1]-self.env.now)
                                 print("Input changed at",self.env.now)
                                 self.output[0]=i[0]
                                 for i in range(1,self.fanoutCount+1):
                                            self.output[i].put(True)
           def addFanout(self):
                      self.fanoutCount+=1
                      self.output.append(simpy.Store(self.env))
                      self.output[-1].put(True)
                      return self.fanoutCount

           def run(self):
                      self.env.process(self.go())
                      

class Machine(Run):
         
           def __init__(self, env, clock, NSL, OL):
                      
                      self.env=env
                      self.clock=clock
                      self.NSL=NSL
                      self.OL=OL
                      
                      self.NS=0
                      self.PS=0
                      self.Pchange=simpy.Store(self.env)
                      
                      self.fanoutCount=0
                      self.output=[0]
                      
           def __le__(self,other):
                      self.input=other.output
                      self.cid=other.addFanout()

                      Run.lst.append(self)

                      return True

           def addFanout(self):
                      self.fanoutCount+=1
                      self.output.append(simpy.Store(self.env))
                      self.output[-1].put(True)
                      return self.fanoutCount

           def runNSLi(self):
                      while True:
                                 yield self.input[self.cid].get()
                                 print("recalculate at ", self.env.now, "using", self.input[0], "inside", self)
                                 tempout=self.input[0]+1
                                 yield self.env.timeout(0.6)
                                 self.output[0]=tempout
                                 for i in range(1,self.fanoutCount+1):
                                            self.output[i].put(True)
                                 print(self.input[0],self,self.env.now)
                      
           def runNSLp(self):
                      while True:
                                 yield self.Pchange.get()
                                 print("recalculate at ", self.env.now, "using", self.input[1])
                                 yield self.env.timeout(0.5)
                                 self.output[1]=self.input[1]+1
                                 self.output[0].put(True)

           def runReg(self):
                      pass

           def runOL(self):
                      pass

           def run(self):
                      self.env.process(self.runNSLi())
                      

class Out(Run):
           
           def __init__(self,env,ans):
                      self.env=env
                      self.ans=ans

                      

           def __le__(self,other):
                      self.input=other.output
                      self.cid=other.addFanout()

                      Run.lst.append(self)
                      
                      return True

           def give(self):
                      while True:
                                 yield self.input[self.cid].get()
                                 print("Output is",self.input[0],"at",self.env.now)
                                 self.ans.append((self.input[0],self.env.now))
           def run(self):
                      self.env.process(self.give())                      



class Clock():
           def __init__(self,env,tp,tc):
                      self.env=env
                      self.tu=tc
                      self.td=tp-tc



ans=[]
question=[(1,1),(6,3),(9,5),(16,8)]


env=simpy.Environment()

clk=None
i=Input(question,env)
m1=Machine(env,clk,1,1)
m2=Machine(env,clk,1,1)
o=Out(env, ans)



m1 <= i
m2 <= m1
o <= m2

r=Run()
env.run(until=40)
print("\nMachine out is:", ans,"\nreal output is:")#, [(i[0]+2,i[1]+1) for i in ([(0,0)]+question)])
input()
                      
                      
                      
                      
