import cv2
import numpy as np
import imutils
import posenet.constants
import posenet.computeangle


def valid_resolution(width, height, output_stride=16):
    target_width = (int(width) // output_stride) * output_stride + 1
    target_height = (int(height) // output_stride) * output_stride + 1
    return target_width, target_height


def _process_input(source_img, scale_factor=1.0, output_stride=16):
    # print('source_img:')
    # print(source_img.shape)
    target_width, target_height = valid_resolution(
        source_img.shape[1] * scale_factor, source_img.shape[0] * scale_factor, output_stride=output_stride)
    scale = np.array([
        source_img.shape[0] / target_height,
        source_img.shape[1] / target_width])

    input_img = cv2.resize(
        source_img, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB).astype(np.float32)
    input_img = input_img * (2.0 / 255.0) - 1.0
    input_img = input_img.reshape(1, target_height, target_width, 3)
    return input_img, source_img, scale


def read_img(img, scale_factor=1.0, output_stride=16):
    return _process_input(img, scale_factor, output_stride)


def read_cap(cap, rotate, scale_factor=1.0, output_stride=16):
    res, img = cap.read()

    if rotate:
        img = imutils.rotate_bound(img, -90)

    if not res:
        raise IOError("webcam failure")
    return _process_input(img, scale_factor, output_stride)


def read_imgfile(path, scale_factor=1.0, output_stride=16):
    img = cv2.imread(path)
    return _process_input(img, scale_factor, output_stride)


def draw_keypoints(
        img, instance_scores, keypoint_scores, keypoint_coords,
        min_pose_confidence=0.5, min_part_confidence=0.5):
    cv_keypoints = []
    for ii, score in enumerate(instance_scores):
        if score < min_pose_confidence:
            continue
        for ks, kc in zip(keypoint_scores[ii, :], keypoint_coords[ii, :, :]):
            if ks < min_part_confidence:
                continue
            cv_keypoints.append(cv2.KeyPoint(kc[1], kc[0], 10. * ks))
    out_img = cv2.drawKeypoints(img, cv_keypoints, outImage=np.array([]))
    return out_img


def get_adjacent_keypoints(keypoint_scores, keypoint_coords, min_confidence=0.1):
    results = []
    for left, right in posenet.CONNECTED_PART_INDICES:
        #    if keypoint_scores[left] < min_confidence or keypoint_scores[right] < min_confidence:
        #         continue
        results.append(
            np.array(
                [
                    keypoint_coords[left][::-1],
                    keypoint_coords[right][::-1]
                ]
            ).astype(np.int32),
        )
    return results


def get_skeleton(
        control, img, instance_scores, keypoint_scores, keypoint_coords,
        min_pose_confidence=0.5, min_part_confidence=0.5):
    adjacent_keypoints = []
    all_startpoint_angle = None
    for ii, score in enumerate(instance_scores):
        if score < min_pose_confidence:
            continue
        new_keypoints = get_adjacent_keypoints(
            keypoint_scores[ii, :], keypoint_coords[ii, :, :], min_part_confidence)

        adjacent_keypoints.extend(new_keypoints)

        all_startpoint_angle = posenet.computeangle.calculateangle_all_body(
            adjacent_keypoints)

        control.update_model(adjacent_keypoints, all_startpoint_angle)

        if control.is_body_in_box():
            img = cv2.polylines(img, adjacent_keypoints,
                                isClosed=False, color=(255, 255, 0), thickness=1)
        else:
            c = 0
            for ks, kc in zip(keypoint_scores[ii, :], keypoint_coords[ii, :, :]):
                if c > 4:
                    break
                c += 1
                if ks < min_part_confidence:
                    continue
                x = int(kc[1])
                y = int(kc[0])
                r = int(10 * ks) + 20
                img[y-r:y+r, x-r:x+r] = 255

    return img, adjacent_keypoints, all_startpoint_angle


def get_all_skeleton(
        instance_scores, keypoint_scores, keypoint_coords,
        min_pose_confidence=0.5, min_part_confidence=0.5):
    adjacent_keypoints = []

    for i, score in enumerate(instance_scores):
        if score < min_pose_confidence:
            continue
        new_keypoints = get_adjacent_keypoints(
            keypoint_scores[i, :], keypoint_coords[i, :, :], min_part_confidence)

        face_points = []
        for ks, kc in zip(keypoint_scores[i, :5], keypoint_coords[i, :5, :5]):
            if ks < min_part_confidence:
                continue
            x = kc[1]
            y = kc[0]
            confidence = ks
            face_points.append([x, y, confidence])
        adjacent_keypoints.append([new_keypoints, face_points])

    return adjacent_keypoints


def draw_skel_and_kp(
        img, instance_scores, keypoint_scores, keypoint_coords,
        min_pose_score=0.5, min_part_score=0.5):
    out_img = img
    adjacent_keypoints = []
    cv_keypoints = []
    for ii, score in enumerate(instance_scores):
        if score < min_pose_score:
            continue
        # if ii == 0:
        new_keypoints = get_adjacent_keypoints(
            keypoint_scores[ii, :], keypoint_coords[ii, :, :], min_part_score)
        adjacent_keypoints.extend(new_keypoints)

        for ks, kc in zip(keypoint_scores[ii, :], keypoint_coords[ii, :, :]):
            if ks < min_part_score:
                continue
            print(kc[1], kc[0], 10. * ks)
            cv_keypoints.append(cv2.KeyPoint(kc[1], kc[0], 10. * ks))

        """
        new_keypoints = get_adjacent_keypoints(
            keypoint_scores[ii, :], keypoint_coords[ii, :, :], min_part_score)
        adjacent_keypoints.extend(new_keypoints)

        for ks, kc in zip(keypoint_scores[ii, :], keypoint_coords[ii, :, :]):
            if ks < min_part_score:
                continue
            cv_keypoints.append(cv2.KeyPoint(kc[1], kc[0], 10. * ks))
        """

    print(cv_keypoints)
    out_img = cv2.drawKeypoints(
        out_img, cv_keypoints, outImage=np.array([]), color=(255, 255, 0),
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    out_img = cv2.polylines(out_img, adjacent_keypoints,
                            isClosed=False, color=(255, 255, 0), thickness=1)

    if len(adjacent_keypoints) == 12:
        upper_startpoint_angle = posenet.computeangle.calculateangle_upper_body(
            adjacent_keypoints)
        down_startpoint_angle = posenet.computeangle.calculateangle_down_body(
            adjacent_keypoints)
        # for i in range(4):
        #     out_img = cv2.putText(out_img, str(upper_startpoint_angle[i][1]), tuple(
        #         upper_startpoint_angle[i][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (84, 46, 8), 1, cv2.LINE_AA)
        #     out_img = cv2.putText(out_img, str(down_startpoint_angle[i][1]), tuple(
        #         down_startpoint_angle[i][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (84, 46, 8), 1, cv2.LINE_AA)
    else:
        upper_startpoint_angle = np.zeros(2)
        down_startpoint_angle = np.zeros(2)
    return out_img, adjacent_keypoints, upper_startpoint_angle, down_startpoint_angle
