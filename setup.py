from helper import check_bool
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("flps", type=int)
parser.add_argument("epns", type=int)
parser.add_argument("--hold", type=check_bool)
args = parser.parse_args()

if args.hold:
    bash_start = ["xterm", "-hold", "-e", "python"]
else:
    bash_start = ["xterm", "-e", "python"]


def setup():
    bash_icn = bash_start + ["icn.py", str(args.epns)]
    bash_flp = bash_start + ["flp.py"]
    bash_epn = bash_start + ["epn.py"]

    subprocess.Popen(bash_icn)

    port = 5557

    for _ in range(args.epns):
        bash_flp += [str(port)]
        subprocess.Popen(bash_epn + [str(port)])
        port += 1

    for _ in range(args.flps):
        subprocess.Popen(bash_flp)


if __name__ == "__main__":
    setup()
