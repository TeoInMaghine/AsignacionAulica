import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// https://forum.qt.io/topic/87306/multiselect-combobox/2
// https://doc.qt.io/qt-6/qtquickcontrols-customize.html#customizing-combobox
ComboBox {
    id: comboBox

    required property var aula

    displayText: selectedElements.length == 0 ? "Select" : selectedElements.join(",")
    property list<string> selectedElements: []
    function changeSelectedElements(elementName, selected) {
        if (selected) {
            selectedElements.push(elementName)
        }
        else {
            const index = selectedElements.indexOf(elementName)
            if (index > -1) selectedElements.splice(index, 1)
        }
        selectedElements.sort()
    }

    // TODO: reemplazar con un modelo propio
    // TODO: usar aula.equipamiento para saber que está seleccionado, y setear
    // aula.equipamiento para actualizar
    model: ListModel {
        id: equipamientos
        ListElement { name: "One"; selected: false }
        ListElement { name: "Two"; selected: false }
        ListElement { name: "Three"; selected: false }
    }

    // ComboBox cierra el popup cuando sus items (si heredan de AbstractButton)
    // son activados. Wrappear el delegate es lo que previene que eso pase.
    delegate: RowLayout {
        Layout.margins: 10

        CheckDelegate {
            id: checkDelegate
            text: model.name
            highlighted: comboBox.highlightedIndex == index
            checked: model.selected
            onCheckedChanged: {
                if (model.selected != checked) {
                    model.selected = checked
                    comboBox.changeSelectedElements(name, selected)
                    aula.equipamiento = "TODO"
                }
            }
        }
        Button {
            Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
            text: "del"
            onClicked: {
                comboBox.changeSelectedElements(name, false)
                equipamientos.remove(index)
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
                        equipamientos.append({ "name": "Four", "selected": false })
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
                currentItem.checkDelegate.toggle()
                event.accepted = true
            }
        }
    }

    Keys.onReleased: (event) => {
        if (comboBox.popup.visible)
            event.accepted = (event.key === Qt.Key_Space)
    }
}
