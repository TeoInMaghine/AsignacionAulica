import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

/** Se encarga de determinar cual es la carrera actual, y de agregar carreras
 * nuevas.
 */
ComboBox {
    id: comboBox

    required property var modelo_de_carreras
    property bool hayCarreraSeleccionada: comboBox.currentIndex >= 0

    model: modelo_de_carreras

    Layout.preferredWidth: 350

    textRole: "nombre"
    displayText: hayCarreraSeleccionada ? currentText : "Ninguna"

    popup: Popup {
        id: popup
        y: comboBox.height - 1
        width: comboBox.width

        // Para que el popup no se clippee con los bordes de la ventana:
        topMargin: comboBox.height
        bottomMargin: comboBox.height
        height: Math.min(contentItem.implicitHeight, comboBox.Window.height - topMargin - bottomMargin)

        padding: 0

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: comboBox.delegateModel
            currentIndex: comboBox.highlightedIndex

            Rectangle {
                width: parent.width
                height: parent.height
                color: "transparent"
                border.color: comboBox.palette.mid
            }

            footer: RowLayout {
                width: parent.width
                spacing: 0

                TextField {
                    id: editorNuevaCarrera
                    Layout.margins: 5
                    Layout.fillWidth: true

                    horizontalAlignment: TextInput.AlignLeft
                    placeholderText: "Nueva"

                    onAccepted: {
                        var índice = modelo_de_carreras.agregarCarrera(editorNuevaCarrera.text)
                        if (índice >= 0) {
                            comboBox.currentIndex = índice
                            editorNuevaCarrera.clear()
                            popup.close()
                        }
                        else{
                            // TODO: reaccionar visualmente al input inválido
                            editorNuevaCarrera.focus = false
                        }
                    }
                }
                BotónAgregar {
                    Layout.margins: 5
                    Layout.leftMargin: 0
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    onClicked: editorNuevaCarrera.accepted()
                }
            }

            ScrollBar.vertical: ScrollBar { }
        }

        background: Item {
            Rectangle {
                anchors.fill: parent
                color: comboBox.palette.window
            }
        }
    }

    // Override space key handling to toggle items when the popup is visible
    Keys.onSpacePressed: (event) => {
        if (comboBox.popup.visible) {
            var currentItem = comboBox.popup.contentItem.currentItem
            if (currentItem) {
                currentItem.toggle()
                event.accepted = true
            }
        }
    }

    Keys.onReleased: (event) => {
        if (comboBox.popup.visible)
            event.accepted = (event.key === Qt.Key_Space)
    }
}
