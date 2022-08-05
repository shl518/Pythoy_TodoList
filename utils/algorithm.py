"""
input：顺序三个数组，截止时间数组，持续时间数组，误时惩罚数组，注意时间格式转换为纯分钟数，比如22：30转换为22*60+30 = 1350
return:按原顺序返回字典数组，字典格式{'id':没用，'start':正常时间，'end'：正常时间},同时会自动输出罚时
请注意！：罚时数组，罚时以level为准，即0-3一一对应，若为日常任务，请传入罚时=10作为日常任务的标记
method：贪心
未解决的潜在问题：日常任务固定时间冲突，由于时间只有24h = 1440min无法安排所有任务（任务总时间超出24h，超出范围的任务将不会被安排，也不会被返回）。这些问题均未考虑
用法：参见底部测试main,使用时先import
"""

import time


class Optimal:
    def __init__(self, d, l, p):
        self.relax = 0  # 暂定任务休息间隔10min
        self.timeline = [1] + [0] * 1440
        self.deadlines = [0]  # 截至时间  分钟数
        self.lasttime = [0]  # 持续时间  分钟数
        self.punishments = [-1]  # 误时惩罚 日常任务暂定以10为标记
        self.maxtime = 0
        self.deadlines += d
        self.lasttime += l
        self.punishments += p
        self.n = len(d)
        self.id = list(range(0, self.n + 1))
        self.penaltyTTime = 0
        self.arrange_result = []  # 字典存储最终结果

    def Arrange(self):
        self.punishDescent()
        self.optimalOrder()
        for res in self.arrange_result:
            res['start'] = self.toTime(res['start'])
            res['end'] = self.toTime(res['end'])
        self.arrange_result = sorted(self.arrange_result, key=lambda x: x['id'])
        return self.arrange_result

    def toTime(self, i):
        t = str(i // 60)
        m = str(i % 60)
        return t.zfill(2) + ":" + m.zfill(2)

    def fill_past_time(self):
        h, m, s = time.asctime().split()[3].split(':')
        now_time = int(h) * 60 + int(m)
        for i in range(1, now_time + 1):
            self.timeline[i] = 1

    # 获取最优的安排顺序 1440时间粒度 1为占用，0为未占用
    def optimalOrder(self):
        print(self.punishments)
        self.fill_past_time()
        # 首先固定日常任务
        i0 = 1
        for i0 in range(1, self.n + 1):
            if self.punishments[i0] == 10:
                for t in range(self.lasttime[i0]):
                    self.timeline[self.deadlines[i0] - t] = 1
                self.arrange_result.append(
                    {'id': self.id[i0], 'start': self.deadlines[i0] - self.lasttime[i0],
                     'end': self.deadlines[i0]})
                self.maxtime = self.deadlines[i0] if self.deadlines[i0] > self.maxtime else self.maxtime
            else:
                break
        for i in range(i0, self.n + 1):
            j = 0
            put = 0
            for j in range(self.deadlines[i], self.lasttime[i], -1):
                if self.NoMission(i, j):  # 如果该时间片还没有任务，则将这个任务放在这里，即置为1
                    self.PutMission(i, j)
                    put = 1
                    break
            # 若[1:i]的时间片都有安排的任务，则这个任务肯定会产生罚时。
            # 注意，此时不要将其安排在optimalChoice[i+1,n]中，以免产生后效性。已经产生了罚时的任务，最后安排在[i+1,n]中
            # 时间片中，因为可能有punishments[i+1,n]中的一个任务，的deadlines的时间在[i+1:n]中
            if put == 0:
                for j in range(self.deadlines[i] + 1, 1441):
                    if self.NoMission(i, j):  # 如果该时间片还没有任务，则将这个任务放在这里，即置为1
                        self.PutMission(i, j)
                        break
                if j == 1440:
                    continue  # 如果已经超出1440范围，直接跳过该任务
                self.penaltyTTime += self.punishments[i]

        # print(self.penaltyTTime)

    # 排序：对相同截止时间的误时惩罚进行降序排列
    def punishDescent(self):
        # 冒泡排序n-1次
        for i in range(1, self.n):
            for j in range(1, self.n + 1 - i):
                if self.punishments[j] < self.punishments[j + 1]:
                    self.punishments[j], self.punishments[j + 1] = self.punishments[j + 1], self.punishments[j]
                    self.deadlines[j], self.deadlines[j + 1] = self.deadlines[j + 1], self.deadlines[j]
                    self.lasttime[j], self.lasttime[j + 1] = self.lasttime[j + 1], self.lasttime[j]
                    self.id[j], self.id[j + 1] = self.id[j + 1], self.id[j]

    def NoMission(self, i, end):
        for t in range(self.lasttime[i]):
            if self.timeline[end - t] == 1:
                return False
        # print(i,self.id[i],self.toTime(end))
        return True

    def PutMission(self, i, end):  # 暂时取消休息时间，加上休息时间Bug较多
        # if end + self.relax <= 1440:
        #     if self.timeline[end + self.relax] == 1:
        #         pos = 0
        #         while 1:
        #             pos += 1
        #             if self.timeline[end + pos] == 1:
        #                 break
        #         end -= self.relax - pos + 1
        # if end - self.lasttime[i] - self.relax >= 0:
        #     if self.timeline[end - self.lasttime[i] - self.relax] == 1:
        #         pos = 0
        #         while 1:
        #             pos += 1
        #             if self.timeline[end - self.lasttime[i] - pos] == 1:
        #                 break
        #         print(pos)
        #         end += self.relax + 1 - pos
        for t in range(self.lasttime[i]):
            self.timeline[end - t] = 1
        self.arrange_result.append(
            {'id': self.id[i], 'start': end - self.lasttime[i], 'end': end})
        self.maxtime = end if end > self.maxtime else self.maxtime


"""
测试例子
"""
if __name__ == '__main__':
    deadline = [500, 400, 300, 1350, 1200, 900]
    lasttime = [50, 300, 200, 40, 200, 350]
    level = [2, 1, 3, 10, 2, 0]
    O = Optimal(deadline, lasttime, level)  # 首先创建对象
    ress = O.Arrange()  # 接着调用Arrange函数，并在左侧接受返回的字典
    for res in ress:
        print(res)


def scheduling(todos):
    deadline = []
    lasttime = []
    level = []
    for todo in todos:
        hour = int(str(todo.expiration_date)[11:13])
        minute = int(str(todo.expiration_date)[14:16])
        deadline.append(hour * 60 + minute)
        lasttime.append(todo.predict_hour * 60 + todo.predict_minute)
        if todo.isDaily != 1:
            level.append(todo.level)
        else:
            level.append(10)
    O = Optimal(deadline, lasttime, level)  # 首先创建对象
    ress = O.Arrange()  # 接着调用Arrange函数，并在左侧接受返回的字典
    return ress
