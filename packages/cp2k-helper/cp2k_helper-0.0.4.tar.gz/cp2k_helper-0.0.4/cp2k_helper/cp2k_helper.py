import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO   # StringIO behaves like a file object
import os
from collections import defaultdict
import argparse 
from shutil import copy2
import datetime 
import getpass
from pathlib import Path
# HELPER FUNCTIONS

def search_util(root='.',depth=np.inf,parse_by = None):
    """
        Recursively find all files in a directory.
        Parameters
        ---------
        root : str
            The root directory to search from.
        depth : int
            The depth to search to. Default is infinite.
        parse_by : str
            The string to parse the files by. Default is None.
        Returns
        -------
        files : list
            A list of files found.
    """

    files = []
    root = os.path.abspath(os.path.expanduser(os.path.expandvars(root)))
    if parse_by: 
        for r, d, f in os.walk(root):
            try:
                if 'RESTART' in '\t'.join(d):
                    continue
            except:
                restart = False
            if r[len(root):].count(os.sep) < depth:
                for file in f:
                    if parse_by in file:
                        files += [os.path.join(r, file)]
    else:
        for r, d, f in os.walk(root):
            if r[len(root):].count(os.sep) < depth:
                for file in f:
                    files += [os.path.join(r, file)]
    return files

def checkIfDuplicates(listOfElems):
    """
        Check if given list contains any duplicates

        Parameters
        ---------
        listofElems : list
             List of elements to be checked for duplicates
    """
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

class output_parser:
    "This class is used to parse the output files from CP2K"
    def __init__(self,base_file_path='.',depth=np.inf):
        self.base_file_path=base_file_path
        # We should add init statements to find a list of all of the important files
        self.opt_files = search_util(base_file_path,parse_by='OPT.out',depth=depth) # OPT.out files
        parent_dirs = []
        for file in self.opt_files:
            parent_dir = os.path.split(os.path.split(os.path.realpath(file))[0])[1]
            parent_dirs.append(parent_dir)
        assert not checkIfDuplicates(parent_dirs), "There are duplicate directory names in your given base path"
        self.parent_dirs = parent_dirs # List of all parent directories
        self.input_files = search_util(base_file_path,parse_by='.inp',depth=depth) # .inp files
        self.run_types = get_run_types(self.input_files) # Dictionary of run types
        self.all_energies = {'ENERGY':defaultdict(),'GEO_OPT':defaultdict()} # Dictionary of energies


    def get_run_types(self,input_files: list) -> dict:
        """
        This function parses the .inp files under the given directory and outputs the run type

        Parameters
        ---------
        input_files : list
             List of .inp files to be parsed

        Returns
        -------
        dict
            Dictionary of run types
        
        """

        run_types = defaultdict(str)
        for file in input_files:
            inp_file = file
            with open(inp_file,'r') as g:
                inp_file1 = g.read()
            inp = np.genfromtxt(StringIO(inp_file1),delimiter='\t',dtype='str',skip_header=1)
            line = np.flatnonzero(np.char.find(inp,'RUN_TYPE')!=-1)
            assert len(line) == 1 # There seems to be more than one line in the input file for "RUN_TYPE"
            # parent_dir = os.path.split(os.path.split(os.path.realpath(file))[0])[1]

            path = Path(str(file))
            parent_dir = path.parent.absolute()

            run_types[parent_dir] = inp[line][0].strip().split()[1]

        return run_types


    def get_energies(self,all=True):
        """
        This function parses the OPT.out files under the given directory and outputs the energy values

        Parameters
        ---------
        all : bool
             If True - Output all energy values| If False - Output final energy value. Defaults to True.
        
        Returns
        -------

        energies : dict
                Dictionary of energy values from each directory
        """
        
        # TODO add functionality to choose between getting single point and GEO_OPT energies
        run_types = self.run_types
        
        if all:
            for file in self.opt_files:
                Out_File = file
                with open(Out_File,'r') as g:
                    Out_File1 = g.read()
                out = np.genfromtxt(StringIO(Out_File1),delimiter='\t',dtype='str',skip_header=1)
                lines = np.flatnonzero(np.char.find(out,'ENERGY| Total FORCE_EVAL ( QS ) energy (a.u.):')!=-1)
                #parent_dir = os.path.split(os.path.split(os.path.realpath(file))[0])[1]
                path = Path(str(file))
                parent_dir = path.parent.absolute()
                if run_types[parent_dir]=='GEO_OPT':
                    self.all_energies['GEO_OPT'][parent_dir] = []
                for line in lines:
                    if run_types[parent_dir]=='ENERGY':
                        self.all_energies[run_types[parent_dir]][parent_dir] = float(out[line].split()[-1])
                    elif run_types[parent_dir]=='GEO_OPT':
                        self.all_energies[run_types[parent_dir]][parent_dir].append(float(out[line].split()[-1]))
            Energy = self.all_energies
        else:
            for file in self.opt_files:
                Out_File = file
                with open(Out_File,'r') as g:
                    Out_File1 = g.read()
                out = np.genfromtxt(StringIO(Out_File1),delimiter='\t',dtype='str',skip_header=1)
                lines = np.flatnonzero(np.char.find(out,'ENERGY| Total FORCE_EVAL ( QS ) energy (a.u.):')!=-1)
                #parent_dir = os.path.split(os.path.split(os.path.realpath(file))[0])[1]
                path = Path(str(file))
                parent_dir = path.parent.absolute()
                self.all_energies[run_types[parent_dir]][parent_dir] = float(out[lines[-1]].split()[-1])
            Energy = self.all_energies

        return Energy
    


    def restart_job(self):
        """
        This function sets up a restart folder for the job that did not converge
        """

        input_file = search_util(self.base_file_path,parse_by='.inp',depth=1)
        assert len(input_file)==1, f"There are more than one input file found in the directory\nInput files found: {input_file}"
        input_file = input_file[0]
        restart_files = search_util(self.base_file_path,parse_by='.restart',depth=1)
        restart_wfn_files = search_util(self.base_file_path,parse_by='.wfn',depth=1)
        restart_file = []
        restart_wfn = []
        for f in restart_files:
            if f.endswith('.restart'):
                restart_file.append(f)
        for f in restart_wfn_files:
            if f.endswith('.wfn'):
                restart_wfn.append(f)
        assert len(restart_file)==1, f"There are more than one restart file found in the directory\nRestart files found: {restart_file}"
        assert len(restart_wfn)==1, f"There are more than one restart file found in the directory\nRestart files found: {restart_wfn}"
        restart_file = restart_file[0]
        restart_wfn = restart_wfn[0]

        xyz_files = search_util(self.base_file_path,parse_by='.xyz',depth=1)
        xyz_files = [x for x in xyz_files if '-pos' not in x]
        xyz_file = min(xyz_files, key=len) # Assuming the original xyz file is the shortest one

        with open(input_file,'r') as g:
            input_f = g.read().split('\n')
        
        restart_input_file = ['&EXT_RESTART',f'RESTART_FILE_NAME {os.path.basename(restart_file)}','&END EXT_RESTART']
        for i,line in enumerate(input_f):
            if 'SCF_GUESS' in line:
                input_f[i] = input_f[i].replace('ATOMIC','RESTART')
        
        if '&EXT_RESTART' in input_f[0]:
            restart_input_file.extend(input_f[3:])
            RESTART_INPUT_FILE = '\n'.join(restart_input_file)
        else:
            restart_input_file.extend(input_f)
            RESTART_INPUT_FILE = '\n'.join(restart_input_file)
        
        slurm_file = search_util(self.base_file_path,parse_by='.slurm',depth=1)

        if len(slurm_file) > 1:
            print(f"WARNING MORE THAN ONE SLURM FILE\nUSING THE SHORTEST ONE\nSLURM FILES FOUND: {slurm_file}")

        slurm_file = min(slurm_file,key=len)

        ##### MAKING THE RESTART DIRECTORY AND ADDING THE FILES NEEDED
        struct_name = os.path.basename(xyz_file).split('.xyz')[0]
        folder_name = f'RESTART_{struct_name}'
        os.mkdir(folder_name)
        copy2(xyz_file,folder_name)
        copy2(os.path.basename(restart_wfn),folder_name)
        copy2(os.path.basename(slurm_file),folder_name)
        copy2(os.path.basename(restart_file),folder_name)
        f = open(os.path.join(folder_name,os.path.basename(input_file)),"w+")
        f.write(RESTART_INPUT_FILE)
        f.close()
    

