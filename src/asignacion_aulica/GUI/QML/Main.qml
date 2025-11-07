import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QML.Edificios
import QML.BarraLateral

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

        BarraLateral {
            id: sidebar
        }

        // Mecanismo para cambiar de pestaña
        // TODO: Quizás cambiarlo a TabBar
        // (https://doc.qt.io/qt-6/qml-qtquick-controls-tabbar.html)
        Loader {
            id: tabLoader
            Layout.fillWidth: true
            Layout.fillHeight: true

            sourceComponent: {
                switch(sidebar.pestaña_actual) {
                    case "Edificios": return pestañaEdificios
                    case "Materias": return pestañaMaterias
                    default: return pestañaEdificios
                }
            }
        }
    }

    Component {
        id: pestañaEdificios
        Edificios { }
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
