# -*- coding: utf-8 -*-
import numpy as np
import mrcfile

# Load gain reference
with mrcfile.open('gain_ref.mrc', permissive=True) as mrc:
    gain = mrc.data.copy()

# Find hot pixels (outliers beyond N standard deviations)
mean = np.mean(gain)
std = np.std(gain)
threshold = 5  # adjust as needed

hot_pixels = np.abs(gain - mean) > threshold * std
print(f"Found {np.sum(hot_pixels)} hot pixels")

# Replace hot pixels with local median (3x3 neighbourhood)
from scipy.ndimage import median_filter
gain_filtered = median_filter(gain, size=3)
gain_fixed = gain.copy()
gain_fixed[hot_pixels] = gain_filtered[hot_pixels]

# Save corrected gain reference
with mrcfile.new('gain_ref_fixed.mrc', overwrite=True) as mrc:
    mrc.set_data(gain_fixed)

print("Done!")
