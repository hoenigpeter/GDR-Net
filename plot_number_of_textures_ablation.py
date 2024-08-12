import matplotlib.pyplot as plt
import numpy as np
import scienceplots
plt.style.use('science')

# Data
texture_counts = [1, 3, 5, 10, 20, 50, 100, 200, 500, 1226]
yolox_map = [0.3610, 0.5430, 0.7480, 0.7560, 0.7690, 0.7840, 0.7940, 0.7830, 0.7900, 0.7970]

# Linear scale plot
plt.figure(figsize=(4, 3))

plt.plot(texture_counts, yolox_map, marker='o', linestyle='-')
plt.xscale('log')
plt.xlabel('Number of Textures', fontsize=14)
plt.ylabel('mAP', fontsize=14)
plt.title('YOLOx', fontsize=16)
#plt.grid(True, which="both", ls="--")

# Custom ticks to match data points
plt.xticks(texture_counts, labels=texture_counts, rotation=0)
plt.tight_layout()
#plt.show()

# Show the plot
plt.grid(False)
plt.savefig('ablation_texture_count.jpg', dpi=300, bbox_inches='tight')