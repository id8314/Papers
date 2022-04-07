# Exportig top 10 families reviews to file

from collections import Counter
from time import time
from common import ptime, now

SOURECE_DATAFILE = "amazon_reviews_us_Automotive_v1_00.tsv"
TARGET_DATAFILE = "amazon_reviews_us_Automotive_v1_00_SHORT.tsv"
product_families = Counter()

print(f"Start: {now()}")
t0 = time()
n = 0

with open(SOURECE_DATAFILE,"r",encoding="utf-8") as sf:
    while True:
        line = sf.readline()
        if not line:
            break
        if n > 0: # skip header (n == 0)
            f = line.split('\t')
            #print(f[4],f[5])
            product_families.update({f"{f[4]}":1}) # increment product family f[4] count
        n+=1
        if n % 100000 == 0:
            print(f"{n} lines processed",end="\r")

print(f"{n} lines processed")
print(f"{n} Records\nFound {len(product_families)} product families\n")

families_to_study = []
print("Top 10 families with reviews:")
print(f"code\t\treviews")
for family, frequency in product_families.most_common(10):
    print(f"{family}\t{frequency}")
    families_to_study.append(family)

print("\nExportig top 10 families reviews to file",TARGET_DATAFILE)
n = 0
exported = 0
with open(SOURECE_DATAFILE,"r",encoding="utf-8") as sf:
    with open(TARGET_DATAFILE,"w",encoding="utf-8") as tf:
        while True:
            line = sf.readline()
            if not line:
                break

            if n > 0:
                f = line.split('\t')
                if f[4] in families_to_study:
                    tf.write(line)
                    exported += 1
            else:
                tf.write(line) # write header

            n+=1
            if n % 100000 == 0:
                print(f"{n} lines processed",end="\r")
            
print(f"{n} lines processed\n{exported} records exported")
print(f"\nProcessing time: {ptime(time()-t0)}\n")
