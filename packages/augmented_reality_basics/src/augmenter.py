import cv2
import numpy as np


def draw_segment(image, pt_x, pt_y, color):
    defined_colors = {
        'red': ['rgb', [1, 0, 0]],
        'green': ['rgb', [0, 1, 0]],
        'blue': ['rgb', [0, 0, 1]],
        'yellow': ['rgb', [1, 1, 0]],
        'magenta': ['rgb', [1, 0, 1]],
        'cyan': ['rgb', [0, 1, 1]],
        'white': ['rgb', [1, 1, 1]],
        'black': ['rgb', [0, 0, 0]]}
    _color_type, [r, g, b] = defined_colors[color]
    return cv2.line(image, (pt_x[0], pt_y[0]), (pt_x[1], pt_y[1]), (b * 255, g * 255, r * 255), 5)


class Augmenter:

    # initialize it with the relevant camera calibration matricies
    def __init__(self, camera_params):
        self.h = camera_params['image_height']
        self.w = camera_params['image_width']
        self.cam_mat = camera_params['camera_matrix']
        self.dist_coeff = camera_params['distortion_coefficients']
        self.H_ground2pixel = np.linalg.inv(camera_params['homography'])

        self.new_cam_mat, self.roi = cv2.getOptimalNewCameraMatrix(self.cam_mat,
                                                                   self.dist_coeff,
                                                                   (self.w,
                                                                    self.h), 0,
                                                                   (self.w, self.h))

    # Undistorts image
    def process_image(self, distorted_img):
        return cv2.undistort(distorted_img, self.cam_mat, self.dist_coeff, None, self.new_cam_mat)

    def crop_to_roi(self, img):
        x, y, w, h = self.roi
        return img[y:y+h, x:x+w]

    # Projects ground points to image points

    def ground2pixel(self, point_ground):
        # point_ground = [x y 0]
        point_ground[-1] = 1
        point_img = np.dot(self.H_ground2pixel, np.array(
            point_ground).reshape(3, 1)).squeeze()

        return [point_img[0]/point_img[2], point_img[1]/point_img[2]]

    def render_segments(self, original_img, map_dict):
        img = original_img.copy()
        for segment in map_dict['segments']:
            point_1 = map_dict['points'][segment['points'][0]][-1]
            point_2 = map_dict['points'][segment['points'][1]][-1]

            pt_x = (int(point_1[0]), int(point_2[0]))
            pt_y = (int(point_1[1]), int(point_2[1]))

            draw_segment(img, pt_x, pt_y, segment['color'])

        return img
