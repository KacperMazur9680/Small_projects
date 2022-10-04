import gzip


file1 = "data1.gz"
file2 = "data2.gz"
file3 = "data3.gz"

files = [file1, file2, file3]

files_info = {}

for file in files:
    with gzip.open(file, "rt") as stream:
        content = stream.read()

    lengths_counter = {}
    lengths = []
    strands = []
    gc = []
    ns = []
    n = 0
    undef_nucl = 0

    dnas = ["@SRR" + info for info in content.split("@SRR") if info]
    reads = len(dnas)

    for info in dnas:
        info_f = info.split("\n")
        read_ = info_f[1]
        length = len(read_)
        lengths_counter[length] = lengths_counter.get(length, 0) + 1
        lengths.append(length)
        strands.append(read_)

    avg_len = int(round(sum(lengths)/reads, 0))

    reps = len(strands) - len(set(strands))

    for strand in strands:
        undef_nucl = 0
        if "N" in strand:
            n += 1
            for nucl in strand:
                if nucl == "N":
                    undef_nucl += 1
            ns.append(undef_nucl * 100 / len(strand))

    for strand in strands:
        gc_content = 0
        for form in strand:
            if form == "G" or form == "C":
                gc_content += 1
        gc.append(round(gc_content / len(strand) * 100, 2))

    avg_gc = f"{round(sum(gc) / reads, 2)}%"
    ns_per_read = f"{round(sum(ns) / reads , 2)}%"

    files_info.update({file: [reads, avg_len, reps, n, avg_gc, ns_per_read]})

files_reps_ns = []
for file, info in files_info.items():
    if info[2] == 0:
        files_reps_ns.append(info[3])

best_file = min(files_reps_ns)

for key, value in files_info.items():
    if best_file == value[3]:
        print(key)
        print(f"Reads in the file = {value[0]}")
        print(f"Reads sequence average length = {value[1]}\n")
        print(f"Repeats = {value[2]}")
        print(f"Reads with Ns = {value[3]}\n")
        print(f"GC content average = {value[4]}")
        print(f"Ns per read sequence = {value[5]}")