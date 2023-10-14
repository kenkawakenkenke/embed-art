
base_resolutions = [
    (4,3),
    (16, 10),
    (16, 9),
    (3,2),
    (21,9),
    (1,1),
]
resolutions = [] + base_resolutions
for (width, height) in base_resolutions:
    resolutions += [(height, width)]

minWidth = 1
minHeight = 1
for (width, height) in resolutions:
    if width >= height:
        actualWidth = 1
        actualHeight = height / width
    else:
        actualHeight = 1
        actualWidth = width / height
    minWidth = min(minWidth, actualWidth)
    minHeight = min(minHeight, actualHeight)
    # print(width, height, actualWidth, actualHeight)

# The center 0.428 x 0.428 square is visible in every resolution, so the clock must be smaller that.
print(minWidth, minHeight)