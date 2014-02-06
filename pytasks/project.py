

""" A class representing a project (a list of tasks) """

class Project:
    def __init__(self):
        self.tasks = []

    def __len__(self):
        return len(self.tasks)

    def __getitem__(self,i):
        return self.tasks[i]
        
    def goodind(self,i):
        return 0 <= i < len(self.tasks)

    def add(self,t):
        if t.__class__.__name__ != 'Task': t = Task(t)
        self.tasks.append(t)
        
    #def ins(self,task,i):
    #    if self.goodind(i):
    #        self.tasks.insert(i,task)
        
    def rm(self,i):
        if self.goodind(i):
            self.tasks.pop(i)

    def mrk(self,i,mm):
        if self.goodind(i):
            a = self.tasks[i].mark 
            self.tasks[i].mark = (a+1)%2
            if mm: 
                self.strk(i)
                self.fsh(i)
                

    def mm_ind(self,i):
        # translate index to mark mode (i.e. ith marked from back)
        mcount = -1
        for t in range(len(self.tasks)-1,-1,-1):
            mcount += self.tasks[t].mark == 1
            if mcount == i: return t
        return -1

    def mrk_mode_exit(self):
        s # exit mark mode...

    def hlt(self,i):
        if self.goodind(i):
            a = self.tasks[i].bold 
            self.tasks[i].bold = (a+1)%2

    def hlt_clr(self):
        # de-hilight all hilighted entries
        for i in range(len(self.tasks)):
            if self.tasks[i].bold:
                self.hlt(i)

    def hlt_fsh(self):
        # 'finish'/complete all highlighted entries
        for i in range(len(self.tasks)-1,-1,-1): # go backwards...
            if self.tasks[i].bold:
                self.fsh(i)

    def strk(self,i):
        if self.goodind(i):
            a = self.tasks[i].strk 
            self.tasks[i].strk = (a+1)%2

    def strk_del(self):
        # remove (permanent) all stricken entries
        for i in range(len(self.tasks)-1,-1,-1): # go backwards...
            if self.tasks[i].strk:
                self.rm(i)
        
    def fsh(self,i):
        if self.goodind(i):
            self.tasks[i].mark = 0  # could just make a new task...
            self.add(self.tasks.pop(i))
