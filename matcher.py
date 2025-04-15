import cv2

def compute_keypoints_and_descriptors(image):                   # Extracts SIFT keypoints and descriptors from an image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)              # Convert image to grayscale for SIFT
    sift = cv2.SIFT_create()                                    # Create a SIFT detector object
    keypoints, descriptors = sift.detectAndCompute(gray, None)  # Detect keypoints and compute descriptors
    return keypoints, descriptors                               # Return both keypoints and their descriptors

def compare_fingerprints(img1, img2):                           # Compares two fingerprint images using SIFT and FLANN matcher
    kp1, des1 = compute_keypoints_and_descriptors(img1)         # Get keypoints and descriptors for image 1
    kp2, des2 = compute_keypoints_and_descriptors(img2)         # Get keypoints and descriptors for image 2

    if des1 is None or des2 is None:        # If descriptors could not be computed (e.g., blank image)
        return float('inf')                 # Return a high distance score (infinite)

    index_params = dict(algorithm=1, trees=5)                   # FLANN index parameters for KD-Tree
    search_params = dict(checks=50)                             # FLANN search params: number of times the tree(s) are recursively traversed
    flann = cv2.FlannBasedMatcher(index_params, search_params)  # Create the FLANN matcher object
    matches = flann.knnMatch(des1, des2, k=2)                   # Find the 2 nearest matches for each descriptor

    good_matches = []                               # Store matches that pass Lowe's ratio test
    for m, n in matches:                            # Loop through each pair of matches
        if m.distance < 0.7 * n.distance:           # Apply Lowe's ratio test
            good_matches.append(m)                  # Keep only good matches

    if not good_matches:                            # If no good matches are found
        return float('inf')                         # Return infinite score (no similarity)

    score = 1 / len(good_matches)                   # Inverse of number of good matches (lower score = better match)
    return score                                    # Return the match score
