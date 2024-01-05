import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageDraw
import os, sys

class ImageClass:
    def select_image(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", ".png .jpg .jpeg .gif .bmp .PNG .JPG .JPEG .GIF .BMP")])
        if not file_path:
            print("No image selected. Exiting.")
            return
        return file_path
    
    def resize_image(self, file_path):
        if not file_path:
            print("No image selected. Exiting.")
            return
        
        # Prompt the user for the desired width
        new_width = int(input("Enter the desired image width: "))

        # Resize the image and save it with a new name
        output_path = f"resized_{new_width}_image.jpg"

        original_image = Image.open(file_path)

        # Calculate the new height while maintaining the aspect ratio
        aspect_ratio = original_image.width / original_image.height
        new_height = int(new_width / aspect_ratio)
        
        # Resize the image
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save the resized image
        resized_image.save(output_path)

        print(f"Image resized and saved to: {output_path}")
        return output_path

    def create_empty_image(self, output_path="empty_image.png"):
        # Prompt the user for the desired width
        width = int(input("Enter the desired background image width: "))
        # Prompt the user for the desired height
        height = int(input("Enter the desired background image height: "))
        # Create a new image with a white background
        empty_image = Image.new("RGB", (width, height), "white")
        empty_image.save(output_path)
        print(f"Empty image saved to: {output_path}")
        return output_path

    def paste_image(self, background_image_path="", overlay_image_path="", output_image_path="output_image.png", overlay_x_pos = 100):
        background = Image.open(background_image_path)
        overlay = Image.open(overlay_image_path)
        overlay_position = (background.size[0]//2 - overlay.size[0]//2, overlay_x_pos)
        background.paste(overlay, overlay_position)

        # Save the result
        background.save(output_image_path)
        print(f"Image with overlay saved to: {output_image_path}")
    
    def make_image_gradient(self, img, x, y, x1, y1, start, end, direction = "portrait"):
        # start="222222"
        # end = "000088"
        if (x > x1 or y > y1):
            return False

        if (direction == "portrait"):
            steps = y1 - y
            for i in range(steps):
                r = start[0] - (((start[0] - end[0]) / steps) * i)
                g = start[1] - (((start[1] - end[1]) / steps) * i)
                b = start[2] - (((start[2] - end[2]) / steps) * i)
                draw = ImageDraw.Draw(img)
                draw.rectangle([(x,y + i),(x1,y + i + 1)], fill = (r,g,b) )
        else:
            steps = x1 - x
            for i in range(steps):
                r = s[0] - (((s[0] - e[0]) / steps) * i)
                g = s[1] - (((s[1] - e[1]) / steps) * i)
                b = s[2] - (((s[2] - e[2]) / steps) * i)
                draw = ImageDraw.Draw(img)
                draw.rectangle([(x + i, y),(x + i + 1, y1)], fill = (r,g,b) )
        return img

    def generate_background_image(self, background_image_path="", overlay_image_path="", output_image_path="output_image.png", overlay_x_pos = 100):
        background = Image.open(background_image_path)
        overlay = Image.open(overlay_image_path)
        overlay_position = (background.size[0]//2 - overlay.size[0]//2, overlay_x_pos)
        width, height = background.size
        random_numbers = 20
        split_number = 2

        square_size = width
        remaining_to_square_size = width - height
        if (remaining_to_square_size / 2 <= height):
            ############/ First method ##########
            avg_color_keeper = []
            for partial in range(split_number):
                array_colors = [[], [], [], []]
                rand_x = []
                for i in range(random_numbers):
                    rand_x.append(rand(partial * (width / split_number), partial * (width / split_number) + (width / split_number - 1)))
                
                rand_y = []
                for i in range(random_numbers):
                    rand_y.append(rand(0, height / 2 - 1))

                for i in range(random_numbers):
                    array_color = overlay.getpixel((rand_x[i], rand_y[i]))
                    for j in range(len(array_color)):
                        array_colors[j].append(array_color[j])
                
                sum = [0, 0, 0, 0]
                avg = [0, 0, 0, 0]
                for channel in range(len(array_colors)):
                    for i in range(random_numbers):
                        sum[channel] += array_colors[channel][i]
                    
                    avg[channel] = (int)(sum[channel] / random_numbers)
                
                avg_color_keeper.append(avg)
            
            dest = background
            for partial in range(split_number):
                color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                if (partial == split_number - 1):
                    color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                else:
                    color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                
                result = self.make_image_gradient(dest, partial * (width / split_number - 1), 0, partial * (width / split_number) + (width / split_number - 1), remaining_to_square_size / 2, color_start, color_end,  direction = "landscape")
                if (result != false):
                    dest = result
        
            dest = background
            for partial in range(split_number):
                color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                if (partial == split_number - 1):
                    color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                else:
                    color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                
                result = self.make_image_gradient(dest, partial * (width / split_number - 1), 0, partial * (width / split_number) + (width / split_number - 1), remaining_to_square_size / 2, color_start, color_end,  direction = "landscape")
                if (result != false):
                    dest = result

            ############/ half bottom ##############
            avg_color_keeper = []
            for partial in range(split_number):
                array_colors = [[], [], [], []]
                rand_x = []
                for i in range(random_numbers):
                    rand_x.append(rand(partial * (width / split_number), partial * (width / split_number) + (width / split_number - 1)))
                
                rand_y = []
                for i in range(random_numbers):
                    rand_y.append(rand_y, rand(height / 2, height - 1))

                for i in range(random_numbers):
                    array_color = overlay.getpixel((rand_x[i], rand_y[i]))
                    for j in range(len(array_color)):
                        array_colors[j].append(array_color[j])
                
                sum = [0, 0, 0, 0]
                avg = [0, 0, 0, 0]
                for channel in range(len(array_colors)):
                    for i in range(random_numbers):
                        sum[channel] += array_colors[channel][i]
                    
                    avg[channel] = (int)(floor(sum[channel] / random_numbers))
                
                avg_color_keeper.append(avg)

            for partial in range(split_number):
                color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                if (partial == split_number - 1):
                    color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                else:
                    color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                
                result = self.make_image_gradient(dest, partial * (width / split_number - 1), square_size - remaining_to_square_size / 2, partial * (width / split_number) + (width / split_number - 1), square_size, color_start, color_end,  direction = "landscape")
                if (result != false):
                    dest = result

            self.paste_image(background, overlay)
            
            # ###########/ Second method ##########
            # this takes more time but the result is more convenient
            # for x in range(width):
            #     # half top of the image
            #     for y in range(remaining_to_square_size / 2):
            #         array_color = overlay.getpixel((x, y))
            #         for i in range(len(array_color)):
            #             array_colors[i].append(array_color[i])

            # for x in range(width):
            #     # half bottom of the image
            #     for y in range(floor(height - (remaining_to_square_size / 2)),height):
            #         array_color = overlay.getpixel((x, y))
            #         for i in range(len(array_color)):
            #             array_colors[i].append(array_color[i])

            # # it's time to calculate the average
            # # first array => half top => array of RGBA
            # # second array => half bottom => array of RGBA
            # avg_array = [[[[], [], [], []]], [[[], [], [], []]]]
            # # half top
            # for x in range(width):
            #     for channel in range(len(array_colors)):
            #         sum = 0
            #         for i in range(x * (remaining_to_square_size / 2), (x + 1) * (remaining_to_square_size / 2)):
            #             sum += array_colors[channel][i]
                    
            #         avg_array[0][channel][x] = sum / (remaining_to_square_size / 2)

            # # half bottom
            # for x in range(width):
            #     for channel in range(len(array_colors)):
            #         sum = 0
            #         for i in range(x * (remaining_to_square_size / 2) + (remaining_to_square_size / 2 * width), (x + 1) * (remaining_to_square_size / 2) + (remaining_to_square_size / 2 * width)):
            #             sum += array_colors[channel][i]
                    
            #         avg_array[1][channel][x] = sum / (remaining_to_square_size / 2)
                
            # for x in range(width):
            #     # half top of the image
            #     for y in range(remaining_to_square_size / 2):
            #         color = (avg_array[0][0][x], avg_array[0][1][x], avg_array[0][2][x])
            #         background.putpixel((x, y), color)

            # for x in range(width):
            #     # half bottom of the image
            #     for y in range(floor(square_size - (remaining_to_square_size / 2))):
            #         color = (avg_array[1][0][x], avg_array[1][1][x], avg_array[1][2][x])
            #         background.putpixel((x, y), color)

            # self.paste_image(background, overlay)
        else:
            ###########/ First method ##########
            avg_color_keeper = []
            for partial in range(split_number):
                array_colors = [[], [], [], []]
                rand_x = []
                for i in range(random_numbers):
                    rand_x.append(rand(partial * (width / split_number), partial * (width / split_number) + (width / split_number - 1)))
                
                rand_y = []
                for i in range(random_numbers):
                    rand_y.append(rand(0, height / 2 - 1))
                
                for i in range(random_numbers):
                    # gb_overlay = overlay.convert('RGB')
                    array_color = overlay.getpixel((rand_x[i], rand_y[i]))
                    for j in range(len(array_color)):
                        array_colors[j].append(array_color[j])
                    
                sum = [0, 0, 0, 0]
                avg = [0, 0, 0, 0]
                for channel in range(len(array_colors)):
                    for i in range(random_numbers):
                        sum[channel] += array_colors[channel][i]
                    
                    avg[channel] = (int)(floor(sum[channel] / random_numbers))
                
                avg_color_keeper.append(avg)

            for partial in range(split_number):
                color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                if (partial == split_number - 1):
                    color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                else:
                    color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                
                result = self.make_image_gradient(background, partial * (width / split_number - 1), 0, partial * (width / split_number) + (width / split_number - 1), remaining_to_square_size / 2, color_start, color_end,  direction = "landcape")
                if (result != false):
                    background = result

            ############/ half bottom ##############
            avg_color_keeper = []
            for partial in range(split_number):
                array_colors = [[], [], [], []]
                rand_x = []
                for i in range(random_numbers):
                    rand_x.append(rand(partial * (width / split_number), partial * (width / split_number) + (width / split_number - 1)))
                
                rand_y = []
                for i in range(random_numbers):
                    rand_y(rand(height / 2, height - 1))
                
                for i in range(random_numbers):
                    array_color = overlay.getpixel((rand_x[i], rand_y[i]))
                    for j in range(len(array_color)):
                        array_colors[j].append(array_color[j])
                
                sum = [0, 0, 0, 0]
                avg = [0, 0, 0, 0]
                for channel in range(len(array_colors)):
                    for i in range(random_numbers):
                        sum[channel] += array_colors[channel][i]
                    
                    avg[channel] = (int)(floor(sum[channel] / random_numbers))
                
                avg_color_keeper.append(avg)

            for partial in range(split_number):
                color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                if (partial == split_number - 1):
                    color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                else:
                    color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                
                result = self.make_image_gradient(dest, partial * (width / split_number - 1), square_size - remaining_to_square_size / 2, partial * (width / split_number) + (width / split_number - 1), square_size, color_start, color_end,  direction = "portrait")
                if (result != false):
                    dest = result
                
            self.paste_image(background, overlay)

        if (width > height):
            pass
        elif (height > width):
            square_size = height
            remaining_to_square_size = height - width
            if (remaining_to_square_size / 2 <= width):
                ###########/ First method ##########
                avg_color_keeper = []
                for partial in range(split_number):
                    array_colors = [[], [], [], []]
                    rand_x = []
                    for i in range(random_numbers):
                        rand_x.append(rand(0, width / 2 - 1))
                    
                    rand_y = []
                    for i in range(random_numbers):
                        rand_y.append(rand(partial * (height / split_number), partial * (height / split_number) + (height / split_number - 1)))

                    for i in range(random_numbers):
                        array_color = overlay.getpixel((rand_x[i], rand_y[i]))
                        for j in range(len(array_color)):
                            array_colors[j].append(array_color[j])
                    
                    sum = [0, 0, 0, 0]
                    avg = [0, 0, 0, 0]
                    for channel in range(len(array_colors)):
                        for i in range(random_numbers):
                            sum[channel] += array_colors[channel][i]
                        
                        avg[channel] = (int)(floor(sum[channel] / random_numbers))
                    
                    avg_color_keeper.append(avg)
                
                for partial in range(split_number):
                    color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                    if (partial == split_number - 1):
                        color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                    else:
                        color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                    
                    result = self.make_image_gradient(background, 0, partial * (height / split_number - 1), remaining_to_square_size / 2, partial * (height / split_number) + (height / split_number - 1), color_start, color_end, direction = "portrait")
                    if (result != false):
                        background = result

                ############/ half bottom ##############
                avg_color_keeper = []
                for partial in range(split_number):
                    array_colors = array(array(), array(), array(), array())
                    rand_x = []
                    for i in range(random_numbers):
                        rand_x.append(rand(width / 2, width - 1))
                    
                    rand_y = []
                    for i in range(random_numbers):
                        rand_y.append(rand(partial * (height / split_number), partial * (height / split_number) + (height / split_number - 1)))

                    for i in range(random_numbers):
                        array_color = overlay.getpixel((rand_x[i], rand_y[i]))
                        for j in range(len(array_color)):
                            array_colors[j].append(array_color[j])
                        
                    sum = [0, 0, 0, 0]
                    avg = [0, 0, 0, 0]
                    for channel in range(len(array_colors)):
                        for i in range(random_numbers):
                            sum[channel] += array_colors[channel][i]
                        
                        avg[channel] = (int)(floor(sum[channel] / random_numbers))
                    
                    avg_color_keeper.append(avg)

                for partial in range(split_number):
                    color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                    if (partial == split_number - 1):
                        color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                    else:
                        color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                    
                    result = this.make_image_gradient(dest, square_size - remaining_to_square_size / 2, partial * (height / split_number - 1), square_size, partial * (height / split_number) + (height / split_number - 1), color_start, color_end, direction = "portrait")
                    if (result != false):
                        dest = result   
            else:
                ###########/ First method ##########
                avg_color_keeper = []
                for partial in range(split_number):
                    array_colors = [[], [], [], []]
                    rand_x = []
                    for i in range(random_numbers):
                        rand_x.append(rand(0, width / 2 - 1))
                    
                    rand_y = []
                    for i in range(random_numbers):
                        rand_y.append(rand(partial * (height / split_number), partial * (height / split_number) + (height / split_number - 1)))
                    
                    for i in range(random_numbers):
                        array_color = overlay.getpixel((rand_x[i], rand_y[i]))
                        for j in range(len(array_color)):
                            array_colors[j].append(array_color[j])
                    
                    sum = [0, 0, 0, 0]
                    avg = [0, 0, 0, 0]
                    for channel in range(len(array_colors)):
                        for i in range(random_numbers):
                            sum[channel] += array_colors[channel][i]
                        
                        avg[channel] = (int)(floor(sum[channel] / random_numbers))
                    
                    avg_color_keeper.append(avg)
                
                for partial in range(split_number):
                    color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                    if (partial == split_number - 1):
                        color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                    else:
                        color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                    
                    result = self.make_image_gradient(background, 0, partial * (height / split_number - 1), remaining_to_square_size / 2, partial * (height / split_number) + (height / split_number - 1), color_start, color_end, direction = "portrait")
                    if (result != false):
                        background = result

                ############/ half bottom ##############
                avg_color_keeper = []
                for partial in range(split_number):
                    array_colors = array(array(), array(), array(), array())
                    rand_x = []
                    for i in range(random_numbers):
                        rand_x.append(rand(width / 2, width - 1))
                    
                    rand_y = []
                    for i in range(random_numbers):
                        rand_y.append(rand(partial * (height / split_number), partial * (height / split_number) + (height / split_number - 1)))

                    for i in range(random_numbers):
                        array_color = overlay.getpixel((rand_x[i], rand_y[i]))
                        for j in range(len(array_color)):
                            array_colors[j].append(array_color[j])
                    
                    sum = [0, 0, 0, 0]
                    avg = [0, 0, 0, 0]
                    for channel in range(len(array_colors)):
                        for i in range(random_numbers):
                            sum[channel] += array_colors[channel][i]
                        
                        avg[channel] = (int)(floor(sum[channel] / random_numbers))
                    
                    avg_color_keeper.append(avg)

                for partial in range(split_number):
                    color_start = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                    if (partial == split_number - 1):
                        color_end = (avg_color_keeper[partial][0], avg_color_keeper[partial][1], avg_color_keeper[partial][2])
                    else:
                        color_end = (avg_color_keeper[partial + 1][0], avg_color_keeper[partial + 1][1], avg_color_keeper[partial + 1][2])
                    
                    result = self.make_image_gradient(background, square_size - remaining_to_square_size / 2, partial * (height / split_number - 1), square_size, partial * (height / split_number) + (height / split_number - 1), color_start, color_end, direction = "portrait")
                    if (result != false):
                        background = result
        else:
            print("here")
            pass
    
    def get_average_color(self,image):
        """Calculate the average color of an image."""
        return tuple(int(sum(channel) / len(channel)) for channel in zip(*image.getdata()))

    def apply_average_color(self, background_path, overlay_path, output_path):
        # Open the background and overlay images
        background = Image.open(background_path).convert('RGBA')
        overlay = Image.open(overlay_path).convert('RGBA')

        # Set the desired position for the overlay image (x, y, width, height)
        overlay_position = (background.size[0]//2-overlay.size[0]//2, 50, overlay.size[0], overlay.size[1])
        # Iterate over each row in the overlay image
        for row in range(overlay.height):
            # Crop the row from the overlay image
            row_image = overlay.crop((0, row, overlay.width, row + 1))
            # Calculate the average color of the row
            average_color = self.get_average_color(row_image)
            background.paste(average_color, (0, row, 0 + background.width, row + 1))
        for row in range(overlay.height,background.height):
            background.paste(average_color, (0, row, 0 + background.width, row + 1))

        background.paste(overlay, (overlay_position[0],overlay_position[1]))
        background.save(output_path)
        print(f"Image with averaged colors saved to: {output_path}")

if __name__ == "__main__":
    img_class = ImageClass()
    image_file_path = img_class.select_image()
    resized_image_file_path = img_class.resize_image(image_file_path)
    empty_image_file_path = img_class.create_empty_image()
    img_class.paste_image(empty_image_file_path, resized_image_file_path)
    # img_class.generate_background_image(background_image_path=empty_image_file_path, overlay_image_path=resized_image_file_path, output_image_path="output_image.jpg", overlay_x_pos = 100)
    img_class.apply_average_color(empty_image_file_path, resized_image_file_path, "output_image.png")
