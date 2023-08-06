MIN_SEQ_LEN = 3000
DEFAULT_PROB_CUTOFF = [0.65, 0.65]
SHORT2LONG = {
    "mit": "mitochondrion",
    "pla": "plastid",
    "bac": "bacteria",
    "arc": "archaea",
    "euk": "eukarya",
    "unk": "unknown",
    "pro": "prokarya",
}
FIRST_NNET_KMER2PARAMS = {
    4: dict(
        fname="first_nnet_kmer_4.pkl", k=4, hidden_1=2048, hidden_2=2048, dropout=0.2
    ),
    5: dict(
        fname="first_nnet_kmer_5.pkl", k=5, hidden_1=2048, hidden_2=2048, dropout=0.2
    ),
    6: dict(
        fname="first_nnet_kmer_6.pkl", k=6, hidden_1=2048, hidden_2=1024, dropout=0.2
    ),
}
SECOND_NNET_KMER2PARAMS = {
    4: dict(
        fname="second_nnet_kmer_4.pkl", k=4, hidden_1=256, hidden_2=128, dropout=0.2
    ),
    5: dict(
        fname="second_nnet_kmer_5.pkl", k=5, hidden_1=256, hidden_2=128, dropout=0.2
    ),
    6: dict(
        fname="second_nnet_kmer_6.pkl", k=6, hidden_1=256, hidden_2=128, dropout=0.5
    ),
    7: dict(
        fname="second_nnet_kmer_7.pkl", k=7, hidden_1=128, hidden_2=64, dropout=0.2
    ),
}
CLASSES = ["org", "bac", "arc", "euk", "unk1", "pla", "unk2", "mit"]
DESCRIPTION = """tiara - a deep-learning-based approach for identification of eukaryotic sequences 
in the metagenomic data powered by PyTorch.  

The sequences are classified in two stages:

- In the first stage, the sequences are classified to classes: 
      archaea, bacteria, prokarya, eukarya, organelle and unknown.
- In the second stage, the sequences labeled as organelle in the first stage 
      are classified to either mitochondria, plastid or unknown.
"""
