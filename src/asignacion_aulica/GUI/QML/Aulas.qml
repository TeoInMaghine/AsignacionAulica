import QtQuick
import QtQuick.Controls
import Custom

ListView {
    anchors.fill: parent
    spacing: 1

    model: ListAulas { }

    delegate: Row {
        id: delegate
        spacing: 1

        required property var model

        TextField {
            text: model.nombre
            onEditingFinished: {
                model.nombre = text
            }
        }
        TextField {
            text: model.edificio
            onEditingFinished: {
                model.edificio = text
            }
        }
        TextField {
            text: model.capacidad
            onEditingFinished: {
                model.capacidad = parseInt(text)
            }
        }
    }
}
