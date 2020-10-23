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

    def choosepagevm(self):
        process = random.randint(0, len(self.vm.processes) - 1)
        page = choose_page(len(self.vm.processes[process].allocation),
                           self.vm.processes[process].startpage, workset_halfwidth)
        logging.info('Page #{!s} of process #{!s} is chosen to insert'.format(page, process))
        try:
            if self.vm.processes[process].allocation[page] != -1:
                logging.info('Page #{!s} of process #{!s} is already inserted'.format(page, process))
                return None, None
            logging.info('Page #{!s} of process #{!s} will be inserted'.format(page, process))
        except:
            print(process, page)
        return process, page

    def choosepagepm(self, process, page):
        a, b, c = self.pm.choosepagepm(process, page)
        self.vm.processes[process].allocation[page] = a
        if b is not None:
            self.vm.processes[b].allocation[c] = -1

    def resetR_bytes(self):
        self.pm.reset_R_bytes()


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
                res += '#{!s}: Process:{!s}, Page:{!s}, Byte R: {!s}, Allocated at:{!s}\n'. \
                    format(i, self.space[i].process, self.space[i].page, self.space[i].R_byte,
                           self.space[i].settime)
        return res

    def choosepagepm(self, process, page):
        for item in self.space:
            if not item.allocated():
                item.allocate(process, page)
                logging.info(
                    'Cell #{!s} allocated for page #{!s} of process #{!s}'.format(self.space.index(item), process,
                                                                                  page))
                return self.space.index(item), None, None

        logging.info('All cells are used. Starting NRU algorithm')
        for item in self.space:
            if not item.R_byte:
                b = item.process
                c = item.page
                item.allocate(process, page)
                logging.info(
                    'Cell #{!s} allocated for page #{!s} of process #{!s}'.format(self.space.index(item), process,
                                                                                  page))
                return self.space.index(item), b, c
        item = self.space[0]
        b = item.process
        c = item.page
        item.allocate(process, page)
        return 0, b, c

    def reset_R_bytes(self):
        logging.info('Resetting R bits')
        for item in self.space:
            item.R_byte = False


class Page:
    """ страница физической памяти """

    def __init__(self, process=-1, page=-1):
        self.settime = datetime.now()
        self.process = process
        self.page = page
        self.R_byte = False
        self.M_byte = False

    def allocated(self):
        if self.process == -1:
            return False
        else:
            self.R_byte = True
            return True

    def allocate(self, process, page):
        self.process = process
        self.page = page
        self.R_byte = True


# классы, моделирующие виртуальную память
class VProcess:
    """ класс, представляющий процессы, размещаемые в виртуальной памяти """

    def __init__(self, size):
        self.allocation = [-1] * size
        self.startpage = random.randint(0, size - 1)
        self.tick_to_change = ticks_to_change


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
                        .format(i, item.allocation[i]) if item.allocation[
                                                              i] != -1 else 'Page #{!s} is not allocated in ' \
                                                                            'physical memory\n'.format(i)
        return res

    def addprocess(self, pages):
        self.processes.append(VProcess(pages))

    def deleteprocess(self, N):
        self.processes.pop(N)


def choose_page(fullsize, center, halfwidth):
    workset = [i for i in range(center - halfwidth if center - halfwidth > -1 else 0,
                                center + halfwidth + 1 if center + halfwidth < fullsize else fullsize)]
    res = [i for i in range(0, center - halfwidth)]
    rest2 = [i for i in range(center + halfwidth + 1, fullsize)]
    res.extend(workset * 9)
    res.extend(rest2)
    random.shuffle(res)
    return random.choice(res)
