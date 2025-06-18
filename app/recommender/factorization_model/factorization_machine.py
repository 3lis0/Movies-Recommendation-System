from torch import nn
import torch

class FactorizationMachineModel(nn.Module):
    def __init__(self, num_users, num_movies, num_cont_features, emb_dim=64):
        super().__init__()

        # Embedding layers
        self.user_emb = nn.Embedding(num_users, emb_dim)
        self.movie_emb = nn.Embedding(num_movies, emb_dim)

        # Linear (first-order) terms for categorical
        self.user_bias = nn.Embedding(num_users, 1)
        self.movie_bias = nn.Embedding(num_movies, 1)

        # Linear for continuous
        self.linear_cont = nn.Linear(num_cont_features, 1)

        self.dropout = nn.Dropout(0.2)
        self.output = nn.Linear(1, 1)  # optional non-linearity head

    def forward(self, X_cat, X_cont):
        user_idx, movie_idx = X_cat[:, 0], X_cat[:, 1]

        user_vec = self.user_emb(user_idx)
        movie_vec = self.movie_emb(movie_idx)

        # ----- FM interaction (dot product of embeddings) -----
        interaction = torch.sum(user_vec * movie_vec, dim=1, keepdim=True)

        # ----- Linear terms -----
        linear_cat = self.user_bias(user_idx) + self.movie_bias(movie_idx)
        linear_cont = self.linear_cont(X_cont)

        # ----- Final output -----
        out = interaction + linear_cat + linear_cont
        out = self.output(self.dropout(out))

        return out.squeeze(1)
