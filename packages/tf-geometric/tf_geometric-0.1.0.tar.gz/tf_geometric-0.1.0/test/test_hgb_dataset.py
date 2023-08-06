import tf_geometric as tfg

# hetero_graph, train_mask_dict, test_mask_dict = HGBDataset("acm").load_data()
hetero_graph, train_mask_dict, test_mask_dict = tfg.datasets.HGBIMDBDataset().load_data()

print(hetero_graph)
print(hetero_graph.x_dict)