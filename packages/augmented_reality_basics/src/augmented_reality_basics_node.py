#!/usr/bin/env python3

import rospy
import rospkg
import cv2 as cv
import numpy as np
import yaml
from cv_bridge import CvBridge

from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage

from augmenter import Augmenter


def readYamlFile(fname):
    """
    Reads the YAML file in the path specified by 'fname'.
    E.G. :
        the calibration file is located in : `/data/config/calibrations/filename/DUCKIEBOT_NAME.yaml`
    """
    with open(fname, 'r') as in_file:
        try:
            yaml_dict = yaml.load(in_file)
            return yaml_dict
        except yaml.YAMLError as exc:
            self.log("YAML syntax error. File: %s fname. Exc: %s"
                     %(fname, exc), type='fatal')
            rospy.signal_shutdown()
            return



class AugmentedRealityBasicsNode(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(AugmentedRealityBasicsNode, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        # bridge between opencv and ros
        self.bridge = CvBridge()

        # get map params
        self.map_file = rospy.get_param('~map_file')
        self.map_file_basename = self.map_file.split('.')[0]

        # construct subscriber for images
        self.camera_sub = rospy.Subscriber('camera_node/image/compressed', CompressedImage, self.callback)
        # construct publisher for AR images
        self.pub = rospy.Publisher('~' + self.map_file_basename + '/image/compressed', CompressedImage, queue_size=10)

    

        # get camera calibration parameters (homography, camera matrix, distortion parameters)
        self.intrinsics_file = '/data/config/calibrations/camera_intrinsic/' + rospy.get_namespace().strip("/") + ".yaml"
        self.extrinsics_file = '/data/config/calibrations/camera_extrinsic/' + rospy.get_namespace().strip("/") + ".yaml"
        rospy.loginfo('Reading camera intrinsics from {}'.format(self.intrinsics_file))
        rospy.loginfo('Reading camera extrinsics from {}'.format(self.extrinsics_file))


        intrinsics = readYamlFile(self.intrinsics_file)
        extrinsics = readYamlFile(self.extrinsics_file)

        camera_params = {}
        camera_params['image_height'] = intrinsics['image_height']
        camera_params['image_width'] = intrinsics['image_width']
        camera_params['camera_matrix'] = np.array(intrinsics['camera_matrix']['data']).reshape(3,3)
        camera_params['distortion_coefficients'] = np.array(intrinsics['distortion_coefficients']['data'])
        camera_params['homography'] = np.array(extrinsics['homography']).reshape(3,3)


        # initialize augmenter with camera calibration parameters
        self.augmenter = Augmenter(camera_params)


         # read mapfile as a dictionary
        rospack = rospkg.RosPack()
        map_path= rospack.get_path('augmented_reality_basics') + '/maps/' + self.map_file
        rospy.loginfo('Reading map file from {}'.format(map_path))
        self.map_dict = readYamlFile(map_path)

        # make sure map is in the right coordinates
        for _, val in self.map_dict['points'].items():
            if val[0] == 'axle':
                val[0] = 'image_undistorted'
                val[-1] = self.augmenter.ground2pixel(val[-1])

                   

    def callback(self, data):
        raw_img = self.bridge.compressed_imgmsg_to_cv2(data, desired_encoding="passthrough")

        undistorted_img = self.augmenter.process_image(raw_img)
        ar_img = self.augmenter.render_segments(undistorted_img, self.map_dict)
        ar_img = self.augmenter.crop_to_roi(ar_img)

        msg = self.bridge.cv2_to_compressed_imgmsg(ar_img, dst_format='jpeg')
        self.pub.publish(msg)


if __name__ == '__main__':
    # create the node
    rospy.loginfo('Starting segment projection')
    node = AugmentedRealityBasicsNode(node_name='augmented_reality_basics_node')
    # keep spinning
    rospy.spin()