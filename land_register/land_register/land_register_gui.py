from PyQt6.QtWidgets import QTabWidget, QApplication, QMainWindow, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QDialog, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
import pyqtgraph as pg

import sys
#import yaml
import io
import folium

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

conf = {
    "gps_topic" : None, 
    "msg_type": "sensor_msgs/msg/NavSatFix",
}

puntos = list()

class GPSSubscriber(Node):
    def __init__(self):
        super().__init__("gps_sub")
        self.subscription = self.create_subscription(NavSatFix, conf["gps_topic"], self.subscription_callback, 10)
    
    def subscription_callback(self, msg: NavSatFix):
        puntos.append(
            {
                "Latitude": msg.latitude,
                "Longitude": msg.longitude,
                "Altitude": msg.altitude,
            }
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ros2_conf_w = None
        self.node_gps_sub = None

        self.titulo = "Registrador de parcelas"
        self.setWindowTitle(self.titulo)

        # Layaouts

        main_layaout = QVBoxLayout()
        add_del_layaout = QHBoxLayout()
        list_layaout = QVBoxLayout()
        central_layaout = QHBoxLayout()
        end_layaout = QHBoxLayout()

        # Labels

        title_label = QLabel(self.titulo)
        title_font = title_label.font()
        title_font.setPointSize(25)
        title_label.setFont(title_font)

        # Botones

        self.add_button = QPushButton("Añadir")
        self.remove_button = QPushButton("Eliminar punto")
        self.save_button = QPushButton("Guardar parcela")
        self.clear_button = QPushButton("Reset")

        ## Asociamos los callbacks
        self.add_button.clicked.connect(self.add_button_callback)
        self.remove_button.clicked.connect(self.remove_button_callback)
        self.save_button.clicked.connect(self.save_button_callback)
        self.clear_button.clicked.connect(self.clear_button_callback)

        # Lista

        self.gps_list = QListWidget()

        # Mapa

        self.map_web_engine = QWebEngineView()
        self.map_web_engine.setMinimumSize(400, 400)

        # Mapa como Gráfico

        self.map_plot = pg.PlotWidget()
        self.map_ploting = self.map_plot.plot([], [], pen=None, symbol="o", symbol_size=10)
        self.map_plot.setLabel("left", "Latitude")
        self.map_plot.setLabel("bottom", "Longitude")

        # Pestañas

        self.map_tab = QTabWidget()
        self.map_tab.addTab(self.map_web_engine, "Mapa")
        self.map_tab.addTab(self.map_plot, "Gráfico")


        # Acciones del menú

        ros2_conf_button = QAction(parent=self, text="ROS 2")
        ros2_conf_button.triggered.connect(self.conf_ros2_callback)

        # Menu

        menu = self.menuBar()

        conf_menu = menu.addMenu("&Configuración")
        conf_menu.addAction(ros2_conf_button)

        self.buttons_enabled() # Disabilita algunos botones

        # Composición de los layaouts

        main_layaout.addWidget(title_label) # Añadido al Layaout Title

        add_del_layaout.addWidget(self.add_button)
        add_del_layaout.addWidget(self.remove_button)
        add_del_layaout.addWidget(self.clear_button)

        list_layaout.addLayout(add_del_layaout)
        list_layaout.addWidget(self.gps_list)

        central_layaout.addLayout(list_layaout)
        central_layaout.addWidget(self.map_tab)

        end_layaout.addWidget(self.save_button)

        # Composición de la ventana

        main_layaout.addLayout(central_layaout)
        main_layaout.addLayout(end_layaout)

        widget = QWidget()
        widget.setLayout(main_layaout)
        self.setCentralWidget(widget)
    
    # Callbacks

    def conf_ros2_callback(self):
        if self.ros2_conf_w is None:
            self.ros2_conf_w = Ros2ConfWindow(self)
        
        if self.ros2_conf_w.exec():
            self.node_gps_sub = GPSSubscriber()

        self.buttons_enabled()
    
    def save_button_callback(self):
        #for i in range(self.gps_list.count()):
        #    item = self.gps_list.item(i).text()
        #    print(item)
        self.save_file_dialog()

    def clear_button_callback(self):
        refence_point = puntos[0]
        
        puntos.clear()
        self.gps_list.clear()
        self.buttons_enabled()
        self.map_ploting.setData([], [])
        self.update_map(ref_point=refence_point)
    
    def add_button_callback(self):
        rclpy.spin_once(self.node_gps_sub, timeout_sec=30.0)
        self.gps_list.clear()
        lat = []
        long = []
        for punto in puntos:
            punto_str = ""
            for k in punto.keys():
                punto_str = f"{punto_str}{k}: {punto[k]:.8f}\n"
            self.gps_list.addItem(punto_str)
        self.map_ploting.setData(long, lat) # Reset
        self.buttons_enabled()
        self.update_map()

    def remove_button_callback(self):
        item = self.gps_list.currentItem()

        if item is not None:
            row = self.gps_list.row(item)
            self.gps_list.takeItem(row)
            
            if len(puntos) == 1:
                ref_point = puntos[0]
            else:
                ref_point = None

            puntos.pop(row)
            self.buttons_enabled()
            self.update_map(ref_point=ref_point)
    
    def update_map(self, ref_point=None):

        if ref_point is None:
            init_point = [puntos[0]["Latitude"], puntos[0]["Longitude"]]
        else:
            init_point = [ref_point["Latitude"], ref_point["Longitude"]]
        
        puntos_list = []
        lat = []
        long = []
        data = io.BytesIO()
        
        map_folium = folium.Map(location=init_point, zoom_start=20, max_zoom=40)

        for punto in puntos:
            puntos_list.append([punto["Latitude"], punto["Longitude"]])
            lat.append(punto["Latitude"])
            long.append(punto["Longitude"])
            folium.Circle(radius=0.1,
                          color="Red",
                          fill=True,
                          fill_color="Red", 
                          fill_opacity=0.5,
                          location=puntos_list[-1], 
                          popup=f"Punto número: {len(puntos_list)}").add_to(map_folium)
            #folium.Marker(location=puntos_list[-1], popup=f"Punto número: {len(puntos_list)}").add_to(map_folium)

        if len(puntos_list) > 1:
            folium.Polygon(locations=puntos_list, 
                        color="blue", 
                        weight=2, 
                        fill_color="blue", 
                        fill_opacity=0.7, 
                        fill=True, 
                        popup="Area del terreno").add_to(map_folium)

        map_folium.save(data, close_file=False)

        self.map_ploting.setData(long, lat)
        self.map_web_engine.setHtml(data.getvalue().decode())
    ##
    
    def buttons_enabled(self):
        if conf["gps_topic"] is None:
            self.add_button.setEnabled(False)
            self.remove_button.setEnabled(False)
        else:
            self.add_button.setEnabled(True)
            self.remove_button.setEnabled(True)
        
        self.save_button.setEnabled(self.gps_list.count() >= 4)
        self.clear_button.setEnabled(self.gps_list.count() > 0)
    
    def save_file_dialog(self):
        import geopandas
        from shapely.geometry import Polygon

        #ruta, _ = QFileDialog.getSaveFileName(self, "Guardar parcela", "nueva_parcela.gml", "Archivos GML (*.gml);;Archivos XML (*.xml);;Todos los archivos (*)")
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar parcela", "nueva_parcela.geojson", "Archivos GeoJSON (*.geojson);;Archivos JSON (*.json);;Todos los archivos (*)")

        if ruta:
            
            try:
                with open(ruta, 'w') as file:
                    puntos_poly = []
                    for punto in puntos:
                        puntos_poly.append(punto.values())
                    gdf  = geopandas.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[Polygon(puntos_poly)])
                    gdf.geometry = gdf.geometry.force_2d()
                    gdf["Name"] = ruta.split("/")[-1].split(".")[0]
                    #yaml.dump(puntos, file, default_flow_style=False, allow_unicode=True)
                    #gdf.to_file(ruta, driver="GML")
                    gdf.to_file(ruta, driver="GeoJSON")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Se ha producido un error al guardar: {e}")

