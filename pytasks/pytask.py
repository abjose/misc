import sys, tty, termios, re

# SPLIT UP INTO FILES!
# -> in doing so, should make easier to create new 'doing' intefaces
#    (i.e. add new ways of completing tasks)
#    So would make sense to have single class/file for files, then 
#    one each for different methods - have meta/superclass as well?
# ADD PROJECTS (TAGS)!
# REIMPLEMENT IN WXPYTHON, CALL 'DOPY'?

class tfx:
    # should delete some of these, or move elsewhere
    # terminal/cursor  modification
    CLEARSCRN = '\x1b[H\x1b[2J'
    NOBLINK = '\033[25m'
    # effects
    STRIKE = '\033[9m'
    BOLD = '\033[1m'
    NEGATIVE = '\033[7m'
    # background colors
    BGCYAN = '\033[106m'
    BGMAGENTA = '\033[105m'
    BGBLUE = '\033[104m'
    BGYELLOW = '\033[103m'
    BGREEN = '\033[102m'
    BGRED = '\033[101m'
    BGBLACK = '\033[100m'
    # foreground colors
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLACK = '\033[90m'
    # other
    NRML = '\033[0m'
        
    @staticmethod
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch



'''
would be cool to implement a variety of different 'getting stuff done' methods, and then have a single text file in this folder

Then could run any of the programs and edit the list in that 'mode'
Perhaps each 'method' should just be its own class...

'''

class Task:
    def __init__(self, task):
        self.mark = 0
        self.bold = 0
        self.strk = 0
        self.task = task  # task description

    def __str__(self):
        return self.task
    def save(self):
        info = str(self.mark)+'/'+str(self.bold)+'/'+str(self.strk)+': '
        return info+self.task

class TaskList:
    # Handles printing slices of tasklist, numbering, etc...
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


cmds = {'z':'fsh', 'l':'fsh',
        'Z':'hlt_fsh',  'L':'hlt_fsh',
        'c':'strk', 'k':'strk',
        'C':'strk_del',  'K':'strk_del',
        'x':'mrk', ' ':'mrk', 'm':'mrk',  'j':'mrk',
        'X':'mrk_mode', 'M':'mrk_mode',  'J':'mrk_mode',
        'q':'mrk_mode_exit',
        'v':'hlt', 'h':'hlt',  ';':'hlt',
        'V':'hlt_clr', 'H':'hlt_clr',  ':':'hlt_clr',
        'w':'up', '8':'up',
        's':'down', '2':'down',
        'a':'left', '4':'left',
        'd':'right', '6':'right',
        chr(13):'input',
        '?':'help',
        'Q':'quit'}

class TaskProc:

    def __init__(self):
        self.head = 0
        self.pgsize = 20 # make option...
        self.taskscache = None
        self.tasks = TaskList()
        self.markmode = 0
        self.loop()

    def loop(self):
        title = "PYTASK :: '?' helps, 'Q' quits"
        self.read()
        go = True
        while go:
            print tfx.CLEARSCRN+title
            self.fixhead()
            if len(self.marklist()) == 0: self.markmode = 0
            self.chunk(self.head,self.pgsize)
            go = self.parse(tfx.getch())
        print tfx.NRML # just in case...
        print 'saving and quitting...'
        self.save()

    def parse(self,c):
        # should perhaps split up...
        #assert c in cmds.keys()
        val = None
        if c in cmds.keys(): val = cmds[c]
        
        if val == 'input':
            self.addTask()
        if val == 'fsh':
            self.tasks.fsh(self.gethead())
        elif val == 'hlt_fsh':
            self.tasks.hlt_fsh()
        elif val == 'strk':
            self.tasks.strk(self.gethead())
        elif val == 'strk_del':
            self.tasks.strk_del()
        elif val == 'mrk':
            self.tasks.mrk(self.gethead(), self.markmode)
        elif val == 'mrk_mode':
            self.head = 0
            self.markmode = 1
        elif val == 'mrk_mode_exit': 
            self.head = 0
            self.markmode = 0
        elif val == 'hlt':
            self.tasks.hlt(self.gethead())
        elif val == 'hlt_clr':
            self.tasks.hlt_clr()
        elif val == 'up':
            self.head -= 1
        elif val == 'down':
            self.head += 1
        elif val == 'right':
            self.head += self.pgsize
        elif val == 'left':
            self.head -= self.pgsize            
        elif val == 'help':
            self.help() 
        elif val == 'quit':
            return False
        return True

    def addTask(self):
        inp = raw_input(tfx.GREEN+'  >> '+tfx.NRML)
        if inp != '': self.tasks.add(inp)

    def fixhead(self):
        # this is ugly
        if self.head < 0: self.head = 0
        else:
            tk = self.tasks
            if self.markmode: tk = [i for i in self.tasks if i.mark == 1]
            if self.head > len(tk)-1: self.head = len(tk)-1

    def gethead(self): # hurhur
        return self.head if not self.markmode else self.tasks.mm_ind(self.head)
        
    def marklist(self):
        # hopefully passes pointers...
        tk = self.tasks
        if not self.markmode and  not tk[0].mark: tk[0].mark = 1
        return [tk[i] for i in range(len(tk)-1,-1,-1) if tk[i].mark == 1]

    def help(self):
        out = "Help function placeholder"
        print out
        
    def save(self, name='pytasks.txt'):
        with open(name, 'w') as f:
            for i in range(len(self.tasks)):
                f.write(self.tasks[i].save()+'\n')

    def read(self, name='pytasks.txt'):
        frmt = '[01]/[01]/[01]: *'
        self.tasks = TaskList()
        with open(name) as f:
            for line in f:
                m = re.match(frmt, line)
                if m: # preformatted
                    t = Task(line[m.end():].rstrip())
                    t.mark = int(line[0])
                    t.bold = int(line[2])
                    t.strk = int(line[4])
                    self.tasks.add(t)
                else: # user-entered/unformatted
                    self.tasks.add(line.rstrip())

    def chunk(self, head,size):
        """ Determine which chunk to display based on head loc and pg size """
        a = max(0,head//size)*size
        b = min(a+size,len(self.tasks))
        # not very nice
        rndr,tk = [],self.tasks
        if self.markmode: rndr = self.marklist()
        else: rndr = [tk[i] for i in range(a,b)]
        
        for i,t in enumerate(rndr):
            label = '  ' + str(i) + ': '
            task = str(t)
            if t.strk: task = tfx.STRIKE+task
            if t.bold: task = tfx.NEGATIVE+task
            if t.mark or i == 0: label = 'X' + label[1:]
            out = label+task
            if i == head: out = tfx.NEGATIVE+out
            if i%2==0: print tfx.CYAN + out + tfx.NRML
            else: print tfx.BLUE + out + tfx.NRML
        # PUT STRING FORMATTING HERE FOR NUMBER LABELSSssss!!11!111

#while True:
#    print(tfx.getch())
TaskProc()
