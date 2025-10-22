import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Custom

// https://forum.qt.io/topic/87306/multiselect-combobox/2
// https://doc.qt.io/qt-6/qtquickcontrols-customize.html#customizing-combobox
ComboBox {
    id: comboBox

    required property var aula

    displayText: equipamientos.seleccionadosText

    model: ListEquipamientos {
        id: equipamientos
        indexAula: aula.index
    }

    // ComboBox cierra el popup cuando sus items (si heredan de AbstractButton)
    // son activados. Wrappear el delegate es lo que previene que eso pase.
    delegate: Item {
        width: parent.width
        height: checkDelegate.height

        required property var model

        function toggle() {
            // checkDelegate.toggle() no triggerea onToggled, lol
            checkDelegate.click()
        }

        CheckDelegate {
            id: checkDelegate
            anchors.fill: parent

            text: model.nombre
            highlighted: comboBox.highlightedIndex == index
            checked: model.seleccionado
            onToggled: {
                 model.seleccionado = checked
            }
        }
    }

    popup: Popup {
        y: comboBox.height - 1
        width: comboBox.width
        height: Math.min(contentItem.implicitHeight, comboBox.Window.height - topMargin - bottomMargin)
        padding: 0

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: comboBox.popup.visible ? comboBox.delegateModel : null
            currentIndex: comboBox.highlightedIndex

            Rectangle {
                width: parent.width
                height: parent.height
                z: 10
                color: "transparent"
                border.color: comboBox.palette.mid
            }

            footer: RowLayout {
                Button {
                    text: "add"
                    onClicked: {
                        equipamientos.insertRow(equipamientos.rowCount())
                    }
                }
            }

            ScrollIndicator.vertical: ScrollIndicator { }
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
