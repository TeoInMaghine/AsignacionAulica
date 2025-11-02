import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica
import QML.ComponentesUI

ListView {
    id: view

    required property var edificio
    model: ListAulas { id: aulas; indexEdificio: edificio.index }

    readonly property int padding: 20
    leftMargin: padding
    rightMargin: padding
    topMargin: padding
    bottomMargin: padding
    width: contentItem.childrenRect.width + 2 * padding
    height: contentHeight + 2 * padding

    spacing: headerItem.spacing
    clip: true

    header: Item {
        property alias spacing: headerAulas.spacing
        property alias widthNombre: headerAulas.widthNombre
        property alias widthCapacidad: headerAulas.widthCapacidad
        property alias widthEquipamiento: headerAulas.widthEquipamiento
        height: headerAulas.height + view.spacing
        width: headerAulas.width

        HeaderAulas {
            id: headerAulas
            anchors.top: parent.top
        }
    }

    delegate: RowLayout {
        id: editorDeAula
        spacing: headerItem.spacing

        // Referencia: https://doc.qt.io/qt-6/qtquick-modelviewsdata-modelview.html#models

        required property var model
        required property var index

        property alias aula : editorDeAula.model

        TextField {
            Layout.preferredWidth: headerItem.widthNombre

            text: aula.nombre
            onEditingFinished: {
                aula.nombre = text
            }
        }
        TextField {
            Layout.preferredWidth: headerItem.widthCapacidad

            text: aula.capacidad
            onEditingFinished: {
                aula.capacidad = parseInt(text)
            }
        }

        Item { } // Espacio vacío de 2 * spacing de ancho

        EditorHorariosSemanales { }

        Item { } // Espacio vacío de 2 * spacing de ancho

        SelectorEquipamiento {
            Layout.preferredWidth: headerItem.widthEquipamiento
            aula: parent.aula
        }

        // TODO: crear un componente de botón reusable custom (para que las
        // animaciones y eso sean todas iguales)
        Button {
            text: "borrar"
            highlighted: hovered
            onClicked: {
                aulas.removeRow(index)
            }
        }
    }

    footer: Item {
        height: footerAulas.height + view.spacing
        width: footerAulas.width

        Button {
            id: footerAulas
            anchors.bottom: parent.bottom
            width: headerItem.widthNombre

            text: "añadir"
            highlighted: hovered
            onClicked: {
                aulas.insertRow(aulas.rowCount())
            }
        }
    }

    ScrollBar.vertical: ScrollBar { }
    // TODO: esto no funciona todavía: ScrollBar.horizontal: ScrollBar { }
}
