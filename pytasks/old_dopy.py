from task import Task
from project import Project as proj
from display import Display as disp
#from cli import Interface as cli

""" Maintains a list of projects.  Central class of dopy. """

class Dopy:
    def __init__(self):
        # perhaps attempt to load from local file...or create new dopy.
        self.tags = {'':[]}
        self.order = [] # manages order of displayed tags/tasks
        self.hide = [] # list of tasks and tags to not render
        self.mode = '' # name of tag to list contents of. '' is all.
        self.rdr = [] # printed list of tasks, for reference/lookup
 
    def __str__(self):
        return disp.draw(self.rdr)

    def parse(self, line, task=False):
        """ Take line (from cmd arg) as input, converts to whatever was
        probably intended.
        """
        if line in self.tags.keys():
            if task: return self.tags[line][0]
            return line
        elif line.isdigit() and 0 <= int(line) < len(self.rdr):
            return self.rdr[int(line)]
        return None

    def render(self):
        """ Return list of current tasks (i.e. tasks to be displayed) """
        
        # TO HAVE TAG NAMES NEXT TO TASK, could add tag variable to tasks
        # or could make render into list of (tag,task) tuples...?

        rdr = [] # list of task objects
        if self.mode != '': rdr = self.tags[self.mode]
        else:
            for task in self.order:
                if task not in self.hide:
                    if type(task) == str: 
                        if self.tags[task] == []: continue
                        task = self.tags[task][0]
                    rdr.append(task)
        self.rdr = rdr

    def update(self):
        """ Update various things """
        #self.updateOrder()
        self.updateHide()
        self.render()
    
    #def updateOrder(self):
    #    for 

    def updateHide(self):
        """ Update times, remove if time == 0 """
        newHide = []
        for task,time in self.hide:
            if time > 0: newHide.append((task, time-1))
        self.hide = newHide

    def addHide(self, task, time):
        """ Add to hide list. Task can be task object or tag. """
        time = int(time)
        if time > 0: self.hide.append((task,time))

    def setMode(self, tag):
        self.mode = '' if tag == 'all' else tag

    def addTask(self, task, tag=''):
        # NEED TO CHECK FOR TASKINESS
        if tag not in self.tags.keys(): self.addTag(tag)
        if type(task) == str: task = Task(task)
        self.tags[tag].append(task)# if task not in self.tags[tag]
        self.order.append(task)

    def rmTask(self, task, tag=None):
        taglist = [tag] if tag != None else self.tags.keys()
        for key in taglist:
            self.tags[key] = filter(lambda x: x != task, self.tags[key])
        self.order.remove(task)

    def mvTask(self, task, tag):
        self.rmTask(task)
        self.addTask(task, tag=tag)

    def popTask(self, task):
        i = self.order.index(task)
        self.order.append(self.order.pop(int(i)))

    def addTag(self, tag):
        if not tag in self.tags: self.tags[tag] = []
        self.order.append(tag)

    def rmTag(self, tag):
        if tag in self.tags: del self.tags[tag]
        self.order.remove(tag)
    
    



        
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

    
