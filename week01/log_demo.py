import logging

DATEFMT = '%Y-%m-%d %H:%M:%S'
FORMAT = '%(asctime)s %(name)20s %(levelname)s [line: %(lineno)d] %(message)s'
logging.basicConfig(filename='test1.log',
                    datefmt=DATEFMT,
                    format=FORMAT,
                    level=logging.DEBUG)
logging.info('你好 %s', 1)