class Ros2ConfWindow(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Configuración ROS 2")
        self.rtk_topic = str()

        
        # Layaouts

        main_layaout = QVBoxLayout()
        conf_topic_layaout = QHBoxLayout()
        save_cancel_layaout = QHBoxLayout()

        # Labels

        conf_topic_label = QLabel("Tópic del GPS")

        # ComboBox

        self.conf_topic_combobox = QComboBox()

        # Botones

        self.save_button = QPushButton("Guardar")
        self.cancel_button = QPushButton("Cancelar")
        self.update_button = QPushButton("Actualizar")

        # Composición de layaouts

        conf_topic_layaout.addWidget(conf_topic_label)
        conf_topic_layaout.addWidget(self.conf_topic_combobox)
        conf_topic_layaout.addWidget(self.update_button)

        save_cancel_layaout.addWidget(self.save_button)
        save_cancel_layaout.addWidget(self.cancel_button)

        main_layaout.addLayout(conf_topic_layaout)
        main_layaout.addLayout(save_cancel_layaout)

        self.setLayout(main_layaout)

        self.resize(300, self.height())
        #print(self.width(), self.height())
        self.setModal(True) # Bloquea la ventana principal

        #self.save_button.setEnabled(False)

        self.save_button.clicked.connect(self.save_button_callback)
        self.cancel_button.clicked.connect(self.reject)
        self.update_button.clicked.connect(self.update_button_callback)
        self.conf_topic_combobox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        #self.conf_topic_combobox.currentTextChanged.connect(self.option_changed_callback)

    
    #def option_changed_callback(self, s):
        #self.save_button.setEnabled(True)
    #    print(s)
    #    self.rtk_topic = s
    
    def save_button_callback(self):
        conf["gps_topic"] = self.conf_topic_combobox.currentText() #self.rtk_topic
        self.accept()

    def cancel_button_callback(self):
        self.reject()
    
    def update_button_callback(self):
        node = rclpy.create_node("node_listener")

        rclpy.spin_once(node, timeout_sec=0.5)

        topics = node.get_topic_names_and_types()
        topic_list = list()

        print(topics)

        self.conf_topic_combobox.clear()

        for name, msg_type in topics:
            if conf["msg_type"] in msg_type:
                topic_list.append(f"{name}")

        node.destroy_node()

        self.conf_topic_combobox.addItems(topic_list)

def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

    rclpy.shutdown()


if __name__=="__main__":
    main()
