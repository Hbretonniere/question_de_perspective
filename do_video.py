import sys
from perspective_utils import make_movie

image = str(sys.argv[1])
fps = str(sys.argv[2])
make_movie(image, int(fps))
