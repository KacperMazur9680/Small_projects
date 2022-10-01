file = "./dna_reader/dna_data/dna.fastq"
x = {}
y = []
strands = []
gc = []

with open(file, "r") as stream:
    content = stream.read()

dnas = ["@SRR" + info for info in content.split("@SRR") if info]
reads = len(dnas)

for info in dnas:
    info_f = info.split("\n")
    read_ = info_f[1]
    length = len(read_)
    x[length] = x.get(length, 0) + 1
    y.append(length)
    strands.append(read_)

print(f"Reads in the file = {reads}")
for key, value in x.items():
    print(f"    with length {key} = {value}")

print(f"Reads sequence average length = {int(round(sum(y)/reads, 0))}")

print()
print(f"Repeats = {len(strands) - len(set(strands))}")
print()


for strand in strands:
    gc_content = 0
    for form in strand:
        if form == "G" or form == "C":
            gc_content += 1
    gc.append(round(gc_content / len(strand) * 100, 2))

print(f"GC content average = {round(sum(gc) / reads, 2)}%")