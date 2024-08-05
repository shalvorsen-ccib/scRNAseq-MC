import argparse
import os
import subprocess


def read_mapping(infile):
    map_dict = {}
    with open(infile, 'r') as input:
        line = input.readline()
        line = input.readline()     #ignore header
        while line:     
            s_line = line.split()
            if s_line == []:        #empty line
                line = input.readline()
                continue
            map_dict[s_line[0]] = ",".join(s_line[1].split(";"))
            line = input.readline()
    return map_dict


def get_readfiles(f_list):
    f_map = {}
    for f in f_list:
        if f.endswith('fastq.gz'):
            if "_L00" in f:
                lane = "L" + f.split("_L00")[1][0]
                read = "R" + f.split("_R")[1][0]
                if lane not in f_map:
                    f_map[lane] = {}
                if read in f_map[lane]:
                    print("potentially duplicated read?\n{}".format(f))
                    exit()
                f_map[lane][read] = f
            else:
                print("I don't know how to identify this file...\n{}".format(f))
                exit()
    for lane in f_map:
        if len(f_map[lane]) != 4:
            print("There might be a mistake -- I could not identify all reads for some lanes. Current listing of lanes and files in the directory are:")
            print(f_map)
            print(f_list)
    return f_map



def main(basedir, subdirs, ind_map_file, outdir, script_file):
    processes = []
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not subdirs:
        subdirs = os.listdir(basedir)
    else:
        with open(subdirs, 'r') as input:
            subdirs = input.read().split()
    for subdir in subdirs:
        cur_root = "{}/{}".format(basedir, subdir)
        cur_files = os.listdir(cur_root)
        if ind_map_file not in cur_files:
            print("ERROR: Couldnt find the index mapping file in this directory:\n{}".format(cur_root))
            exit()
        ind_map = read_mapping("{}/{}".format(cur_root, ind_map_file))
        readfiles = get_readfiles(cur_files)
        for lane in readfiles:
            command = ["python3", script_file,
                        "--R1", "{}/{}".format(cur_root, readfiles[lane]["R1"]),
                        "--R2", "{}/{}".format(cur_root, readfiles[lane]["R2"]),
                        "--R3", "{}/{}".format(cur_root, readfiles[lane]["R3"]),
                        "--R4", "{}/{}".format(cur_root, readfiles[lane]["R4"]),
                        "--indices", ind_map[lane[1]],
                        "--R1_out", "{}/{}_{}_R1".format(outdir, subdir, lane),
                        "--R2_out", "{}/{}_{}_R2".format(outdir, subdir, lane)]
            process = subprocess.Popen(command)
            processes.append(process)
    for process in processes:
        process.wait()
    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', help='Base input directory')
    parser.add_argument('--subdirs', default=None, help='File listing subdirectories to operate on (within the base). Default operates on all subdirectories.')
    parser.add_argument('--ind_map_file', default="Lane_Lib_Mapping.txt", help='name of the index mapping file within each subdirectory. Default is Lane_Lib_Mapping.txt')
    parser.add_argument('--out', help='output directory')
    parser.add_argument('--script', default = "Parse_ReadFiles_WithIndex.py", help="location of the read parsing script. Default is Parse_ReadFiles_WithIndex.py")
    x = parser.parse_args()
    
    
    main(x.base, x.subdirs, x.ind_map_file, x.out, x.script)



