# Use same heights as OES (Folder SRTM6000)

The location from "srtm_45_13" includes the area to test "SS.json", with latitude 40 to 45 and longitude -5 to 0.

"AreaHATA.json" requires more files.

Conversion from TIF to BIL by: (already done, requires `gdal-bin`)

```
gdal_translate srtm_45_13.tif srtm_45_13.tif.bil
```

## Task

We need to rewrite "utils/sdf/usgs2sdf/srtm2sdf.cc" to convert correctly BIL to SDF:
- Our files have dimension 6000x6000, but only 3601x3601 and 1201x1201 are supported now, in the current conversion of `./srtm2sdf srtm_45_13.tif.bil` most of information are lost in the result.
- Know the coodinates correctly, these needs to be obtained from HDR files. The correct output file for "srtm_45_13.tif.bil" should be "40:45:355:0.sdf", but the output is always "0:1:0:1.sdf" for all the BIL files.

The usability of this new generated file at the main program also needs to be confirmed.

## A command prepared for SS.json

```
./signalserver -sdf ./dataSRTM -lat 40.402770 -lon -1.212317 -f 450 -txh 20 -dbm -m -o ss.png -R 0.25 -pm 6 -pe 3
```

## File formats

### .bil

6000x6000 integers of 2 bytes

### .hgt

1201x1201 integers of 2 bytes

### .sdf

4 lines of corner value, and lines of height values in digits.

```
x MAX
y MIN
x MIN
y MAX
height x0 y0
height x0 y1
...
height x0 y1199
height x1 y0
...
height x1199 y1199
```

# Use recomended height information of Cloud-RF (SRTM 1201)

I have not confirmed if the heights are the same.

A script to download the heights is written.
