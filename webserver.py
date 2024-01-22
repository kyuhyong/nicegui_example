# For nicegui
from nicegui import app, Client, ui_run, ui, events

class WebServer:
    def __init__(self):
        self.markers1 = []
        with Client.auto_index_client:
            
            #create a row
            with ui.row().classes('w-full h-60 no-wrap').style("height: 100%"):
                self.ui_map = ui.leaflet(center=(37.1, 127.2))
                self.ui_map.on('map-click', self.handle_click)
                ui.label().bind_text_from(self.ui_map, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
                ui.label().bind_text_from(self.ui_map, 'zoom', lambda zoom: f'Zoom: {zoom}')
            with ui.row().classes('items-stretch'):
                ui.button('center', on_click=lambda: self.cb_button())
                ui.button('clear', on_click=lambda: self.clear_markers(self.markers1))
            
        ui.run()

    def cb_button(self):
        print("Pressed button")
        #self.ui_map.marker(latlng=(37.2, 127.3))
        #self.ui_map.set_center(center=(38.5,127,1))

    def handle_click(self, e: events.GenericEventArguments):
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