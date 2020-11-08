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