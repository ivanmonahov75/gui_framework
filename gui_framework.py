# custom "lib" for fast gui setup

# libs
import dearpygui.dearpygui as dpg


class MyGUI:
    def __init__(self, UI_type='eng_small'):

        # set internal flags
        self.enable_com = False
        self.enable_flight = False
        if UI_type == 'eng_small':
            print('eng_small')

    def comm_stop(self, sender):
        self.enable_com = False
        dpg.set_item_label(sender + 1, 'Start')

    def comm_start(self, sender):
        self.enable_com = True
        dpg.set_item_label(sender, 'Started')

    def flight_stop(self, sender):
        self.enable_flight = False
        dpg.set_item_label(sender + 1, 'Start')

    def flight_start(self, sender):
        self.enable_flight = True
        dpg.set_item_label(sender, 'Started')

    # values: header, [name of value, value]
    def block_text(self, name, data, spacing=True):  # simple function 
        if spacing: dpg.add_text('')
        dpg.add_text(name)
        for name, val in zip(data.keys(), data.values()):
            with dpg.group(horizontal=True):
                dpg.add_text(name)
                dpg.add_text(val)

    # values: header, [label, callback]

    def block_button(self, title, data, spacing=True):  # simple function for faster init
        if spacing: dpg.add_text('')
        dpg.add_text(title)
        with dpg.group(horizontal=True):
            for name, callback in zip(data.keys(), data.values()):
                dpg.add_button(label=name, callback=callback)

    # name speaks for itself
    def start(self, fullscreen=False):
        dpg.create_context()
        # use full-screen if needed
        if fullscreen:
            dpg.toggle_viewport_fullscreen()

        # setup font
        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf file
            default_font = dpg.add_font("gui_framework/font.ttf", 22)
        dpg.bind_font(default_font)

        # make main window
        dpg.create_viewport(title='UAV Controls', width=1280, height=800)
        dpg.setup_dearpygui()

        # open image
        width, heights, depth, data = dpg.load_image('gui_framework/def_img.jpg')
        with dpg.texture_registry():
            dpg.add_dynamic_texture(width, heights, data, tag='img')

        # implement image into window
        min_length = 160
        scale_factor_img = 1.67
        width_img = 4 * min_length * scale_factor_img
        heights_img = 3 * min_length * scale_factor_img
        with dpg.window(label="Video stream", width=width_img, height=heights_img):
            with dpg.drawlist(width=width_img, height=heights_img - 50):
                dpg.draw_image("img", (0, 0), (width_img, heights_img), uv_min=(0, 0), uv_max=(1, 1))

        # setup window with contorls
        with dpg.window(label="Controls", pos=[round(width_img), 0], width=(1280 - round(width_img)), height=800):
            # setup buttons
            self.block_button('Communication', {'Stop': self.comm_stop, 'Start': self.comm_start}, spacing=False)
            self.block_button('Secondary', {'Unfold': None, 'Fold': None}, spacing=False)

            # setup displayed values
            self.block_text('Bat. state:', {'V:': 'N/A', '%: ': 'N/A'})
            self.block_text('Coordinates:', {'Lat:': 'N/A', 'Long:': 'N/A', 'Atl:': '0 m.'})
            self.block_text('Angles:', {'Roll:': 'N/A', 'Pitch:': 'N/A'})
            self.block_text('Current modes:', {'Activated:': 'False', 'Speed:': "Low", 'Flight:': 'Vert.'})

            # button to stop program
            dpg.add_button(label="Stop prog.", callback=dpg.destroy_context)

        # internal
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            print(self.enable_com)

            dpg.render_dearpygui_frame()
