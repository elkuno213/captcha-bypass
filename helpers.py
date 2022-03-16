import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_bounding_box(pane, rect_coordinates):
    # Show bounding boxes

    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(pane, cmap="gray")

    # Create a Rectangle patch
    for e in rect_coordinates:
        (x, y, w, h) = e
        rect = patches.Rectangle((x,y),w,h,linewidth=1,edgecolor='r',facecolor='none')
        ax.add_patch(rect)

    plt.show()
