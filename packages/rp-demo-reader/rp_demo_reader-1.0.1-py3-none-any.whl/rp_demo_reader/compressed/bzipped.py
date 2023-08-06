import bz2
from rp_demo_reader.util import writer

opener = bz2.open

if __name__ == '__main__':
    writer.main(opener)
