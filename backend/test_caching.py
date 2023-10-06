import os
import pandas as pd
import glob

mylist=[1,2,3,4]

def read_all_csv_files():
  
    csv_files = []
    for directory in os.listdir():
        print(directory)
        files = glob.glob(os.path.join('./3W/', "*.csv"))
    for file in files:
        csv_files.append(file)

    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True)
    final_df=list(final_df)
    return final_df

# folder_path = "./3W/0"
# for file_name in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, file_name)
#     if os.path.isfile(file_path):
#         data = pd.read_csv(file_path)
#         data_list = list(data['P-TPT'])

data_list=read_all_csv_files()
print(len(data_list))
# def getNext():
#     with open('./cache.txt','r+') as f:
#         counter=int(f.read())
#         end_counter=int(int(counter)+700)
#         data_updated=data_list[int(counter):int(end_counter)]
#         counter=int(int(counter)+700)
#         f.seek(0)
#         f.write(str(counter))
#         data_string = "  ".join(map(str, data_updated))
#         print(data_string)

# getNext()
# counter_file = 'counter.txt'

# def read_counter():
#     try:
#         with open(counter_file, 'r') as file:
#             return int(file.read().strip())
#     except FileNotFoundError:
#         return 0

# def write_counter(counter):
#     with open(counter_file, 'w') as file:
#         file.write(str(counter))


# folder_path = "./3W/0"

#     # Initialize the counter or load it from the file
# counter = read_counter()

#     # Get the next 700 data points based on the counter
# data_list = []
# for file_name in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, file_name)
#     if os.path.isfile(file_path):
#         data = pd.read_csv(file_path)
#         data_list.extend(list(data['P-TPT']))

#     # Slice the data to get the next 700 data points
# next_data_points = data_list[counter:counter+700]

#     # Update the counter for the next API call
# counter += 700

#     # Store the updated counter in the file
# write_counter(counter)

# print('data:',next_data_points)
