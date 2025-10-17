import QtQuick
import QtQuick.Controls
import Custom

ListView {
    anchors.fill: parent
    spacing: 1

    model: ListAulas { id: aulas }

    // TODO: no hardcodear tantas cosas (los anchos/espaciado, la cantidad de
    // cajitas de texto y a qué rol corresponden, etc)
    header: Row {
        spacing: 1

        required property var model

        Text {
            text: "Nombre"
            width: 200
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        Text {
            text: "Edificio"
            width: 200
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        Text {
            text: "Capacidad"
            width: 200
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        Button {
            text: "Ordenar"
            onClicked: {
                aulas.ordenar()
            }
        }
    }

    delegate: Row {
        spacing: 1

        required property var model

        TextField {
            text: model.nombre
            onEditingFinished: {
                model.nombre = text
            }
        }
        // TODO: eliminar este field de edificio (se definiría simplemente por
        // el valor en el elemento de la lista padre)
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
        // Quizás crear un componente de botón reusable custom (para que las
        // animaciones y eso sean todas iguales)
        Button {
            text: "delete"
            onClicked: {
                aulas.removeRow(model.index)
            }
        }
    }

    footer: Item {
        Button {
            // No sé si esta es la mejor forma de espaciar el footer
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.margins: 1
            text: "add"
            onClicked: {
                aulas.insertRow(aulas.rowCount())
            }
        }
    }
}
