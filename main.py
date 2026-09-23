import pandas as pd
import torch
import transformers

print("MoodleGuide environment is ready")
print("PyTorch version:", torch.__version__)
print("Transformers version:", transformers.__version__)
print("GPU available:", torch.cuda.is_available())