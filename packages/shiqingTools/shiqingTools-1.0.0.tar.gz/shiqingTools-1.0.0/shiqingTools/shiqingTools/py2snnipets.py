from argparse import ArgumentParser

parse = ArgumentParser()
parse.add_argument("-i", "--input", default=r'input.py', type=str)
parse.add_argument("-o", "--output", default=r'output.txt', type=str)

args=parse.parse_args()


with open(args.input,"r") as f:
    lines = f.readlines()
    lines = ["\""+line.strip("\n")+"\""+",\n"  for line in lines if line.strip()!=""]

with open(args.output,"w") as g:
    g.writelines(lines)

