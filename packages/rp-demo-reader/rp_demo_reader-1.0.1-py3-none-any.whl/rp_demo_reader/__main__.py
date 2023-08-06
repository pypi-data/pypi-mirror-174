import sys
from rp_demo_reader.multireader import MultiReader

r = MultiReader(sys.argv[1])
print(r.read())
r.close()
