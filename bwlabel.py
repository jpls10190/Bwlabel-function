import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from scipy.ndimage import label, center_of_mass
import cv2
from skimage import measure
from screeninfo import get_monitors
import re

# Function description:
#
#   - Find every object in a binary image;
#   - Compute properties for each object: area, bounding box, centroid, orientation, eccentricity, perimeter, aspect ratio, solidity, extent
# 
#   - Interactive:  Shows every object individually and its correspondent properties in the terminal. 
#                   To go to the next object press "N". 
#                   To save the properties of a determined object, press 'S' 
#                   To exit, press 'Q'
#   
def show_labels_and_props(bin_img):
    # Label the objects
    labeled_image, num_labels = label(bin_img)

    # Get region properties using skimage.measure
    regions = measure.regionprops(labeled_image)

    # Initialize the index for displaying objects
    current_index = 0

    # Get the primary monitor (first monitor)
    monitor = get_monitors()[1]
    # Get the window size (height, width)
    window_height, window_width = bin_img.shape[:2]

    # Calculate the center of the screen
    center_x = monitor.width // 2
    center_y = monitor.height // 2

    # Calculate the top-left corner of the window
    top_left_x = center_x - (window_width // 2)
    top_left_y = center_y - (window_height // 2)

    # Open a file for saving the properties
    with open('properties.txt', 'w') as f:
        while True:
            if current_index >= num_labels:
                break  # Stop when there are no more objects to display
            
            # Create a mask for the current object
            object_mask = (labeled_image == current_index + 1).astype(np.uint8) * 255

            # Get the properties of the current object
            region = regions[current_index]
            
            # Area (size)
            area = region.area
            # Bounding box (min_row, min_col, max_row, max_col)
            min_row, min_col, max_row, max_col = region.bbox
            # Centroid (center of mass)
            centroid = region.centroid
            # Orientation (angle of the major axis)
            orientation = region.orientation
            # Eccentricity
            eccentricity = region.eccentricity
            # Perimeter (contour length)
            perimeter = region.perimeter
            # Aspect ratio (width / height of bounding box)
            aspect_ratio = region.bbox[3] / region.bbox[2]
            # Solidity (area of object / area of its convex hull)
            solidity = region.solidity
            # Extent (area / area of bounding box)
            extent = region.extent

            # Print properties for the current object
            print(f"Object {current_index + 1}:")
            print(f"  Area: {area}")
            print(f"  Bounding Box: {min_row, min_col, max_row, max_col}")
            print(f"  Centroid: {centroid}")
            print(f"  Orientation: {orientation}")
            print(f"  Eccentricity: {eccentricity}")
            print(f"  Perimeter: {perimeter}")
            print(f"  Aspect Ratio: {aspect_ratio}")
            print(f"  Solidity: {solidity}")
            print(f"  Extent: {extent}")
            print("-" * 40)
            
            # Save properties to the file if 's' is pressed
            properties = f"Object {current_index + 1}:\n"
            properties += f"  Area: {area}\n"
            properties += f"  Bounding Box: {min_row, min_col, max_row, max_col}\n"
            properties += f"  Centroid: {centroid}\n"
            properties += f"  Orientation: {orientation}\n"
            properties += f"  Eccentricity: {eccentricity}\n"
            properties += f"  Perimeter: {perimeter}\n"
            properties += f"  Aspect Ratio: {aspect_ratio}\n"
            properties += f"  Solidity: {solidity}\n"
            properties += f"  Extent: {extent}\n"
            properties += "-" * 40 + "\n"
                
            # Create a new image for the current object
            object_image = np.zeros_like(bin_img)
            object_image[object_mask == 255] = 255

            # Convert to BGR for visualization
            colored_image = cv2.cvtColor(object_image, cv2.COLOR_GRAY2BGR)

            # Draw the index on the image
            cv2.putText(colored_image, str(current_index + 1), (int(centroid[1]), int(centroid[0])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # Create a window for the object
            window_name = f"Object {current_index + 1}"
            # Create a window and move it to the center of the screen
            cv2.namedWindow(window_name)
            cv2.moveWindow(window_name, top_left_x, top_left_y)  # Adjust window size accordingly

            # Display the object with the index
            cv2.imshow(window_name, colored_image)

            # Wait for key press
            key = cv2.waitKey(0)  # Wait indefinitely until a key is pressed
            if key == ord('n'):  # If 'q' is pressed, go to the next object
                # Close all windows
                cv2.destroyAllWindows()
                current_index += 1
            elif key == ord('b'):  # If 'b' is pressed, go to the previous object
                cv2.destroyAllWindows()
                current_index = max(0, current_index - 1)  # Ensure it doesn't go below 0
            elif key == ord('s'):  # If 's' is pressed, save the current object's properties
                f.write(properties)
                print(f"Properties of Object {current_index + 1} saved to 'properties.txt'.")
            elif key == ord('q'):  # If '0' is pressed, exit the loop
                print("Exiting loop.")
                break
        # Close all windows
        cv2.destroyAllWindows()

def average_properties(txt_file="./properties.txt"):

    # Initialize variables to store the sums and counts of each property
    area_sum = 0
    eccentricity_sum = 0
    perimeter_sum = 0
    aspect_ratio_sum = 0
    solidity_sum = 0
    extent_sum = 0

    num_objects = 0  # Counter for the number of objects

    # Open the properties.txt file for reading
    with open(txt_file, 'r') as file:
        # Read the entire file
        content = file.read()
        
        # Split the content into object blocks
        object_blocks = content.split('-' * 40)  # Assuming each object is separated by 40 dashes

        for block in object_blocks:
            if block.strip():  # Avoid empty blocks
                num_objects += 1

                # Extract numerical values for each property using regular expressions
                area_match = re.search(r"Area: (\d+)", block)
                eccentricity_match = re.search(r"Eccentricity: (\d+\.\d+)", block)
                perimeter_match = re.search(r"Perimeter: (\d+)", block)
                aspect_ratio_match = re.search(r"Aspect Ratio: (\d+\.\d+)", block)
                solidity_match = re.search(r"Solidity: (\d+\.\d+)", block)
                extent_match = re.search(r"Extent: (\d+\.\d+)", block)

                if area_match:
                    area_sum += int(area_match.group(1))
                if eccentricity_match:
                    eccentricity_sum += float(eccentricity_match.group(1))
                if perimeter_match:
                    perimeter_sum += int(perimeter_match.group(1))
                if aspect_ratio_match:
                    aspect_ratio_sum += float(aspect_ratio_match.group(1))
                if solidity_match:
                    solidity_sum += float(solidity_match.group(1))
                if extent_match:
                    extent_sum += float(extent_match.group(1))

    # Calculate the averages
    if num_objects > 0:
        average_area = area_sum / num_objects
        average_eccentricity = eccentricity_sum / num_objects
        average_perimeter = perimeter_sum / num_objects
        average_aspect_ratio = aspect_ratio_sum / num_objects
        average_solidity = solidity_sum / num_objects
        average_extent = extent_sum / num_objects

        # Print the average values
        print(f"Average Area: {average_area}")
        print(f"Average Eccentricity: {average_eccentricity}")
        print(f"Average Perimeter: {average_perimeter}")
        print(f"Average Aspect Ratio: {average_aspect_ratio}")
        print(f"Average Solidity: {average_solidity}")
        print(f"Average Extent: {average_extent}")
    else:
        print("No objects found in the properties file.")