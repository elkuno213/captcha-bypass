import cv2


def find_bounding_box(image, bounding_box_lower_thresholds, bounding_box_upper_thresholds):
    rect_coordinates = []
    
    width_lower_threshold, height_lower_threshold = bounding_box_lower_thresholds
    width_upper_threshold, height_upper_threshold = bounding_box_upper_thresholds
    
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if height_upper_threshold >= h > height_lower_threshold \
            and width_upper_threshold >= w > width_lower_threshold:
            rect_coordinates.append((x, y, w, h))
        else:
            continue

    return rect_coordinates


def segment_pictures(image, rect_coordinates, dimension_resized, offset=2):
    segmented_pictures = []

    for rec_coordinate in rect_coordinates:
        (x, y, w, h) = rec_coordinate
        cropped_image = image[max(0,y-offset):y+h+offset, max(0,x-offset):x+w+offset]
        segmented_pictures.append(cv2.resize(cropped_image, dimension_resized))
    
    return segmented_pictures