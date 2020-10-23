from datetime import datetime
import logging
from accessify import protected
import random

ticks_to_change = 20
workset_halfwidth = 2


class Memory:
    """ класс, представляющий память в целом """

    def __init__(self, ph_cells=32):
        """ конструктор класса
            ph_cells - количество страниц физической памяти
            vprocesses - процессы виртуальной памяти """
        self.pm = PhMemory(ph_cells)
        self.vm = VMemory()

    def __str__(self):
        res = 'Physical memory\n' + str(self.pm) + str(self.vm)
        return res

    def addprocess(self, pages):
        self.vm.addprocess(pages)

    def putinpm(self, Nprocess, Npage):
        pmpage = self.pm.choosepage()
        self.pm.addprocessbypage(pmpage, Nprocess, Npage)
        self.vm.processes[Nprocess].allocation[Npage] = pmpage

    def choosepagevm(self):
        process = random.randint(0, len(self.vm.processes) - 1)
        page = choose_page(len(self.vm.processes[process].allocation),
                           self.vm.processes[process].startpage, workset_halfwidth)
        logging.info('Page #{!s} of process #{!s} is chosen to insert'.format(page, process))
        return process, page


# классы, моделирующие физическую память
class PhMemory:
    """ физическая память """

    def __init__(self, size=32):
        self.size = size
        self.space = [Page() for i in range(0, size)]

    def __str__(self):
        res = ''
        for i in range(0, self.size):
            if self.space[i].process == -1:
                res += '#{!s}: ---\n'.format(i)
            else:
                res += '#{!s}: Process:{!s}, Page:{!s}, Allocated:{!s}\n'. \
                    format(i, self.space[i].process, self.space[i].page, self.space[i].settime)
        return res

    def addprocessbypage(self, N, processN, pageN):
        try:
            self.space[N] = Page(process=processN, page=pageN)
            logging.info('Cell #{!s} allocated for page #{!s} of process #{!s}'.format(N, processN, pageN))
            return True
        except:
            return False

    def choosepage(self):
        return random.randint(0, len(self.space)-1)


class Page:
    """ страница физической памяти """
    def __init__(self, process=-1, page=-1):
        self.settime = datetime.now()
        self.process = process
        self.page = page


# классы, моделирующие виртуальную память
class VProcess:
    """ класс, представляющий процессы, размещаемые в виртуальной памяти """

    def __init__(self, size):
        self.allocation = [-1] * size
        self.startpage = random.randint(0, size-1)
        self.tick_to_change=ticks_to_change


class VMemory:
    """ класс, представляющий виртуальную память """

    def __init__(self):
        self.processes = []

    def __str__(self):
        res = 'Virtual memory\n' + 'Number of process: {!s}\n'.format(len(self.processes))
        if len(self.processes) > 0:
            for item in self.processes:
                res += 'Process #{!s} has {!s} pages\n'.format(self.processes.index(item), len(item.allocation))
            for item in self.processes:
                res += 'Process #{!s}\n'.format(self.processes.index(item))
                for i in range(0, len(item.allocation)):
                    res += 'Page #{!s} is allocated on {!s} page of ph. memory\n' \
                        .format(i, item.allocation[i]) if item.allocation[i] != -1 else 'Page #{!s} is not allocated in ' \
                                                                                      'physical memory\n'.format(i)
        return res

    def addprocess(self, pages):
        self.processes.append(VProcess(pages))

    def deleteprocess(self, N):
        self.processes.pop(N)


def choose_page(fullsize, center, halfwidth):
    workset = [i for i in range(center-halfwidth if center-halfwidth > -1 else 0,
                                center+halfwidth+1 if center+halfwidth < fullsize else fullsize)]
    res = [i for i in range(0, center-halfwidth)]
    rest2 = [i for i in range(center+halfwidth+1, fullsize+1)]
    res.extend(workset * 9)
    res.extend(rest2)
    random.shuffle(res)
    return random.choice(res)