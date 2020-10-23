from memory import Memory
import logging


def launch():
    a = Memory(ph_cells=6)
    a.addprocess(8)
    a.addprocess(12)
    for j in range(0, 5):
        a.resetR_bytes()
        for i in range(0, 20):
            process, page = a.choosepagevm()
            if process is not None:
                a.choosepagepm(process, page)
    print(a)


if __name__ == '__main__':
    logging.basicConfig(filename='memory.log', filemode='w', format='%(asctime)s - %(message)s',
                        level=logging.INFO)
    logging.info('Start logging')
    launch()
    logging.info('Stop logging')