import torch
from monotonic_align import maximum_path

similarity = torch.randn(1, 137, 800).abs()
mask = torch.ones(1, 137, 800)
alignments = maximum_path(similarity, mask)

print(alignments)