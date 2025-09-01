import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15

import "./BarraLateral"

Window {
    id: mainWindow
    visible: true
    visibility: Window.Maximized
    minimumHeight: 500
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
                    case "Edificios": return pestañaEdificios
                    case "Aulas": return pestañaAulas
                    case "Carreras": return pestañaCarreras
                    case "Materias": return pestañaMaterias
                    case "Horarios": return pestañaHorarios
                    default: return pestañaEdificios
                }
            }
        }
    }

    // Acá debería ir el contenido de cada pestaña
    Component {
        id: pestañaEdificios
        Rectangle {
            Text {
                anchors.centerIn: parent
                text: "Edificios"
                font.pixelSize: 24
            }
        }
    }

    Component {
        id: pestañaAulas
        Rectangle {
            Text {
                anchors.centerIn: parent
                text: "Aulas"
                font.pixelSize: 24
            }
        }
    }

    Component {
        id: pestañaCarreras
        Rectangle {
            Text {
                anchors.centerIn: parent
                text: "Carreras"
                font.pixelSize: 24
            }
        }
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

    Component {
        id: pestañaHorarios
        Rectangle {
            Text {
                anchors.centerIn: parent
                text: "Horarios"
                font.pixelSize: 24
            }
        }
    }
}
