import cv2
from scipy import ndimage
import numpy as np

# Rotate the icon by d degree each time and calculate the similarity between icon and target
def calculate_max_matching(target, icon, delta_degree):
    largest_val = 0
    for degree in range(0, 360, delta_degree):
        tmp = ndimage.rotate(target, degree, reshape=False)
        res = cv2.matchTemplate(icon,tmp,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > largest_val:
            largest_val = max_val
    return largest_val


def match_icons_with_targets(icons, targets):
    
    """
    icon\target | t1 | t2 | t3 |
    ------------|----|----|----|
    i1          |s11 |s12 |s13 |
    i2          |s21 |s22 |s23 |
    i3          |s31 |s32 |s33 |
    """

    # Calculate similarity matrix for each target, icon pair
    similarity_matrix = []
    delta_degree = 6
    for icon in icons:
        similarity_per_target = []
        for target in targets:
            similarity_per_target.append(calculate_max_matching(target, icon, delta_degree))
        similarity_matrix.append(similarity_per_target)
    print(f'icons-targets similarity matrix: {similarity_matrix}')

    # Calculate Mapping
    mapping = {}
    target_candidates = [False for _ in range(len(targets))]
    icon_candidates = [False for _ in range(len(icons))]
    # Sort the flatted similarity matrix in descending order, and assign the pair between target and icon if both of them
    # havem't been assigned.
    arr = np.array(similarity_matrix).flatten()
    arg_sorted = np.argsort(-arr)

    for idx in arg_sorted:
        icon_id = idx // len(targets)
        target_id = idx % len(targets)
        if target_candidates[target_id] == False and icon_candidates[icon_id] == False:
            target_candidates[target_id], icon_candidates[icon_id] = True, True
            mapping[target_id] = icon_id

    # for e in arg_sorted:
    #     col = e //len(icons)
    #     row = e % len(icons)
        
    #     if target_candidates[col] == False and icon_candidates[row] == False:
    #         target_candidates[col], icon_candidates[row] = True, True
    #         mapping[col] = row

    return mapping