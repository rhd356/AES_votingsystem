import cv2

def compute_keypoints_and_descriptors(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    return keypoints, descriptors

def compare_fingerprints(img1, img2):
    kp1, des1 = compute_keypoints_and_descriptors(img1)
    kp2, des2 = compute_keypoints_and_descriptors(img2)

    if des1 is None or des2 is None:
        return float('inf')

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    if not good_matches:
        return float('inf')

    score = 1 / len(good_matches)
    return score