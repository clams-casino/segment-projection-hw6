# Usage

Build it on the duckiebot. Assuming in the root directory of the repo
```
dts devel build -f -H <duckiebot name>.local
```

Then the following command to run it on the duckiebot
```
dts devel run -H <duckiebot name>.local
```

Publishes the images with the segments to the topic `/<duckiebot name>/augmented_reality_basics_node/<map name>/image/compressed'`

To run with a different map, edit `launchers/default.sh` and set the `map_file` argument of the roslaunch to the name of the map file. For example `calibration_pattern.yaml`

# Note to the TAs

For the undistortion, I used `cv2.getOptimalNewCameraMatrix()` with an alpha value of `0.0`. I chose this over using `1.0` because I got better results when overlaying the AR pattern on the image. I think it has something to do with how the undistortion was done during the camera calibration. I noticed that after recalibrating my camera for a later assignment (localization assignment) that using an alpha value of `1.0` was actually now better. Please keep this in mind.