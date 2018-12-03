import os

file_path = 'id_title_map'

indices_count = 1
part_indices = []
store_indices = []

# path = './part_indices_files/'

# to take out the first entry
def make_index_entry(count, block_no, level, part_indices, indices_factor):
    file_name_original = 'title'+level+block_no + str(count/indices_factor)+'.txt'
    file_name = os.path.join(os.getcwd(), file_name_original)
    part_indices_file = open(file_name, 'w')
    for indices in part_indices:
        part_indices_file.write(indices)
    part_indices_file.close()

    start = part_indices[0].split()[0]+ ' ' + level + block_no + str(count/indices_factor) + ' InternalNode\n'
    return start

with open(file_path,'r') as indexed_file:
    indices_factor = 500
    for indices in indexed_file:
        if(indices_count % indices_factor == 0):
            fi = make_index_entry(indices_count,'','',part_indices,indices_factor)
            store_indices.append(fi)
            part_indices = []

        part_indices.append(indices)
        indices_count += 1

if len(part_indices) != 0:
    fi = make_index_entry(indices_count+500, '','', part_indices, indices_factor)
    store_indices.append(fi)
    part_indices = []

level = 0

while len(store_indices) > 200:
    indices_factor = 200
    next_level_indices = []
    part_indices = []
    indices_count = 1

    for indices in store_indices:
        if indices_count%indices_factor ==0:
            next_level_indices.append(make_index_entry(indices_count, 'block_no','level'+str(level), part_indices, indices_factor))
            part_indices = []
        part_indices.append(indices)
        indices_count +=1

    if len(part_indices) != 0:
        next_level_indices.append(make_index_entry(indices_count+200,'block_no','level'+str(level),part_indices, indices_factor))

    level += 1

    store_indices = next_level_indices

final_index = open('highest_level_index_file_title', 'w')

for i in store_indices:
    final_index.write(i)