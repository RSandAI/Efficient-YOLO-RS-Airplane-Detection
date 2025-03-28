# -*- coding: utf-8 -*-
"""HRPlanes_ORD.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TBVqVZxy7cE-Bxv6aK6-dkmUs7rzcboZ

<h1 align=center><b>Chicago O'Hare International Airport (ORD)</b></font></h1>

<br>

<p align="center">
    <img src="https://upgradedpoints.com/wp-content/uploads/2019/07/Chicago-O-Hare-International-Airport-Tower.jpeg" height=500 width=1000 alt="Istanbul Airport">
</p>

<small>Picture Source: <a href="https://upgradedpoints.com/">Upgraded Points</a></small>

<br>

## **Statistical Overview of Chicago O'Hare International Airport**

Chicago O'Hare International Airport (ORD) is one of the busiest airports in the United States, consistently ranking among the top in passenger traffic. In the most recent statistics, O'Hare is positioned as a vital hub for both domestic and international travel, contributing significantly to the aviation landscape.

<br>

Key Statistics:

- **Total Passengers:** Approximately 83 million annually, making it one of the leading airports in passenger volume.
- **IATA/ICAO Codes:** ORD/KORD
- **Location:** Chicago, Illinois, USA
- **Rank Among U.S. Airports:** O'Hare is often ranked within the top three airports for total passenger numbers in the United States, alongside Atlanta Hartsfield-Jackson and Los Angeles International Airport.
- **Growth Trends:** O'Hare has experienced consistent year-over-year growth, with a recent percentage increase in passenger numbers reflecting the airport's resilience and capacity for expansion. In comparison, the airport has seen a growth rate similar to major international airports, with an average annual increase of around 5-6%.

Make sure your runtime is **GPU** (_not_ CPU or TPU). And if it is an option, make sure you are using _Python 3_. You can select these settings by going to `Runtime -> Change runtime type -> Select the above mentioned settings and then press SAVE`.

## **0. Initial Steps**

### **0.1. Import and Download Libraries**
"""

# from google.colab import drive
# drive.mount('/gdrive')

!pip install rasterio -q

import os
import rasterio
from rasterio.windows import Window

"""## **1. Pre-process Image**"""

class ImageCropper:
    @classmethod
    def crop_and_save_multiple_images(cls, image_path, output_dir, level):
        img_width, img_height = 8000, 8000

        level_dir = os.path.join(output_dir, f"Level{level}")
        os.makedirs(level_dir, exist_ok=True)

        if level == 2:
            x_length, y_length = img_width // 2, img_height // 2
            row_min, row_max, col_min, col_max = 0, img_height, 0, img_width
        elif level == 3:
            x_length, y_length = img_width // 4, img_height // 4
            row_min, row_max, col_min, col_max = 0, img_height, 0, img_width
        else:
            raise ValueError("Level must be either 2 or 3.")

        image_id = 1
        with rasterio.open(image_path) as src:
            for r in range(row_min, row_max, y_length):
                for c in range(col_min, col_max, x_length):
                    window = Window(c, r, x_length, y_length)
                    transform = src.window_transform(window)
                    profile = src.profile.copy()
                    profile.update({
                        "height": window.height,
                        "width": window.width,
                        "transform": transform
                    })
                    cropped_img = src.read(window=window)
                    output_path = os.path.join(level_dir, f"image_patch_{image_id}.tif")
                    with rasterio.open(output_path, "w", **profile) as dst:
                        dst.write(cropped_img)
                    print(f'image_patch_{image_id} cropped and saved as {output_path}!')
                    image_id += 1

ImageCropper.crop_and_save_multiple_images('/content/ORD.tif', '/content/', level=2)

ImageCropper.crop_and_save_multiple_images('/content/ORD.tif', '/content/', level=3)

!zip -r /content/Level2.zip /content/Level2
!zip -r /content/Level3.zip /content/Level3

# from google.colab import files
# files.download("/content/Level2.zip")
# files.download("/content/Level3.zip")