import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

/** Dropdown para seleccionar una carrera o agregar una nueva. */
RowLayout {
    spacing: 10

    Label{
        text: "Carrera: "
        font.pointSize: FontSize.big
    }

    ComboBox {
        id: comboBox
        Layout.preferredWidth: 350

        displayText: lista_de_carreras.carreraSeleccionada

        model: ListCarreras {
            id: lista_de_carreras
        }

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
                            if (lista_de_carreras.agregarCarrera(editorNuevaCarrera.text)) {
                                editorNuevaCarrera.clear()
                                popup.close()
                            }
                            editorNuevaCarrera.focus = false
                        }
                    }
                    BotónRedondeadoConTexto {
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
}
