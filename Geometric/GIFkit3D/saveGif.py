#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imageio

# == Settings ==
png_dir     = "output" # -------- Subdir for GIF
FPS         = 24 # -------------- Frame Per Second
outFileName = "icoshearyou.gif" # Name of the output file
# __ End Settings __

images = []

for subdir , dirs , files in os.walk( png_dir ):
    for file in files:
        file_path = os.path.join( subdir , file )
        if file_path.endswith(".png"):
            images.append( imageio.imread( file_path ) )
			
imageio.mimsave( os.path.join( png_dir , outFileName ) , images , fps = FPS )