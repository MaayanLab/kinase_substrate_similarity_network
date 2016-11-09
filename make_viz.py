def main():
  kinase_dict = load_kinase_info()

  make_viz(kinase_dict)



def make_viz(kinase_dict):
  '''
  Python 2.7
  The clustergrammer python module can be installed using pip:
  pip install clustergrammer

  or by getting the code from the repo:
  https://github.com/MaayanLab/clustergrammer-py
  '''

  from clustergrammer import Network
  from copy import deepcopy

  tmp_net = deepcopy(Network())
  net     = deepcopy(Network())

  # load matrix tsv file
  tmp_net.load_file('primary_data/kinase_network_based_on_substrates.txt')
  # print(tmp_net.dat['mat'].shape)

  tmp_df = tmp_net.dat_to_df()

  cols = tmp_df['mat'].columns.tolist()

  found = []
  found_tuples = []
  for inst_col in cols:

    if inst_col in kinase_dict:
      print('found: ' + inst_col)
      inst_name = 'kinase: '+ inst_col
      inst_type = 'type: ' + kinase_dict[inst_col]['type']
      inst_fam = 'family: ' + kinase_dict[inst_col]['fam']
      inst_tuple = (inst_name, inst_type, inst_fam)

      found.append(inst_col)
      found_tuples.append(inst_tuple)

  print('found ' + str(len(found)))

  # filter rows (as columns)
  tmp_df['mat'] = tmp_df['mat'][found]
  tmp_df['mat'] = tmp_df['mat'].transpose()
  tmp_df['mat'] = tmp_df['mat'][found]
  tmp_df['mat'] = tmp_df['mat'].transpose()

  print(found_tuples[0])
  tmp_df['mat'].columns = found_tuples
  tmp_df['mat'].index = found_tuples

  found  = list(set(found))
  print(len(found))

  net.df_to_dat(tmp_df)

  # optional filtering and normalization
  #########################################
  net.make_clust(dist_type='cos',views=[] , dendro=True,
                 sim_mat=False, filter_sim=0.1, calc_cat_pval=False)

  # write jsons for front-end visualizations
  net.write_json_to_file('viz', 'json/mult_view.json', 'no-indent')

def load_kinase_info():
  f = open('primary_data/Uniprot_kinases_processed.txt', 'r')
  lines = f.readlines()
  f.close()

  kinase_dict = {}

  for inst_line in lines:
    inst_line = inst_line.strip().split('\t')
    inst_kin = inst_line[0]
    inst_type = inst_line[1]
    inst_fam = inst_line[2]

    kinase_dict[inst_kin] = {}
    kinase_dict[inst_kin]['type'] = inst_type
    kinase_dict[inst_kin]['fam'] = inst_fam

  return kinase_dict

main()