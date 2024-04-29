def CalculateCmax(_pi, _J):
    n = len(_pi)
    m = len(_J[0])
    completionTimes = [[0] * (m + 1) for _ in range(n)]
    for i in range(n):
        for j in range(1, m + 1):
            job = _J[_pi[i] - 1][j - 1]
            completionTimes[i][j] = max(completionTimes[i][j - 1], completionTimes[i - 1][j]) + job

    return completionTimes[n - 1][m]


def neh(_J):
    n = len(_J)  # liczba zadań

    # Obliczanie sum czasów dla każdego zadania
    taskTimes = [(i + 1, sum(_J[i])) for i in range(n)]
    taskTimes.sort(key=lambda x: x[1], reverse=True)  # Sortowanie malejąco
    _pi = [taskTimes[0][0]]  # Inicjalizacja kolejności zadań
    totalTime = CalculateCmax(_pi, _J)
    # print(_pi)
    # print(totalTime)
    # print("Best:    ", _pi)
    
    for i in range(1, n):
        minTotalTime = float('inf')
        best = -1

        for j in range(i + 1):
            _pi.insert(j, taskTimes[i][0])
            totalTime = CalculateCmax(_pi, _J)
            # print(_pi)
            # print(totalTime)
            if totalTime < minTotalTime:
                minTotalTime = totalTime
                best = j

            _pi.remove(taskTimes[i][0])

        _pi.insert(best, taskTimes[i][0])
        # print("Best:    ", _pi)

    return CalculateCmax(_pi, _J)