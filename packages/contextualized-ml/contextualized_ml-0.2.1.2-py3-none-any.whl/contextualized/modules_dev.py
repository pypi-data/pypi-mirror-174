import torch
import torch.nn as nn

from contextualized.functions import identity_link, identity
from contextualized.modules import SoftSelect


class NGAMOE(nn.Module):
    """
    NGAM with Mixture of Experts
    Each additive model includes a mixture of experts + gating function for the parameters of the final linear layer
    """

    def __init__(
        self,
        input_dim,
        output_dim,
        k,
        width,
        layers,
        activation=nn.ReLU,
        gating_fn=identity,
        link_fn=identity_link,
    ):
        super(NGAMOE, self).__init__()
        self.intput_dim = input_dim
        self.output_dim = output_dim
        hidden_layers = lambda: [
            layer
            for _ in range(0, layers - 1)
            for layer in (nn.Linear(width, width), activation())
        ]
        nam_layers = (
            lambda: [nn.Linear(1, width), activation()]
            + hidden_layers()
            + [nn.Linear(width, width), activation()]
        )
        expert_layers = (
            lambda: [nn.Linear(1, width), activation()]
            + hidden_layers()
            + [nn.Linear(width, k), activation()]
        )
        self.nams = nn.ModuleList(
            [nn.Sequential(*nam_layers()) for _ in range(input_dim)]
        )
        self.experts = nn.ModuleList(
            [nn.Sequential(*expert_layers()) for _ in range(input_dim)]
        )
        self.explainer = SoftSelect((k,), (output_dim, width))
        self.gating_fn = gating_fn
        self.link_fn = link_fn

    def forward(self, x):
        batch_size = x.shape[0]
        ret = torch.zeros((batch_size, self.output_dim))
        for i, (nam, expert) in enumerate(zip(self.nams, self.experts)):
            final_gating = self.gating_fn(expert(x[:, i].unsqueeze(-1)))
            final_linear = self.explainer(final_gating)
            final_hidden = nam(x[:, i].unsqueeze(-1))
            ret += torch.matmul(final_linear, final_hidden.unsqueeze(-1)).squeeze(-1)
        return self.link_fn(ret)


if __name__ == "__main__":
    n = 100
    x_dim = 10
    y_dim = 5
    k = 3
    width = 50
    layers = 5
    x = torch.rand((n, x_dim))

    ngamoe = NGAMOE(x_dim, y_dim, k, width, layers)
    ngamoe(x)
