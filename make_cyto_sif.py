def main():
  from clustergrammer import Network
  from copy import deepcopy

  tmp_net = deepcopy(Network())
  net     = deepcopy(Network())

  # load matrix tsv file
  tmp_net.load_file('primary_data/kinase_network_based_on_substrates.txt')

  tmp_df = tmp_net.dat_to_df()
  df = tmp_df['mat']

  cols = df.columns.tolist()
  cols = cols[1:10]

  for row_index in range(len(cols)):
    for col_index in range(len(cols)):

      inst_source = cols[row_index]
      inst_target = cols[col_index]
      print( inst_source + ' ' + inst_target)


main()