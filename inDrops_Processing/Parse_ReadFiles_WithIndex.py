import argparse
import gzip



def get_read(input):
    line = input.readline()
    #Gzipped files read in byte like objects. Decode to ascii string, but only if its currently in bytes
    try:
        line = line.decode().rstrip()
    except (UnicodeDecodeError, AttributeError):
        line = line.rstrip()
    if len(line)==0:
        line = input.readline()   #Allow for possibility of blank line?
        try:
            line = line.decode().rstrip()
        except (UnicodeDecodeError, AttributeError):
            line = line.rstrip()
    if len(line) == 0: return None      #No read here -- end of file?
    if line[0] != "@":
        print("Error -- fastq file possibly corrupted. First character does not match @. line: {}".format(line))
        exit()
    new_read = [line]
    for i in range(3):
        line = input.readline()
        try:
            line = line.decode().rstrip()
        except (UnicodeDecodeError, AttributeError):
            line = line.rstrip()
        new_read.append(line)
    return new_read


def verify_reads(R1, R2, R3, R4):
    cur_read = R1[0].split()[0]
    for read in [R2, R3, R4]:
        if(read[0].split()[0] == cur_read):
            continue
        else:
            print("Read name mismatch. It seems all reads might not be in the same order across files. Read:\n{}".format(read))
            exit()
    return


def create_write_read(R1, R2, R4, out_files):
    new_R1 = R1
    bc1 = R2[1]
    if len(bc1) < 8:
        print("WARNING: barcode 1 read less than required 8. Skipping this read...")
        return
    bc1 = bc1[:8]
    bc1_qs = R2[3][:8]
    if len(R4[1]) < (8+6):
        print("WARNING: barcode 2 and UMI read less than required 14. Skipping this read...")
        return
    bc2 = R4[1][:8]
    bc2_qs = R4[3][:8]
    umi = R4[1][8:(8+6)]
    umi_qs = R4[3][8:(8+6)]
    new_R2 = [R2[0]]
    new_R2.append(bc1 + bc2 + umi)
    new_R2.append("+")
    new_R2.append(bc1_qs + bc2_qs + umi_qs)
    R1_write = "\n".join(new_R1) + "\n"
    out_files["R1"].write(R1_write.encode())
    R2_write = "\n".join(new_R2) + "\n"
    out_files["R2"].write(R2_write.encode())
    return


def convert_reads(R1, R2, R3, R4, indices, do_index_matching, out_files):
    R1_read = "start"       #Initialize for while loop...
    while R1_read:
        R1_read = get_read(R1)
        if not R1_read: continue            #Empty read -- EOF
        R2_read = get_read(R2)
        R3_read = get_read(R3)
        R4_read = get_read(R4)
        verify_reads(R1_read, R2_read, R3_read, R4_read)
        if not do_index_matching:       #No index matching needed
            create_write_read(R1_read, R2_read, R4_read, out_files[indices[0]])
        else:
            lib_ind = R3_read[1][:8]
            if lib_ind in indices:
                create_write_read(R1_read, R2_read, R4_read, out_files[lib_ind])
    return



def main(R1_in, R2_in, R3_in, R4_in, indices, R1_out_base, R2_out_base, force_index_match):
    indices = indices.split(",")
    if len(indices) > 1:        #If we have more than one library index we have to use index matching
        force_index_match = True
    out_files = {}
    for ind in indices:
        if ind in out_files:
            print("Potentially duplicated library index? {}".format(ind))
            exit()
        out_files[ind] = {"R1": gzip.open("{}_{}.fastq.gz".format(R1_out_base, ind), 'wb'),
                          "R2": gzip.open("{}_{}.fastq.gz".format(R2_out_base, ind), 'wb')}
    if R1_in.endswith('gz'): #input files seem gzipped. Make sure they all are:
        for R_in in [R2_in, R3_in, R4_in]:
            if not R_in.endswith('gz'):
                print("It seems some of input files are not gzipped. All files need to be either gzipped or not gzipped.")
                exit()
        with gzip.open(R1_in, 'rb') as R1, \
                gzip.open(R2_in, 'rb') as R2, \
                gzip.open(R3_in, 'rb') as R3, \
                gzip.open(R4_in, 'rb') as R4:
            convert_reads(R1, R2, R3, R4, indices, force_index_match, out_files)
    else:
        with open(R1_in, 'r') as R1, \
                open(R2_in, 'r') as R2, \
                open(R3_in, 'r') as R3, \
                open(R4_in, 'r') as R4:
            convert_reads(R1, R2, R3, R4, indices, force_index_match, out_files)
    for ind in out_files:
        out_files[ind]["R1"].close()
        out_files[ind]["R2"].close()
    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--R1', help='R1 read file')
    parser.add_argument('--R2', help='R2 read file')
    parser.add_argument('--R3', help='R3 read file')
    parser.add_argument('--R4', help='R4 read file')
    parser.add_argument('--indices', help="semicolon separated list of LIBRARY indices to expect (these are in R3).")
    parser.add_argument("--force_index_match", action='store_true', default=False, help="This option will only output reads where the library index is an exact match to what is expected. Default behavior is to output all reads in cases where all reads are expected to come from one library (e.g. one lane is composed of only one library), even if the library index has sequencing errors in it.")
    parser.add_argument('--R1_out', help='R1 output read file base name (lib index will be appended)')
    parser.add_argument('--R2_out', help='R2 output read file base name (lib index will be appended)')
    x = parser.parse_args()
    
    
    main(x.R1, x.R2, x.R3, x.R4, x.indices, x.R1_out, x.R2_out, x.force_index_match)
