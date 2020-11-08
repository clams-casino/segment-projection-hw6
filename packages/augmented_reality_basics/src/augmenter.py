import cv2 



class Augmenter:

    # initialize it with the relevant camera calibration matricies
    def __init__(self, camera_params):
        self.h = camera_params['image_height']
        self.w = camera_params['image_width']
        self.cam_mat = camera_params['camera_matrix']
        self.dist_coeff = camera_params['distortion_coefficients']
        self.H = camera_params['ground_homography']

        self.new_cam_mat, self.roi = cv2.getOptimalNewCameraMatrix(self.cam_mat,
                                                                    self.dist_coeff,
                                                                    (self.w, self.h), 1,
                                                                    (self.w, self.h))

    # Undistorts image
    def process_image(self, distorted_img):
        # undistort
        undistorted_img = cv2.undistort(distorted_img, self.cam_mat, self.dist_coeff, None, self.new_cam_mat)

        # crop the image
        # x,y,w,h = self.roi
        # undistorted_img = undistorted_img[y:y+h, x:x+w]

        return undistorted_img

    
    # Projects ground points to image points
    def ground2pixel(self):
        pass # TODO


    def render_segments(self):
        pass # TODO

    @staticmethod 
    def test():
        return 'hi'