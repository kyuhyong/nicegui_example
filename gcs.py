# For nicegui
from nicegui import app, Client, ui_run, ui, events

class WebServer:
    def __init__(self):
        self.markers1 = []
        with Client.auto_index_client:
            #create a row
            with ui.row().classes('w-full h-60 no-wrap').style("height: 100%"):
                self.ui_map = ui.leaflet(center=(37.500643, 127.036377))
                self.ui_map.on('map-click', self.handle_map_click)
                #ui.label().bind_text_from(self.ui_map, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
                #ui.label().bind_text_from(self.ui_map, 'zoom', lambda zoom: f'Zoom: {zoom}')
            with ui.dialog() as self.dialog_yesno, ui.card():
                ui.label('Are you sure?')
                with ui.row():
                    ui.button('Yes', on_click=lambda: self.dialog_yesno.submit('Yes'))
                    ui.button('No', on_click=lambda: self.dialog_yesno.submit('No'))
            with ui.row().classes('items-stretch'):
                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label("Vehicle State")
                        ui.label("")
                        ui.label("Pref check: ")
                        self.ui_label_vs_pref_checked =     ui.label("")
                        ui.label("Armed: ")
                        self.ui_label_vs_armed =            ui.label("")
                        ui.label("Flying: ")
                        self.ui_label_vs_flying =           ui.label("")
                        ui.label("RC signal: ")
                        self.ui_label_vs_rc_signal =        ui.label("")
                        ui.label("Flight Mode: ")
                        self.ui_label_vs_flight_mode =      ui.label("")
                        ui.label("GCS connection: ")
                        self.ui_label_vs_gcs_connection =   ui.label("")
                        ui.label("Failsafe: ")
                        self.ui_label_vs_failsafe =         ui.label("")

                        ui.button("Terminate", on_click=self.show_dialog_check_terminate)

                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label("Mission State")
                        ui.label("")
                        ui.label("Type: ")
                        self.ui_label_ms_mission_type =     ui.label("")
                        ui.label("Status: ")
                        self.ui_label_ms_mission_status =   ui.label("")
                        ui.label("Path enu pos: ")
                        self.ui_label_ms_path_pos_enu =     ui.label("")
                        ui.label("Path geo pos: ")
                        self.ui_label_ms_path_pos_geo =     ui.label("")
                        ui.label("Target index: ")
                        self.ui_label_ms_target_idx =       ui.label("")
                        ui.label("Land state: ")
                        self.ui_label_land_state =          ui.label("")

                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label("Mission ACK")
                        ui.label("")
                        ui.label("Status: ")
                        self.ui_label_mc_ack_command_id =   ui.label("")
                        ui.label("Result: ")
                        self.ui_label_mc_ack_result =       ui.label("")
                        ui.label("Log:")
                        self.ui_label_log_msg =             ui.label("")
                    with ui.scroll_area().classes('w-70 h-40 border'):
                        self.ui_label_scroll = ui.label('I scroll. ' * 200)
                    ui.button("Add text", on_click=lambda: self.ui_button_add_txt())

                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label("Perception State")
                        ui.label("")
                        ui.label("Success: ")
                        self.ui_cb_percept_success =   ui.checkbox("")
                        ui.label("Count: ")
                        self.ui_label_percept_cnt =    ui.label("")

            with ui.row().classes('items-stretch'):
                #create a card with the joystick in it
                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label("Stick input")
                        ui.label("")
                        ui.label("Roll: ")
                        self.ui_label_stick_roll =      ui.label("")
                        ui.label("Pitch: ")
                        self.ui_label_stick_pitch =     ui.label("")
                        ui.label("Throttle: ")
                        self.ui_label_stick_throttle =  ui.label("")
                        ui.label("Yaw: ")
                        self.ui_label_stick_yaw =       ui.label("")
                        ui.label("CMD:")
                        self.ui_label_joy_cmd =         ui.label("")

                #create a card with the joystick in it
                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label("Keyboard input")
                        ui.label("")
                        ui.label("E:")
                        self.ui_label_key_e =           ui.label("")
                        ui.label("N:")
                        self.ui_label_key_n =           ui.label("")
                        ui.label("U:")
                        self.ui_label_key_u =           ui.label("")
                        ui.label("Yaw:")
                        self.ui_label_key_yaw =         ui.label("")
                        ui.label("CMD:")
                        self.ui_label_key_cmd =         ui.label("")

                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label("Tracker")
                        ui.label("")
                        ui.label("Lat:")
                        self.ui_label_tracker_lat =     ui.label("")
                        ui.label("Lon:")
                        self.ui_label_tracker_lon =     ui.label("")
                        ui.label("Alt:")
                        self.ui_label_tracker_alt =     ui.label("")
                        self.ui_cb_tracker_fixed =      ui.checkbox("Fixed")
                
                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label("Teleop")
                        ui.label("")
                        ui.button('ARM')
                        ui.button('DISARM')

                        ui.button('TAKE OFF')
                        ui.button('LAND')

                        ui.button('VISION LAND')
                        ui.button('AUTO_OFFBOARD')
                        ui.label('Target Pose')
                        self.ui_label_target_pose = ui.label("lat:000.00000, lng:000.00000")
                        self.ui_slider_target_alt = ui.slider(min = 0, max=100, value=5)
                        ui.label().bind_text_from(self.ui_slider_target_alt, 'value')
                        ui.button('Go to target')

            # UI Elements for vehicle status
            with ui.row().classes('items-stretch'):
                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label('Physical Position')
                        self.ui_cb_phy_pos_valid =      ui.checkbox("valid")
                        ui.label("Lat:")
                        self.ui_label_phy_pos_lat =     ui.label("0.0")
                        ui.label("Lon:")
                        self.ui_label_phy_pos_lon =     ui.label("0.0")
                        ui.label("Alt(msl):")
                        self.ui_label_phy_pos_alt =     ui.label("0.0m")

                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label('Physical Velocity')
                        self.ui_cb_phy_vel_valid =      ui.checkbox("valid")
                        ui.label('V(x):')
                        self.ui_label_phy_vel_x =       ui.label("0.0")
                        ui.label('V(y):')
                        self.ui_label_phy_vel_y =       ui.label("0.0")
                        ui.label('V(z):')
                        self.ui_label_phy_vel_z =       ui.label("0.0")
                
                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label('Physical attitude')
                        self.ui_cb_phy_att_valid =      ui.checkbox("valid")
                        ui.label('Roll:')
                        self.ui_label_phy_att_roll =    ui.label("0.0")
                        ui.label('Pitch:')
                        self.ui_label_phy_att_pitch =   ui.label("0.0")
                        ui.label('Yaw:')
                        self.ui_label_phy_att_yaw =     ui.label("0.0")
                
                with ui.card().classes('w-80 text-center items-left'):
                    with ui.grid(columns=2):
                        ui.label('Physical reference')
                        ui.label('')
                        ui.label('lat:')
                        self.ui_label_phy_ref_lat =    ui.label("0.0")
                        ui.label('lon:')
                        self.ui_label_phy_ref_lon =   ui.label("0.0")
                        ui.label('alt(msl):')
                        self.ui_label_phy_ref_alt =     ui.label("0.0")
        ui.run()

    async def show_dialog_check_terminate(self):
        result = await self.dialog_yesno
        ui.notify(f'You chose {result}')
        if result == "Yes":
            print("YES!")
        else:
            print("NO!")

    def cb_button(self):
        print("Pressed button")
        #self.ui_map.marker(latlng=(37.2, 127.3))
        #self.ui_map.set_center(center=(38.5,127,1))
    
    def ui_button_add_txt(self):
        text = self.ui_label_scroll.text + "Hello!!!\n\n"
        self.ui_label_scroll.set_text(text)

    def handle_map_click(self, e: events.GenericEventArguments):
        lat = e.args['latlng']['lat']
        lng = e.args['latlng']['lng']
        print(f"lat:{lat}, long: {lng}")
        self.clear_markers(self.markers1)
        self.markers1.append(self.ui_map.marker(latlng = (lat,lng)))

    def clear_markers(self, markers:[]):
        for marker in markers:
            self.ui_map.remove_layer(marker)
        markers.clear()
        

if __name__ in { '__main__', '__mp_main__' } :
	WebServer()