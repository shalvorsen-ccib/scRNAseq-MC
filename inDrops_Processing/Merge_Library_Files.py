import argparse
import os
import subprocess


def read_mapping_file(file):
    lib_map = {}
    with open(file, 'r') as input:
        line = input.readline()     #Skip header
        line = input.readline()
        while line:
            s_line = line.split()
            if s_line == []:     #Blank line
                line = input.readline()
                continue
            run_id = s_line[0]
            lib_index = s_line[1]
            lib_label = s_line[2]
            if run_id not in lib_map:
                lib_map[run_id] = {}
            if lib_index in lib_map[run_id]:
                print("ERROR: There seems to be a duplicated run ID - lib index pair in the metadata file...")
                exit()
            lib_map[run_id][lib_index] = lib_label
            line = input.readline()
    return lib_map


def parse_filename(fname):
    s_f = fname.split("_")
    run = s_f[0]
    lane = s_f[1]
    read = s_f[2]
    index = s_f[3].split(".")[0]
    return (run, lane, read, index)



def main(basedir, map_file, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    processes = []
    concat_lists = {}
    lib_mapping = read_mapping_file(map_file)
    files = os.listdir(basedir)
    for file in files:
        if file.endswith(".fastq.gz"):
            run_num, lane_num, read_num, lib_ind = parse_filename(file)
            if read_num == "R2": continue       #infer R2 name from R1 name to keep everything in same order
            R1_file = file
            R2_file = R1_file.replace("_R1_", "_R2_")
            if R2_file not in files:
                print("ERROR: Could not locate R2 file for this file:\n{}".format(R1_file))
            new_lab = lib_mapping[run_num][lib_ind]
            if new_lab not in concat_lists:
                concat_lists[new_lab] = {"R1":[],"R2":[]}
            concat_lists[new_lab]["R1"].append(R1_file)
            concat_lists[new_lab]["R2"].append(R2_file)
    for library in concat_lists:
        print("Combining {} read files into one for library {}".format(len(concat_lists[library]["R1"]), library))
        R1_command = ["cat"] + \
                    [basedir + "/" + i for i in concat_lists[library]["R1"]] + \
                    [">", "{}/{}_R1.fastq.gz".format(outdir, library)]
        R2_command = ["cat"] + \
                    [basedir + "/" + i for i in concat_lists[library]["R2"]] + \
                    [">", "{}/{}_R2.fastq.gz".format(outdir, library)]
        process = subprocess.Popen(" ".join(R1_command), shell=True)       #Not the best practice to use shell, but I was having some trouble with Popen stdout redirects... simplest solution for now
        processes.append(process)
        process = subprocess.Popen(" ".join(R2_command), shell=True)
        processes.append(process)
    for process in processes:
        process.wait()
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', help='Base input directory')
    parser.add_argument('--map_file', default="Lane_Lib_Mapping.txt", help='name of the index mapping file within each subdirectory. Default is Lane_Lib_Mapping.txt')
    parser.add_argument('--out', help='output directory')
    x = parser.parse_args()
    
    
    main(x.base_dir, x.map_file, x.out)



