from TestingEssentials import GenerateJ, EvaluateC, CalculateCmax, tasks_df, start_t, plot_schedule, plot_schedule_fancy
J, pi = GenerateJ(6,3,3)


for task in J:
    print(task)
    

print(EvaluateC(J, pi))
print(CalculateCmax(J, pi))

S = start_t(J, pi,EvaluateC(J, pi))

df = tasks_df(pi,J,S)
# print(df)
# plot_schedule_fancy(a,b,c)

plot_schedule_fancy(pi,J,S)