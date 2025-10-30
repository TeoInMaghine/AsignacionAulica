import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica
import QML.ComponentesUI

ListView {
    // TODO: linkear esto al modelo
    required property var edificio

    Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
    Layout.preferredHeight: contentHeight
    spacing: headerItem.spacing

    /*
    TODO: fix (creo que no se va a poder scrollear horizontalmente sin esto)
    clip: true
    Layout.fillWidth: true // Con esto + clip: true queda raro pero al menos
                           // visible, ni idea qué está pasando
    */

    model: ListAulas { id: aulas; indexEdificio: edificio.index }

    property int widthHorario: 100 // Hardcodeado porque no encontré una forma mejor

    header: HeaderAulas {
        leftPadding: 20
        verticalPadding: 5
        widthHeaderHorario: widthHorario
    }

    delegate: RowLayout {
        id: editorDeAula
        spacing: headerItem.spacing

        // Referencia: https://doc.qt.io/qt-6/qtquick-modelviewsdata-modelview.html#models

        required property var model
        required property var index

        property alias aula : editorDeAula.model

        property var rolesDeHorarios: [
            "horario_lunes",
            "horario_martes",
            "horario_miércoles",
            "horario_jueves",
            "horario_viernes",
            "horario_sábado",
            "horario_domingo"
        ]

        TextField {
            Layout.leftMargin: headerItem.leftPadding // Cumple la función de leftPadding
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

        Repeater {
            model: rolesDeHorarios

            EditorRangoHorario {
                // Este modelData es del Repeater, no del model de ListView...
                required property string modelData
                rolDeHorario: modelData
                Layout.preferredWidth: widthHorario
                Layout.alignment: Qt.AlignCenter
            }
        }

        Item { } // Espacio vacío de 2 * spacing de ancho

        SelectorEquipamiento {
            Layout.preferredWidth: headerItem.widthEquipamiento
            aula: parent.aula
        }

        // TODO: crear un componente de botón reusable custom (para que las
        // animaciones y eso sean todas iguales)
        Button {
            text: "delete"
            highlighted: hovered
            onClicked: {
                aulas.removeRow(index)
            }
        }
    }

    footer: RowLayout {
        Button {
            Layout.topMargin: headerItem.verticalPadding
            Layout.leftMargin: headerItem.leftPadding

            text: "add"
            highlighted: hovered

            onClicked: {
                aulas.insertRow(aulas.rowCount())
            }
        }
    }

    ScrollBar.vertical: ScrollBar { }
    // TODO: esto no funciona todavía: ScrollBar.horizontal: ScrollBar { }
}
