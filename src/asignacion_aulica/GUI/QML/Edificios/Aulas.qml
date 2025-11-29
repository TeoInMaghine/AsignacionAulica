import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica
import QML.ComponentesUI

ListView {
    id: view

    required property var edificio
    readonly property int padding: 20

    spacing: headerItem.spacing
    leftMargin: padding
    rightMargin: padding
    topMargin: padding
    bottomMargin: padding

    width: contentItem.childrenRect.width + 2 * padding
    height: contentHeight + 2 * padding

    model: ListAulas { id: aulas; indexEdificio: edificio.index }

    header: Item {
        property alias spacing: headerAulas.spacing
        property alias widthNombre: headerAulas.widthNombre
        property alias widthCapacidad: headerAulas.widthCapacidad
        property alias widthEquipamiento: headerAulas.widthEquipamiento
        height: headerAulas.height + view.spacing
        width: headerAulas.width

        HeaderAulas {
            id: headerAulas
            visible: view.count != 0
        }
        Label {
            Layout.margins: 10
            text: "Todavía no hay aulas registradas"
            visible: view.count === 0
            font.pointSize: FontSize.medium
        }
    }

    delegate: RowLayout {
        id: editorDeAula
        spacing: headerItem.spacing

        // Referencia: https://doc.qt.io/qt-6/qtquick-modelviewsdata-modelview.html#models

        required property var model
        required property var index

        property alias aula : editorDeAula.model

        TextFieldConEnter {
            Layout.preferredWidth: headerItem.widthNombre

            text: aula.nombre
            onEditingFinished: {
                aula.nombre = text
            }
        }
        TextFieldConEnter {
            Layout.preferredWidth: headerItem.widthCapacidad

            text: aula.capacidad
            validator: RegularExpressionValidator {
                // Permitir números positivos o string vacío
                regularExpression: /^[0-9]*$/
            }
            onEditingFinished: {
                aula.capacidad = text
            }
        }

        Item { } // Espacio vacío de 2 * spacing de ancho

        SelectorEquipamiento {
            Layout.preferredWidth: headerItem.widthEquipamiento
            edificio: view.edificio
            aula: parent.aula
        }

        Item { } // Espacio vacío de 2 * spacing de ancho

        EditorHorariosSemanalesAula { entidad_padre: edificio; entidad: aula }

        BotónBorrar {
            onClicked: {
                aulas.removeRow(index)
            }
        }
    }

    footer: Item {
        height: footerAulas.height + view.spacing
        width: footerAulas.width

        BotónRedondeadoConTexto {
            id: footerAulas
            text: "+ Aula"
            anchors.bottom: parent.bottom

            onClicked: {
                aulas.insertRow(aulas.rowCount())
            }
        }
    }
}
