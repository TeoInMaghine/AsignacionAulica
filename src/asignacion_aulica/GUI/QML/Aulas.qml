import QtQuick
import QtQuick.Controls
import Custom

ListView {
    anchors.fill: parent
    spacing: 1

    // TODO: reemplazar esto con una implementación de QAbstractListModel
    model: ListModel {
        ListElement {
            nombre: "B101"
            edificio: "Anasagasti I"
            capacidad: 45
        }
        ListElement {
            nombre: "B102"
            edificio: "Anasagasti I"
            capacidad: 35
        }
        ListElement {
            nombre: "Aula random"
            edificio: "Tacuarí"
            capacidad: 20
        }
    }

    delegate: Row {
        id: delegate
        spacing: 1

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
