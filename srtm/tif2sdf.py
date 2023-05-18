import platform
import os

import rasterio

if platform.system() == "Linux":
    S = ':'
else:
    S = '_'


def format_neg_longitude(longitude):
    w_lon = -longitude
    if w_lon < 0:
        w_lon += 360
    return w_lon


NO_DATA_VALUE = -32768


def tif2sdf(tif_path):
    print("Reading", tif_path)
    tif_file = rasterio.open(tif_path)

    if tif_file.shape != (6000, 6000):
        raise ValueError("Shape {} not supported yet".format(tif_file.shape))

    tif_data = tif_file.read()[0]
    tif_left = int(tif_file.transform[2])
    tif_top = int(tif_file.transform[5])

    for i in range(5):
        for j in range(5):
            top = tif_top - i
            bottom = top - 1
            neg_left = format_neg_longitude(tif_left + j)
            neg_right = format_neg_longitude(tif_left + j + 1)
            sdf_path = f"{bottom}{S}{top}{S}{neg_right}{S}{neg_left}.sdf"

            print("Generating", sdf_path, end=" -> ")
            sdf_file = open(sdf_path, "w", encoding="ascii", newline="\n")

            # Corner: left, bottom, right, top
            sdf_file.write(str(neg_left) + "\n")
            sdf_file.write(str(bottom) + "\n")
            sdf_file.write(str(neg_right) + "\n")
            sdf_file.write(str(top) + "\n")

            valid_file = False

            # Get values, order reverted
            for line in reversed(tif_data[i * 1200: (i+1) * 1200]):
                for value in reversed(line[j * 1200: (j+1) * 1200]):
                    if value == NO_DATA_VALUE:
                        sdf_file.write("0\n")
                    else:
                        valid_file = True
                        sdf_file.write(str(value) + "\n")

            sdf_file.close()

            if valid_file:
                print("Complete")
            else:
                print("Empty content")
                os.remove(sdf_path)

    tif_file.close()
    print("Convertion of", tif_path, "complete")


if __name__ == "__main__":
    import sys
    for path in sys.argv[1: ]:
        tif2sdf(path)
