import simpy
class Input():
           
           def __init__(self,lst,env):

                      self.env=env
                      self.Ochange=simpy.Store(self.env)
                      self.input=lst
                      self.output=[self.Ochange, 0]
                      self.output[0].put(True)
                      self.env.process(self.go())
                      
           def __le__(self):
                      print("Invaid connection")

           def go(self):
                      for i in self.input:
                                 yield self.env.timeout(i[1]-self.env.now)
                                 print("Input changed at",self.env.now)
                                 self.output[1]=i[0]
                                 self.Ochange.put(True)

class Machine():
         
           def __init__(self, env, clock):
                      self.env=env
                      self.clock=clock
                      self.NS=0
                      self.PS=0
                      self.Pchange=simpy.Store(self.env)
                      self.Ochange=simpy.Store(self.env)
                      self.output=[self.Ochange,0]
                      
           def __le__(self,other):
                      self.input=other.output
                      self.env.process(self.runNSLi())
                      #self.env.process(self.reg)

                      return True

           def runNSLi(self):
                      while True:
                                 yield self.input[0].get()
                                 print("recalculate at ", self.env.now, "using", self.input[1])
                                 yield self.env.timeout(0.5)
                                 self.output[1]=self.input[1]+1
                                 self.output[0].put(True)
                      
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

class Out():
           
           def __init__(self,env,ans):
                      self.env=env
                      self.ans=ans

           def __le__(self,other):
                      self.input=other.output
                      self.env.process(self.give())

                      return True

           def give(self):
                      while True:
                                 yield self.input[0].get()
                                 print("Output is",self.input[1],"at",self.env.now)
                                 self.ans.append((self.input[1],self.env.now))



class Clock():
           def __init__(self,env,tp,tc):
                      self.env=env
                      self.tu=tc
                      self.td=tp-tc


ans=[]
question=[(1,1),(4,6),(9,9),(16,18)]


env=simpy.Environment()

clk=None
i=Input(question,env)
m1=Machine(env,clk)
m2=Machine(env,clk)
o=Out(env, ans)



m1 <= i
m2 <= m1
o <= m2

env.run(until=40)
print("\nMachine out is:", ans,"\nreal output is:", [(i[0]+2,i[1]+1) for i in ([(0,0)]+question)])                      
                      
                      
                      
                      
