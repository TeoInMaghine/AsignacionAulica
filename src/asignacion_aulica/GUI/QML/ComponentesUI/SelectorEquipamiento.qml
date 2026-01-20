import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Referencias:
// https://forum.qt.io/topic/87306/multiselect-combobox/2
// https://doc.qt.io/qt-6/qtquickcontrols-customize.html#customizing-combobox
ComboBox {
    id: comboBox

    property alias equipamientos: comboBox.model

    displayText: equipamientos.seleccionadosText
    onPressedChanged: if (pressed && !popup.visible) equipamientos.actualizarLista()

    // ComboBox cierra el popup cuando sus items (si heredan de AbstractButton)
    // son activados. Wrappear el delegate es lo que previene que eso pase.
    delegate: Item {
        width: comboBox.width
        height: checkDelegate.height

        function toggle() {
            // checkDelegate.toggle() no triggerea onToggled, lol
            checkDelegate.click()
        }

        CheckDelegate {
            id: checkDelegate
            anchors.fill: parent
            LayoutMirroring.enabled: true

            text: model.nombre
            highlighted: comboBox.highlightedIndex == index || hovered

            checked: model.seleccionado
            onToggled: {
                model.seleccionado = checked
            }
        }
    }

    popup: Popup {
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

                BotónAgregar {
                    Layout.margins: 5
                    Layout.rightMargin: 0
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    onClicked: editorNuevoEquipamiento.accepted()
                }
                TextField {
                    id: editorNuevoEquipamiento
                    Layout.margins: 5
                    Layout.fillWidth: true

                    horizontalAlignment: TextInput.AlignRight
                    placeholderText: "Nuevo"

                    onAccepted: {
                        if (equipamientos.agregarEquipamiento(editorNuevoEquipamiento.text)) {
                            editorNuevoEquipamiento.clear()
                        }
                        editorNuevoEquipamiento.focus = false
                    }
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
