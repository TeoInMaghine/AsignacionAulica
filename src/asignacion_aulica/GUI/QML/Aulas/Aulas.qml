import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Custom

ListView {
    anchors.fill: parent
    spacing: headerItem.spacing

    model: ListAulas { id: aulas }

    header: HeaderAulas { leftPadding: 20; verticalPadding: 5 }

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

        Repeater {
            id: horarios
            model: rolesDeHorarios

            TextField {
                Layout.preferredWidth: headerItem.widthHorario

                // Este modelData es del Repeater, no del model de ListView...
                required property var modelData

                text: aula[modelData] == undefined ? "NaN" : aula[modelData]
                onEditingFinished: {
                    aula[modelData] = text
                }
            }
        }

        SelectorEquipamiento {
            Layout.preferredWidth: headerItem.widthEquipamiento
            aula: parent.aula
        }

        // TODO: crear un componente de botón reusable custom (para que las
        // animaciones y eso sean todas iguales)
        Button {
            text: "delete"
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
            onClicked: {
                aulas.insertRow(aulas.rowCount())
            }
        }
    }

    ScrollBar.vertical: ScrollBar { }
    // TODO: esto no funciona todavía: ScrollBar.horizontal: ScrollBar { }
}
