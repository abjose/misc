import sys, tty, termios

'''
would be cool to implement a variety of different 'getting stuff done' methods, and then have a single text file in this folder

Then could run any of the programs and edit the list in that 'mode'
Perhaps each 'method' should just be its own class...

'''

class tfx:
    # should delete some of these, or move elsewhere
    # terminal/cursor  modification
    CLEARSCRN = '\x1b[H\x1b[2J'
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

class Task:
    def __init__(self, task):
        self.mark = 0
        self.bold = 0
        self.task = task  # task description

    def __str__(self):
        return self.task
        

class TaskList:
    # Handles printing slices of tasklist, numbering, etc...
    def __init__(self):
        self.tasks = []

    def __len__(self):
        return len(self.tasks)
        
    def goodind(self,i):
        return 0 <= i < len(self.tasks)

    def add(self,task):
        self.tasks.append(task)
        return True

    def ins(self,task,i):
        if self.goodind(i):
            self.tasks.insert(i,task)
        return True

    def rm(self,i):
        if self.goodind(i):
            self.tasks.pop(i)
        return True

    def mrk(self,i):
        if self.goodind(i):
            a = self.tasks[i].mark 
            self.tasks[i].mark = (a+1)%2
        return True

    def hlt(self,i):
        if self.goodind(i):
            a = self.tasks[i].bold 
            self.tasks[i].bold = (a+1)%2
        return True

    def fsh(self,i):
        if self.goodind(i):
            self.add(self.tasks.pop(i))
        return True

    def chunk(self, a,b):
        # make pythonic
        a = max(0,a)
        b = min(b,len(self.tasks)-1)
        if a <= b:
            for i in range(a,b+1):
                t = self.tasks[i]
                label = '  ' + str(i) + ': '
                task = str(t)
                if t.bold: task = tfx.NEGATIVE+task
                if t.mark: label = 'X' + label[1:]
                if i%2==0: print tfx.CYAN + label+task + tfx.NRML
                else: print tfx.BLUE + label+task + tfx.NRML
        #else: print 'Chunk no good'
            

class TaskProc:
    args = '(int(s[1:]))'
    takeargs = {'x':'rm'+args,
                'h':'hlt'+args,
                'm':'mrk'+args,
                'c':'fsh'+args}
    # oh god what is this
    noargs = {'q':'False',
              '[':'self.shiftchunk(-self.chunksize)',
              ']':'self.shiftchunk(self.chunksize)',
              '?':'self.help()'}

    def __init__(self):
        self.chunksize = 20 # make option...
        self.tasks = TaskList()
        self.start = 0
        self.loop()

    def loop(self):
        print "'?' for Help"
        go = True
        while go:
            print tfx.CLEARSCRN
            self.tasks.chunk(self.start,self.start+self.chunksize)
            inp = raw_input(tfx.GREEN+'--> '+tfx.NRML).replace('"',"'")
            go = self.parse(inp)
            
        print 'Saving and quitting.'
        self.save()
        print tfx.NRML # just in case...perhaps not necessary

    def shiftchunk(self,shift):
        if 0 <= self.start+shift < len(self.tasks)-1:
            self.start += shift
        return True

    def parse(self, s):
        # determine if string is good, what command type, then dispatch
        if len(s) == 1 and s in TaskProc.noargs.keys():
            return self.parseNoArgs(s)
        elif len(s) > 1 and s[0] in TaskProc.takeargs.keys():
            if  unicode(s[1:]).isnumeric():
                return self.parseArgs(s)
        return self.addTask(s)

    def parseNoArgs(self,s):
        pre = ''
        return eval(pre+TaskProc.noargs[s[0]])

    def parseArgs(self,s):
        pre = 'self.tasks.'
        return eval(pre+TaskProc.takeargs[s[0]])

    def help(self):
        out = "Help function placeholder"
        print out
        return True

    def addTask(self,s):
        #print 'Adding task'
        return self.tasks.add(Task(s))
        
    def save(self):
        """ Should be human readable/writable, but also save bolds/marks """
        # can save with #,# pair before string, but if not there assume 0,0
        pass

    def read(self, name=None):
        pass

    

#while True:
#    print(tfx.getch())
TaskProc()
