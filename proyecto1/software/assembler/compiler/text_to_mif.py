import argparse

ap = argparse.ArgumentParser(description='Convert .txt init file to .mif')
ap.add_argument("-i","--input", required=True, help="name of input txt")
ap.add_argument("-o","--output", required=True, help="name of output mif")

args = vars(ap.parse_args())
txtfile = open(args["input"],'r')
miffile = open(args["output"],'w')

lines = txtfile.readlines()
if '\n' in lines: lines.remove('\n')
depth = len(lines)*4

initial_text = f"""
WIDTH=8;
DEPTH={depth};
ADDRESS_RADIX=HEX;
DATA_RADIX=BIN;

CONTENT BEGIN
"""
miffile.write(initial_text)

addr = 0
for line in lines:
    line = line.strip('\n')
    miffile.write(f"\t{addr:<6X}: {line[24:32]} {line[16:24]} {line[8:16]} {line[0:8]};\n")
    addr += 4

miffile.write("END;")


txtfile.close()
miffile.close()