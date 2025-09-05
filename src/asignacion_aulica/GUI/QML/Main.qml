import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15

import "."
import "./BarraLateral"

Window {
    id: mainWindow
    visible: true
    visibility: Window.Maximized
    minimumHeight: 300
    minimumWidth: 800
    title: "Asignación Áulica"

    // Layout raíz: barra lateral + contenido de las pestañas
    RowLayout {
        spacing: 0
        anchors.fill: parent

        BarraLateral{
            id: sidebar
        }

        // Mecanismo para cambiar de pestaña
        Loader {
            id: tabLoader
            Layout.fillWidth: true
            Layout.fillHeight: true

            sourceComponent: {
                switch(sidebar.pestaña_actual) {
                    case "Aulas": return pestañaAulas
                    case "Materias": return pestañaMaterias
                    default: return pestañaAulas
                }
            }
        }
    }

    Component {
        id: pestañaAulas
        PruebaTablaSql{}
    }

    Component {
        id: pestañaMaterias
        Rectangle {
            Text {
                anchors.centerIn: parent
                text: "Materias"
                font.pixelSize: 24
            }
        }
    }
}
