def small_molecule_drugbank():
    import os

    import pandas

    return pandas.read_csv(os.path.join(os.path.dirname(__file__), "small_molecule_drugbank.csv"))
