from TestingEssentials import GenerateJ, FromTasksToMatrix, EvaluateC, CalculateCmax, tasks_df, start_t, plot_schedule, plot_schedule_fancy
from Task import Task
A = GenerateJ(6,3,3)


for task in A:
    print(task)
    

print(EvaluateC(A))
print(CalculateCmax(A))

a, b = FromTasksToMatrix(A)
c = start_t(A,EvaluateC(A))

df = tasks_df(a,b,c)
# print(df)
# plot_schedule_fancy(a,b,c)

plot_schedule_fancy(a,b,c)