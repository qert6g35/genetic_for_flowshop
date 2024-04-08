class Task:

  def __init__(self,times,_id):
    self.id = _id
    self.times = []
    for n in times.split(' '):
      self.times.append(int(n))
    #print("id:" + str(self.id) +" times:" + str(self.times))


def getTask(Tasks,Task_id):
  for task in Tasks:
    if(task.id == Task_id):
      return task

def C_max(Tasks, permutation, m):
  Cmax = []
  for _ in range(0,m):
    Cmax.append(0)
  
  for task_id in permutation:
    task = getTask(Tasks,task_id)
    Cmax[0] += task.times[0]
    for i in range(1,m):
      if(Cmax[i-1] > Cmax[i]):
        Cmax[i] = Cmax[i-1]
      Cmax[i] = task.times[i]

  return Cmax[m-1]


  
  

def genetic(Tasks, m):
  print(C_max(Tasks,[],m))