def Summ(PATH):
    """ This function allows you to summarize the output files from a calculation by passing in the .out file
    
    Args:
        PATH (str): The path to the .out file
    """
    username = getpass.getuser()

    if os.path.isfile(PATH) and os.access(PATH, os.R_OK): # The path exists and the file is readable
        print(PATH)
        print()
        with open(PATH,'r') as g:
            Out_File = g.read()
        out = np.genfromtxt(StringIO(Out_File),delimiter='\t',dtype='str',skip_header=1)
        lines = np.flatnonzero(np.char.find(out,'Project name')!=-1)
        project_name = out[lines[0]].strip().split()[-1]
        print(f"Job name:\t{project_name}")
        print(f"Calc run by:\t{username}")
        lines_run_type =  np.flatnonzero(np.char.find(out,'Run type')!=-1)
        run_type = out[lines_run_type[0]].strip().split()[-1] # Assuming it is the first thing you put after RUN_TYPE
        print(f"CP2K run type:\t{run_type}")

        # Now let's get the runtime 
        lines =  np.flatnonzero(np.char.find(out,'CP2K')!=-1)
        time = out[lines[-1]].strip().split()[-1]
        if time.replace(".","").isnumeric():
            conversion = datetime.timedelta(seconds=round(float(time))) # Converting the seconds from OPT file to a time
            converted_time = str(conversion)
            print(f"Total runtime: {converted_time}")
        else:
            lines =  np.flatnonzero(np.char.find(out,'PROGRAM STARTED AT')!=-1)
            time = " ".join(out[lines[0]].strip().split()[-2:])
            date = datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S.%f")
            now = datetime.datetime.now()
            diff = now - date 
            print(f"Total runtime: JOB STILL RUNNING, Current time: {diff}")

        lines =  np.flatnonzero(np.char.find(out,'ENERGY')!=-1)
        print(f'Total Iterations: {len(lines)} iters')
        print()
        # Get the atom info
        lines =  np.flatnonzero(np.char.find(out,'Atomic kind:')!=-1)
        print("System Information:")
        for line in lines:
            print("\t"+out[line])
        print()
        print("Warning Information:")
        # Get the warnings
        lines =  np.flatnonzero(np.char.find(out,'WARNING')!=-1)
        #warns = [out[line] if out[line] not in warns for line in lines]
        warns = []
        for line in lines:
            if out[line] not in warns:
                warns.append(out[line])
        for i, warn in enumerate(warns):
            print(f'\t{i+1}: {warn}')

        print()
        final_lines = out[-9:]
        for line in final_lines:
            print(line)






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command Line Tools for CP2K')

    parser.add_argument('--restart',nargs='?', const='.')
    args = parser.parse_args()

    if args.restart:
        parser_ = output_parser(base_file_path='.',depth=1)
        parser_.restart_job()




