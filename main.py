import tkinter as tk
from tkinter import ttk, Menu, filedialog
from PIL import Image
from core_operations import grayscale, ordered_dithering, auto_levels
from optional_operations import mirror, auto_contrast, sepia, posterize, invert, night_vision, grain, warm, brightness_adjust, blur, sharpen
import utils

from tkinter import font



class BMPViewer(tk.Tk):
    # BMP viewer initializer
    def __init__(self):
        tk.Tk.__init__(self)
        print("intializing")

        print(font.names())
        # set window title and size
        self.title("BMP Photo Editing, CMPT 365")
        self.geometry("1200x700")

        # Set dark theme colors
        self.configure(bg="#2E2E2E")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=10, background="#4A4A4A", foreground="#FFFFFF")
        self.style.configure("TFrame", padding=10, background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Helvetica", 20, "bold italic"))
        self.style.configure("TextLabel.TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Helvetica", 12, "italic"))
        self.style.configure("TMenubutton", font=("Helvetica", 12), background="#4A4A4A", foreground="#FFFFFF")
        
        self.title=ttk.Label(self, text="BMP Photo Editor", style="TLabel")
        self.title.pack(side=tk.TOP, pady=10)

        self.image_info=ttk.Label(self, text="", style="TextLabel.TLabel")
        self.image_info.pack(side=tk.TOP, pady=5)

        # create main frame
        self.frame = ttk.Frame(self, style="TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # canvas for original image
        self.canvas = tk.Canvas(self.frame, width=100, height=100, bg="#1C1C1C", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.arrow_label = ttk.Label(self.frame, text="➡", style="TLabel")
        self.arrow_label.pack(side=tk.LEFT, padx=10)
        
        # canvas for image after the operation is applied
        self.operation_canvas = tk.Canvas(self.frame, width=100, height=100, bg="#1C1C1C", highlightthickness=0)
        self.operation_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # variable to store selected core operation
        self.selected_option = tk.StringVar()
        self.selected_option.set(None)
        self.selected_option.trace_add("write", self.handle_selection)

        # variable to store file path
        self.filepath = tk.StringVar()
        self.filepath.set(None)

        # variable to store last operation, necessary for reapplying operation after file alteration
        self.last_operation = None

        # variable to store processed pixels, necessary for exporting
        self.processed_pixels = None

        self.init_buttons()
        self.create_menus()

    def init_buttons(self):
        button_frame = ttk.Frame(self, style="TFrame")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Import File Button
        import_button = ttk.Button(button_frame, text="📁 Import File", command=self.open_file_dialog)
        import_button.pack(side=tk.LEFT, padx=10)

        # Export Button
        export_button = ttk.Button(button_frame, text="💾 Export", command=self.export_bmp)
        export_button.pack(side=tk.LEFT, padx=10)

        clear_button = ttk.Button(button_frame, text="🧹 Clear Canvas", command=self.clear)
        clear_button.pack(side=tk.LEFT, padx=10)

        # Dropdown menu for core and optional operations (drop up)
        dropdown_button = ttk.Menubutton(button_frame, text="🔗 Operations", style="TMenubutton")
        dropdown_button.pack(side=tk.LEFT, padx=10)
        self.dropdown_menu = Menu(dropdown_button, tearoff=0, background="#4A4A4A", foreground="#FFFFFF", font=("Helvetica", 12))
        dropdown_button.config(menu=self.dropdown_menu)
        self.add_operations_to_menu()

        # Exit Button
        exit_button = ttk.Button(button_frame, text="❌ Exit", command=self.quit)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def create_menus(self):
        print("* C * creating menus")

        # create main menu
        main_menu = Menu(self, tearoff=False, background="#4A4A4A", foreground="#FFFFFF", font=("Helvetica", 12))
        self.config(menu=main_menu)

        # create core operations dropdown menu in the main menu
        core_dropdown_menu = Menu(main_menu, tearoff=False, background="#4A4A4A", foreground="#FFFFFF", font=("Helvetica", 12))
        core_options = ["open file", "exit", "grayscale", "ordered dithering", "auto level"]
        for option in core_options:
            # add radio buttons for each core operation
            core_dropdown_menu.add_radiobutton(label=option, variable=self.selected_option, value=option)
        main_menu.add_cascade(label="Core Operations", menu=core_dropdown_menu)

        # create optional operations dropdown menu in the main menu
        optional_dropdown_menu = Menu(main_menu, tearoff=False, background="#4A4A4A", foreground="#FFFFFF", font=("Helvetica", 12))
        optional_options = ["mirror", "failed auto", "auto contrast", "sepia", "posterize", "invert", "night vision", "grain", "blur", "sharpen", "brightness", "warm tone"]
        for option in optional_options:
            # add radio buttons for each optional operation
            optional_dropdown_menu.add_radiobutton(label=option, variable=self.selected_option, value=option)
        main_menu.add_cascade(label="Optional Operations", menu=optional_dropdown_menu)

    def add_operations_to_menu(self):
        # Add core and optional operations to the dropdown menu
        core_options = ["grayscale", "ordered dithering", "auto level"]
        optional_options = ["mirror", "auto contrast", "sepia", "posterize", "invert", "night vision", "grain", "blur", "sharpen", "brightness", "warm tone"]
        for option in core_options + optional_options:
            self.dropdown_menu.add_radiobutton(label=option, variable=self.selected_option, value=option)

    #def display_width_height(self, w, h):


    def open_file_dialog(self):
        print("* O_F * opening file dialog")

        # open file dialog to select BMP file
        file_path = filedialog.askopenfilename(
            filetypes=[("BMP files", "*.bmp")], title="Select a BMP file"
        )

        # if file path is not empty, set the file path variable and print the original image
        if file_path:
            self.filepath.set(file_path)
            self.check_header(file_path, None)

            # reapply last operation if it exists
            if self.last_operation and self.last_operation != "export":
                self.run(self.last_operation, file_path)
            
            if self.last_operation == "export":
                self.last_operation = None
                self.selected_option.set(None)
                self.operation_canvas.delete("all")

    def handle_selection(self, *args):
        print("* H_S * handling selection")

        # get selected core operation
        core_option = self.selected_option.get()

        # if core operation is exit, quit the application
        if core_option == "exit":
            self.quit()
            return
        
        # if core operation is open file, open file dialog
        if core_option == "open file":
            self.open_file_dialog()
            return
        
        # edge case if we just dithered, we need to reset the canvas
        if self.last_operation == "ordered dithering":
            self.check_header(self.filepath.get(), None)

        # update last operation to our selected core operation
        self.last_operation = core_option

        # get file path
        file_path = self.filepath.get()

        # if file path is empty or doesnt exist for some reason, print error message
        if not file_path or file_path == "None":
            print("error in handle selection, no file selected")
            return
        
        # run the selected core operation
        if core_option and core_option != "None":
            self.run(core_option, file_path)

    def run(self, selected_value, file_path):
        print("* R * running with:", selected_value, file_path)

        # check if we have a file, i don't think this is necessary but just incase 
        if not file_path or file_path == "None":
            print("error in run function, no file selected")
            return
        
        # run the selected core operation
        if selected_value and selected_value != "None":
            print("* R * starting run function", selected_value, file_path)
            self.check_header(file_path, selected_value)

    def export_bmp(self):
        # export operation

        # open file dialog to select export location
        file_path=filedialog.asksaveasfilename(defaultextension=".bmp",filetypes=[("BMP files","*.bmp")])

        if not file_path:
            return
        
        # if no image has been operationed on, return
        if not hasattr(self,"processed_pixels"):
            return
        
        # call upon our global variable
        pixels=self.processed_pixels

        # extract information needed to save
        w,h=len(pixels[0]),len(pixels)
        pixel_data=[]
        for row in pixels:
            pixel_data.extend(row)

        # create image and save
        img=Image.new("RGB",(w, h))
        img.putdata(pixel_data)
        img.save(file_path,format="BMP")

        # i realize i could "unparse" the header and write it to the file but this is easier
        # also, i could create corrupted files and i don't want to do that

        print("exported to ",file_path)

    def clear(self):
        # clear operation
        self.image_info.config(text="")
        self.filepath.set(None)
        self.selected_option.set(None)
        self.last_operation=None
        self.canvas.delete("all")
        self.operation_canvas.delete("all")

    # FLOW CONTROL #
    # i.e. a hub for all operations



    def flow_control(self,pixels,w,h,operation_flag=None):
        # hub for all operations
        # this is not great code

        print("* F_C * flow control")
        # basically, for each flag, we print the operation pixels.

        if operation_flag=="auto level":
            operation_pixels=auto_levels.apply_auto_levels(pixels,w,h,"reg")
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="grayscale":
            operation_pixels=grayscale.apply_grayscale(w,h,pixels)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="ordered dithering":
            gray_pixels=grayscale.apply_grayscale(w,h,pixels)
            self.print_bmp(w,h,gray_pixels)
            operation_pixels=ordered_dithering.apply_ordered_dithering(w,h,gray_pixels)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="mirror":
            operation_pixels=mirror.apply_mirror(pixels,w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="failed auto":
            operation_pixels=auto_levels.apply_auto_levels(pixels,w,h,"acid")
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="auto contrast":
            operation_pixels=auto_contrast.apply_auto_contrast(pixels,w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="sepia":
            operation_pixels=sepia.apply_sepia(pixels,w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="posterize":
            operation_pixels=posterize.apply_posterize(pixels,w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="invert":
            operation_pixels=invert.apply_invert(pixels,w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="night vision":
            operation_pixels=night_vision.apply_night_vision(grayscale.apply_grayscale(w,h,pixels),w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="grain":
            operation_pixels=grain.apply_grain(pixels,w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="blur":
            operation_pixels=blur.apply_blur(pixels,w,h)
            self.operation_print(w,h,operation_pixels)
        
        elif operation_flag=="sharpen":
            operation_pixels=sharpen.apply_sharpen(pixels,w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="brightness":
            operation_pixels=brightness_adjust.apply_brightness(pixels,w,h)
            self.operation_print(w,h,operation_pixels)

        elif operation_flag=="warm tone":
            operation_pixels=warm.apply_warm_tone(pixels,w,h)
            self.operation_print(w,h,operation_pixels)
    
        elif operation_flag=="export":
            self.export_bmp()
        
        # print original image
        elif operation_flag is None:
            self.print_bmp(w,h,pixels)

        # save our processed pixels for exporting
        if operation_flag not in ["export",None]:
            self.processed_pixels=operation_pixels
        


    # BMP PARSING #


    def unpack_header(self,header):
        print("* U_H * unpacking header")
        # helper function to unpack header
        w=utils.int_from_bytes(header[4:8])
        h=utils.int_from_bytes(header[8:12])
        bpp=utils.int_from_bytes(header[14:16])
        compression=utils.int_from_bytes(header[16:20])

        return w,h,bpp,compression        



    def check_header(self,filepath,operation_flag=None):
        print("* C_H * checking header")
        print("operation flag: ",operation_flag)
        # parse header
        with open(filepath,"rb") as file:
            if file is None:
                raise ValueError("no file?")

            header = file.read(14)
            if header is None:
                raise ValueError("invalid header")

            if header[:2]!=b"BM":
                raise ValueError("incorrect file format")

            pixel_start =utils.int_from_bytes(header[10:14])
            dib_header = file.read(40)

            if dib_header is None:
                raise ValueError("no dib header or invalid")
            
            w,h,bpp,compression= self.unpack_header(dib_header)

            if h>576 or w>704:
                raise ValueError("image too big")

            if compression!=0:
                raise ValueError("compressed image")

            if bpp!=24:
                raise ValueError("image must be 24 bit")
            
            self.update_image_info(w, h, bpp)

            file.seek(pixel_start)
            pixels = []
            row_padding = (4-(w*3)%4)%4

            for y in range(h):
                row = []
                for x in range(w):
                    b=file.read(1)[0]
                    g=file.read(1)[0]
                    r=file.read(1)[0]
                    row.append((r,g,b))

                pixels.append(row)
                file.read(row_padding)
    
        pixels.reverse() # images were upside down for some reason


        self.flow_control(pixels,w,h,operation_flag)



    # BMP DISPLAY #



    def print_bmp(self,w,h,pixels):
        # printing the original image

        print("* P_B * printing bmp")

        # reinitialize canvas
        self.canvas.config(width=w,height=h)
        self.canvas.delete("all")

        # using tkinter photo image because is faster than drawing rectangles
        photo = tk.PhotoImage(width=w,height=h)
        
        for x in range(w):
            for y in range(h):
                rgb_instance=pixels[y][x]
                color="#%02x%02x%02x"%rgb_instance
                photo.put(color,(x,y)) # plot each pixel

        self.canvas.create_image(0,0,image=photo,anchor=tk.NW)
        self.canvas.image=photo



    def operation_print(self,w,h,pixels):
        # printing the operation'd image

        print("* O_P * operation print")

        # reinitialize canvas
        self.operation_canvas.config(width=w,height=h)
        self.operation_canvas.delete("all")

        # using tkinter photo image because is faster than drawing rectangles
        photo = tk.PhotoImage(width=w,height=h)
        
        for x in range(w):
            for y in range(h):
                rgb_instance=pixels[y][x]
                color="#%02x%02x%02x"%rgb_instance
                photo.put(color,(x,y)) # plot each pixel

        self.operation_canvas.create_image(0,0,image=photo,anchor=tk.NW)
        self.operation_canvas.image=photo

    def update_image_info(self, width, height, bpp):
        self.image_info.config(text=f"Width: {width} px, Height: {height} px, BPP: {bpp}")



if __name__=="__main__":
    app=BMPViewer()
    app.mainloop()
