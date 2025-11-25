import sys
import gzip
import random

# usage : python rescale.py reference.hist query.bed.gz output.bed

if len(sys.argv) < 4:
    print("need 3 files")
    sys.exit()

ref_file = sys.argv[1]
query_file = sys.argv[2]
out_file = sys.argv[3]

# 1. read refrence file
ref_probs = {}
f = open(ref_file, "r")
for line in f:
    parts = line.split()
    if len(parts) > 1:
        l = int(parts[0])
        p = float(parts[1])
        ref_probs[l] = p
f.close()

# 2. count qury file 
my_counts = {}
# using gzip bcoz input is .gz
f = gzip.open(query_file, "rt")
for line in f:
    parts = line.split()
    # length is end - start
    l = int(parts[2]) - int(parts[1])
    
    if l in my_counts:
        my_counts[l] += 1
    else:
        my_counts[l] = 1
f.close()

# 3. calcluate ratio
min_ratio = 1000000.0
for l in my_counts:
    if l in ref_probs:
        p = ref_probs[l]
        c = my_counts[l]
        
        if p > 0:
            ratio = c / p
            if ratio < min_ratio:
                min_ratio = ratio

print("scaling ratio:", min_ratio)

# 4. wrtie ouput file
f1 = gzip.open(query_file, "rt")
f2 = open(out_file, "w")

for line in f1:
    parts = line.split()
    l = int(parts[2]) - int(parts[1])
    
    if l in ref_probs and l in my_counts:
        # math to decide if we keep the line
        prob = (ref_probs[l] * min_ratio) / my_counts[l]
        
        if random.random() < prob:
            f2.write(line)

f1.close()
f2.close()
print("done")