import posenet


class ThirdParty(object):
    def __init__(self):
        self.sess = None
        self.model_cfg = None
        self.model_outputs = None

    def load_model(self, model_id, sess):
        self.sess = sess
        self.model_cfg, self.model_outputs = posenet.load_model(model_id, sess)

    def predict(self, img, args):
        output_stride = self.model_cfg['output_stride']
        input_image, display_image, output_scale = posenet.read_img(
            img,
            scale_factor=args.scale_factor,
            output_stride=output_stride)
        heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = self.sess.run(
            self.model_outputs,
            feed_dict={'image:0': input_image})
        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
            heatmaps_result.squeeze(axis=0),
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride=output_stride,
            max_pose_detections=10,
            min_pose_score=0.15)
        keypoint_coords *= output_scale
        return display_image, pose_scores, keypoint_scores, keypoint_coords

    def get_multi_skeleton(self, img, args):
        img, pose_scores, keypoint_scores, keypoint_coords = self.predict(
            img, args)
        return posenet.get_all_skeleton(
            img, pose_scores, keypoint_scores, keypoint_coords,
            min_pose_confidence=0.4, min_part_confidence=0.4,
        )
