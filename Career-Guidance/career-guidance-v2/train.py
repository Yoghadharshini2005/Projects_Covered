"""
train.py - Shortcut to retrain the ML model
Usage: python train.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dataset'))
sys.path.insert(0, os.path.dirname(__file__))

# First generate/refresh dataset
exec(open('dataset/generate_dataset.py').read())

# Then train
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from backend.ml.train_model import train
acc = train()
print(f"\n✅ Model ready with {acc*100:.1f}% accuracy")
