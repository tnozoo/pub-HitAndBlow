import argparse;

parser = argparse.ArgumentParser();
parser.add_argument('--keta', '-k', help = '桁数', type = int, default = 4);
args = parser.parse_args();
print(args.keta);

