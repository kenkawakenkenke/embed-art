#!/bin/sh

project="aerial"
ffmpeg -framerate 4 -i $project/out%d.jpg -c:v libx264 -pix_fmt yuv420p out_$project.mp4
