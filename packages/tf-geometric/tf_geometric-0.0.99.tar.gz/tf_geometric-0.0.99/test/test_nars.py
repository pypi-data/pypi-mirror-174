import sys
sys.path.append("/home/hujun/mygit/tf_geometric")
import tf_geometric as tfg

g, target_node_type, (train_index, valid_index, test_index) = tfg.datasets.NARSACMDataset().load_data()
print(g)
print(target_node_type)
print(train_index, valid_index, test_index)
asdfasdf


def load_acm(device, args):
    g, labels, n_classes, train_nid, val_nid, test_nid = load_acm_raw()

    # my
    g = g.to(device)

    features = g.nodes["paper"].data["feat"]

    path = args.use_emb
    author_emb = torch.load(os.path.join(path, "author.pt")).float()
    field_emb = torch.load(os.path.join(path, "field.pt")).float()

    g.nodes["author"].data["feat"] = author_emb.to(device)
    g.nodes["field"].data["feat"] = field_emb.to(device)
    g.nodes["paper"].data["feat"] = features.to(device)
    paper_dim = g.nodes["paper"].data["feat"].shape[1]
    author_dim = g.nodes["author"].data["feat"].shape[1]
    assert(paper_dim >= author_dim)
    if paper_dim > author_dim:
        print(f"Randomly embedding features from dimension {author_dim} to {paper_dim}")
        author_feat = g.nodes["author"].data.pop("feat")
        field_feat = g.nodes["field"].data.pop("feat")
        rand_weight = torch.Tensor(author_dim, paper_dim).uniform_(-0.5, 0.5).to(device)
        g.nodes["author"].data["feat"] = torch.matmul(author_feat, rand_weight)
        g.nodes["field"].data["feat"] = torch.matmul(field_feat, rand_weight)

        # g.nodes["author"].data["feat"] = (torch.rand(g.nodes["author"].data["feat"].size()) - 0.5).to(device)

    # for ntype in g.ntypes:
    #     x = g.ndata["feat"][ntype]
    #     print(ntype, x.size(), x.mean())
    #     print(x[:2])
    #
    # asdfadsf

    labels = labels.to(device)
    train_nid, val_nid, test_nid = np.array(train_nid), np.array(val_nid), np.array(test_nid)

    return g, labels, n_classes, train_nid, val_nid, test_nid

