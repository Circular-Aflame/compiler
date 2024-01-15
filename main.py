from generator import Generator
import sys

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc >= 2:
        generator = Generator()
        if argc == 2:
            input_file = sys.argv[1]
            output_file = '.'.join(input_file.split('.')[:-1]) + '.py'
            generator.translate(input_file, output_file)
        else:
            input_file = sys.argv[1]
            output_file = sys.argv[2]
            generator.translate(input_file, output_file)
    else:
        print("usage: python main.py input_filename [output_file]")