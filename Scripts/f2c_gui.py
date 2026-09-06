import sys
import time
import fields2cover as f2c

from PyQt6.QtWidgets import QApplication, QLineEdit, QCheckBox, QSlider, QMainWindow, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QDialog, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction, QColor, QIntValidator, QPixmap
from PyQt6.QtCore import Qt
from math import pi,radians
import yaml

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.titulo = "Editor de pasadas"
        self.setWindowTitle(self.titulo)

        self.tam_imagen = 500

        self.pasadas_dict =  {"boustrophedon": "Boustrophedon",
                            "snake": "Snake",
                            "spiral": "Spiral"}
        
        self.giros_dict = {"dubins": "Dubins Curves", 
                            "dubins_cc": "Dubins curves with Continuous curvature", 
                            "reeds": "Reeds-Shepp",
                            "reeds_cc": "Reeds-Shepp curves with Continuous curvature"}
        
        self.giros_linde_dict = {"fuera": "Giros por fuera",
                                "dentro": "Giros por dentro"}

        self.ancho_robot = 0.7

        self.ruta_terreno = None
        self.ruta_conf_apero = None

        self.angulo_pasdas_radianes = 0.0
        self.angulo_pasadas_checkbox_currentstate = False

        self.apero_conf = dict()

        #F2C variables

        self.campo = f2c.Fields()
        self.orig_campo = None
        self.robot = f2c.Robot(self.ancho_robot)
        self.cost_hl = f2c.HG_Const_gen()
        self.no_hl = None
        self.bf = f2c.SG_BruteForce()
        self.giros_swaths = None # Giros
        self.pasadas_planner = None # Tipo de pasadas
        self.path_planner = f2c.PP_PathPlanning()

        self.pasadas_f2c_dict =  {"boustrophedon": f2c.RP_Boustrophedon,
                            "snake": f2c.RP_Snake,
                            "spiral": f2c.RP_Spiral}
        
        self.giros_f2c_dict = {"dubins": f2c.PP_DubinsCurves, 
                            "dubins_cc": f2c.PP_DubinsCurvesCC, 
                            "reeds": f2c.PP_ReedsSheppCurves,
                            "reeds_cc": f2c.PP_ReedsSheppCurvesHC}
        self.path_gps = None

        # Layouts

        main_layout = QVBoxLayout()
        central_layout = QHBoxLayout()
        seleccion_terreno_layout = QHBoxLayout()
        seleccion_conf_apero_layout = QHBoxLayout()
        tipo_de_giro_layout = QHBoxLayout()
        giros_linde_layout = QHBoxLayout()
        tipo_de_pasadas_layout = QHBoxLayout()
        orden_de_pasadas_layout = QHBoxLayout()
        angulo_pasadas_layout = QHBoxLayout()
        labels_layout = QVBoxLayout()
        widgets_layout = QVBoxLayout()
        end_layout = QHBoxLayout()

        # Labels

        title_label = QLabel(self.titulo)
        title_font = title_label.font()
        title_font.setPointSize(25)
        title_label.setFont(title_font)

        seleccion_terreno_label = QLabel("Fichero de terreno")
        seleccion_conf_apero_label = QLabel("Fichero de configuración del apero")
        self.giros_linde_label = QLabel("Por donde hacer los giros")
        self.seleccion_terreno_label_abierto = QLabel(" ")
        self.seleccion_apero_label_abierto = QLabel(" ")
        tipo_de_giro_label = QLabel("Tipo de giro")
        tipo_de_pasadas_label = QLabel("Tipo de pasadas")
        orden_de_pasadas_label = QLabel("Orden de pasadas (Solo para Spiral)")
        angulo_pasadas_label = QLabel("Ángulo de las pasadas")

        # Imagen

        self.imagen_pasadas_label = QLabel()
        pixmap = QPixmap(self.tam_imagen, self.tam_imagen)
        pixmap.fill(QColor("lightgray"))
        self.imagen_pasadas_label.setPixmap(pixmap)
        

        # Widgets

        seleccion_terreno_button = QPushButton("Abrir fichero de terreno")
        seleccion_conf_apero_button = QPushButton("Abrir configuración del apero")

        self.tipo_giro_combobox = QComboBox()
        self.tipo_giro_combobox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.tipo_giro_combobox.addItems(self.giros_dict.values())
        self.tipo_giro_combobox.setDisabled(True)

        self.giro_linde_combobox = QComboBox()
        self.giro_linde_combobox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.giro_linde_combobox.addItems(self.giros_linde_dict.values())

        self.tipo_de_pasadas_combobox = QComboBox()
        self.tipo_de_pasadas_combobox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.tipo_de_pasadas_combobox.addItems(self.pasadas_dict.values())
        self.tipo_de_pasadas_combobox.setDisabled(True)

        self.orden_de_pasadas_text = QLineEdit()
        self.orden_de_pasadas_text.setValidator(QIntValidator(1, 999, self))
        self.orden_de_pasadas_text.setDisabled(True)

        self.angulo_pasadas_checkbox = QCheckBox("Ángulo óptimo")
        self.angulo_pasadas_slider = QSlider(Qt.Orientation.Horizontal)
        self.angulo_pasadas_slider.setRange(0, 90)
        self.angulo_pasadas_slider.setSingleStep(5)
        self.angulo_pasadas_valor_label = QLabel("0")

        self.save_button = QPushButton("Guardar trayectorias")
        self.save_button.setDisabled(True)
        visualizer_button = QPushButton("Generar y Visualizar")


        # Composición de la ventana
        labels_layout.addWidget(seleccion_terreno_label)

        #seleccion_terreno_layout.addWidget(seleccion_terreno_label)
        seleccion_terreno_layout.addWidget(seleccion_terreno_button)
        seleccion_terreno_layout.addWidget(self.seleccion_terreno_label_abierto)

        widgets_layout.addLayout(seleccion_terreno_layout)

        #seleccion_conf_apero_layout.addWidget(seleccion_conf_apero_label)
        labels_layout.addWidget(seleccion_conf_apero_label)
        seleccion_conf_apero_layout.addWidget(seleccion_conf_apero_button)
        seleccion_conf_apero_layout.addWidget(self.seleccion_apero_label_abierto)
        widgets_layout.addLayout(seleccion_conf_apero_layout)

        labels_layout.addWidget(tipo_de_giro_label)
        #tipo_de_giro_layout.addWidget(tipo_de_giro_label)
        tipo_de_giro_layout.addWidget(self.tipo_giro_combobox)
        widgets_layout.addLayout(tipo_de_giro_layout)

        labels_layout.addWidget(self.giros_linde_label)
        giros_linde_layout.addWidget(self.giro_linde_combobox)
        widgets_layout.addLayout(giros_linde_layout)

        labels_layout.addWidget(tipo_de_pasadas_label)
        #tipo_de_pasadas_layout.addWidget(tipo_de_pasadas_label)
        tipo_de_pasadas_layout.addWidget(self.tipo_de_pasadas_combobox)
        widgets_layout.addLayout(tipo_de_pasadas_layout)

        labels_layout.addWidget(orden_de_pasadas_label)
        #orden_de_pasadas_layout.addWidget(orden_de_pasadas_label)
        orden_de_pasadas_layout.addWidget(self.orden_de_pasadas_text)
        widgets_layout.addLayout(orden_de_pasadas_layout)

        labels_layout.addWidget(angulo_pasadas_label)
        #angulo_pasadas_layout.addWidget(angulo_pasadas_label)
        angulo_pasadas_layout.addWidget(self.angulo_pasadas_checkbox)
        angulo_pasadas_layout.addWidget(self.angulo_pasadas_slider)
        angulo_pasadas_layout.addWidget(self.angulo_pasadas_valor_label)
        widgets_layout.addLayout(angulo_pasadas_layout)

        #central_layout.addLayout(seleccion_terreno_layout)
        #central_layout.addLayout(seleccion_conf_apero_layout)
        #central_layout.addLayout(tipo_de_giro_layout)
        #central_layout.addLayout(tipo_de_pasadas_layout)
        #central_layout.addLayout(orden_de_pasadas_layout)
        #central_layout.addLayout(angulo_pasadas_layout)

        central_layout.addLayout(labels_layout)
        central_layout.addLayout(widgets_layout)
        #central_layout.addWidget(self.imagen_pasadas_label)

        end_layout.addWidget(visualizer_button)
        end_layout.addWidget(self.save_button)

        main_layout.addWidget(title_label)
        main_layout.addLayout(central_layout)
        main_layout.addWidget(self.imagen_pasadas_label)
        main_layout.addLayout(end_layout)

        # Callbacks

        seleccion_terreno_button.clicked.connect(self.seleccion_terreno_callback)
        seleccion_conf_apero_button.clicked.connect(self.seleccion_apero_callback)

        self.angulo_pasadas_slider.valueChanged.connect(self.angulo_pasadas_slider_value_changed)
        self.angulo_pasadas_checkbox.stateChanged.connect(self.angulo_pasadas_checkbox_state)

        self.tipo_de_pasadas_combobox.currentTextChanged.connect(self.tipo_de_pasadas_callback)
        self.orden_de_pasadas_text.textChanged.connect(self.orden_text_callback)

        visualizer_button.clicked.connect(self.gen_cover)
        self.save_button.clicked.connect(self.save_button_callback)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
    
    def tipo_de_pasadas_callback(self, s):
        if s == "Spiral":
            self.orden_de_pasadas_text.setDisabled(False)
        else:
            self.orden_de_pasadas_text.clear()
            self.orden_de_pasadas_text.setDisabled(True)
    
    def seleccion_terreno_callback(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccione un terreno", filter="Archivos GeoJSON (*.geojson);;Archivos JSON (*.json);;Todos los archivos (*)")
        self.seleccion_terreno_label_abierto.setText(ruta)
        self.ruta_terreno = ruta
    
    def seleccion_apero_callback(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccione un terreno", filter="Archivos YAML (*.yaml);;Todos los archivos (*)")
        self.seleccion_apero_label_abierto.setText(ruta)
        self.ruta_conf_apero = ruta
        self.open_apero_yaml(ruta)
    
    def angulo_pasadas_slider_value_changed(self, i):
        self.angulo_pasdas_radianes = radians(i)
        self.angulo_pasadas_valor_label.setText(str(i))
    
    def angulo_pasadas_checkbox_state(self, s):
        if s == Qt.CheckState.Checked.value:
            self.angulo_pasadas_slider.setDisabled(True)
            self.angulo_pasadas_checkbox_currentstate = True
        else:
            self.angulo_pasadas_slider.setDisabled(False)
            self.angulo_pasadas_checkbox_currentstate = False

    def check_min_turning_radius(self, apero_conf):
        if not "MinTurningRadius" in apero_conf.keys():
                self.robot.setMinTurningRadius(0.0)
        else:
            self.robot.setMinTurningRadius(apero_conf["MinTurningRadius"])

    def check_RoutePlanner(self, apero_conf):

        self.tipo_de_pasadas_combobox.setDisabled(True)
        self.orden_de_pasadas_text.setDisabled(True)

        if (not "RoutePlanner" in apero_conf.keys()) or apero_conf["RoutePlanner"] == "free":
            self.tipo_de_pasadas_combobox.setDisabled(False)
        elif apero_conf["RoutePlanner"] in self.pasadas_dict.keys():
            self.tipo_de_pasadas_combobox.setCurrentText(self.pasadas_dict[apero_conf["RoutePlanner"]])

            if apero_conf["RoutePlanner"] == "spiral":
                self.orden_de_pasadas_text.setDisabled(False)
        else:
            self.tipo_de_pasadas_combobox.setDisabled(False)
            QMessageBox.information(self, "RoutePlanner desconocido","RoutePlanner desconocido. Escoja uno válido del formaulario.")

    def check_GyroPlanner(self, apero_conf):

        self.tipo_giro_combobox.setDisabled(True)

        if (not "GyroPlanner" in apero_conf.keys()) or apero_conf["GyroPlanner"] == "free":
            self.tipo_giro_combobox.setDisabled(False)
        elif apero_conf["GyroPlanner"] in self.giros_dict.keys():
            self.tipo_giro_combobox.setCurrentText(self.giros_dict[apero_conf["GyroPlanner"]])
        else:
            self.tipo_giro_combobox.setDisabled(False)
            QMessageBox.information(self, "GyroPlanner desconocido","GyroPlanner desconocido. Escoja uno válido del formaulario.")
    
    def set_f2c_pasadas_planner(self):
        for k in self.pasadas_dict.keys():
            if self.tipo_de_pasadas_combobox.currentText() == self.pasadas_dict[k] and not (k == "spiral"):
                self.pasadas_planner = self.pasadas_f2c_dict[k]()
    
    def set_f2c_giros_swaths(self):
        for k in self.giros_dict.keys():
            if self.tipo_giro_combobox.currentText() == self.giros_dict[k]:
                self.giros_swaths = self.giros_f2c_dict[k]()
    
    def orden_text_callback(self, t):
        self.pasadas_planner = self.pasadas_f2c_dict["spiral"](int(t))

    def open_apero_yaml(self, ruta):
        
        with open(ruta, "r") as file:
            try:
                apero_conf = yaml.safe_load(file)["f2c_conf"]
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al abrir el archivo de configuración: {e}")
        
        if not "CovWidth" in apero_conf.keys():
            QMessageBox.critical(self, "Parámetro crítico faltante", "El archivo de configuración debe contener al menos el parámetro CovWidth")
        else:
            self.robot.setCovWidth(apero_conf["CovWidth"])

            self.check_min_turning_radius(apero_conf)
            self.check_RoutePlanner(apero_conf)
            self.check_GyroPlanner(apero_conf)
    

    def gen_cover(self):
        if self.ruta_conf_apero is None or self.ruta_terreno is None:
            QMessageBox.information(self, "Faltan archivos", "Compruebe que ha importado correctamente los archivos del terreno y del apero")
            return
        try:
            f2c.Parser().importJson(self.ruta_terreno, self.campo)
            campo = self.campo[0]
            orig_campo = campo.clone()

            f2c.Transform.transformToUTM(campo)

            if self.giro_linde_combobox.currentText() == self.giros_linde_dict["dentro"]:
                no_hl = self.cost_hl.generateHeadlands(campo.getField(), self.robot.getMinTurningRadius()*2.0)
            elif self.giro_linde_combobox.currentText() == self.giros_linde_dict["fuera"]:
                no_hl = self.cost_hl.generateHeadlands(campo.getField(), 0.0)
            else:
                QMessageBox.critical(self, "Error", f"Valor en '{self.giros_linde_label.text()}' no valido")
                return 
            
            if self.pasadas_planner is None:
                self.set_f2c_pasadas_planner()
            
            if self.angulo_pasadas_checkbox_currentstate:
                n_swath = f2c.OBJ_NSwath()
                swaths = self.bf.generateBestSwaths(n_swath, self.robot.getCovWidth(), no_hl.getGeometry(0))
            else:
                swaths = self.bf.generateSwaths(self.angulo_pasdas_radianes, self.robot.getCovWidth(), no_hl.getGeometry(0))
            
            swaths = self.pasadas_planner.genSortedSwaths(swaths)

            self.set_f2c_giros_swaths()

            path = self.path_planner.planPath(self.robot, swaths, self.giros_swaths)

            path.discretizeSwath(1.0)
            #path.populate(200)

            self.path_gps = f2c.Transform.transformToPrevCRS(path, campo)
        except Exception as e:
            QMessageBox.critical(self, "Error", "Configuración no válida")
            return
        
        try:
            f2c.Visualizer.figure()
            f2c.Visualizer.plot(orig_campo.getCellsAbsPosition())
            #f2c.Visualizer.plot(no_hl_gps)
            #f2c.Visualizer.plot(swaths_gps)
            f2c.Visualizer.plot(self.path_gps)
            f2c.Visualizer.save(f"pasadas_{campo.getId()}.png")
            time.sleep(0.5)
            pixmap = QPixmap(f"pasadas_{campo.getId()}.png")
            pixmap = pixmap.scaled(self.tam_imagen, self.tam_imagen)

            self.imagen_pasadas_label.setPixmap(pixmap)

            self.save_button.setDisabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar la visualización: {e}")
        #f2c.Visualizer.show()
    

    def save_button_callback(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar ruta", f"ruta_{self.campo[0].getId()}.csv", "Archivos CSV (*.csv);;Todos los archivos (*)")
        self.path_gps.saveToFile(ruta)
        


        

def main(args=None):
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__=="__main__":
    main()
        

