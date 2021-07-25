import sys
import argparse
from perspective_utils import make_list_cube

# image = str(sys.argv[1])
parser = argparse.ArgumentParser()
parser.add_argument("--image_name", help="name of the image you want to put in perspective (for example "
                                         "smiley", type=str)
args = parser.parse_args()
print(args)
make_list_cube(args.image_name)
