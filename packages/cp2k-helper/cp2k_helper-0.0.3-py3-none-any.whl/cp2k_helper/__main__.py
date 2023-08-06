import sys
import pandas as pd
from cp2k_helper.cp2k_helper import output_parser,Summ

def main():
    
    args = sys.argv[1:]

    if args[0]=='--restart':
        print('CREATING RESTART')
        parser_ = output_parser(base_file_path='.',depth=1)
        parser_.restart_job()
    if args[0] =="--summ":
        print(f"CREATING SUMMARY")
        Summ(args[1])
    if args[0]=='--energy':
        parser_ = output_parser(base_file_path=args[1])
        energies = parser_.get_energies(all=False) # Getting the energy values in a dictionary
        Ha_to_eV = 27.2114
        # Running through the dictionary and putting it in a form we can made a dataframe from and save as a csv
        energy_dict = {'Folder_Name':[],'Type':[],'Energy (eV)':[]}
        for run_type in list(energies.keys()):
            for folder_name in list(energies[run_type].keys()):
                energy_dict['Type'].append(run_type)
                energy_dict['Folder_Name'].append(folder_name)
                energy_dict['Energy (eV)'].append(energies[run_type][folder_name]*Ha_to_eV)
        df = pd.DataFrame(energy_dict)
        try:
            df.to_csv(str(args[2])+'.csv')
        except: # Energy csv file name not specified
            df.to_csv('Energies.csv')

if __name__ == '__main__':
    main()