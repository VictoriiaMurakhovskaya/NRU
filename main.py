from memory import Memory
import logging


def print_hi():
    a = Memory(ph_cells=4)
    a.addprocess(4)
    a.addprocess(2)
    a.putinpm(0, 3)
    a.putinpm(1, 1)
    for i in range(0, 10):
        process, page = a.choosepagevm()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(filename='memory.log', filemode='w', format='%(asctime)s - %(message)s',
                        level=logging.INFO)
    logging.info('Start logging')
    print_hi()
    logging.info('Stop logging')