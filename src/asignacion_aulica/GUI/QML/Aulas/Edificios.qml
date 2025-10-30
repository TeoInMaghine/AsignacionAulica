import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
// import ModelosAsignaciónÁulica
// import QML.ComponentesUI

// TODO: reemplazar números mágicos de padding y spacing por propiedades que se
// definan en un solo lugar (igual que hice antes en Aulas básicamente)
ListView {
    anchors.fill: parent
    clip: true

    // model: ListEdificios { id: edificios }
    model: ListModel {
        id: edificios
        ListElement {
            nombre: "Anasagasti I"
            preferir_no_usar: false
        }
        ListElement {
            nombre: "Anasagasti II"
            preferir_no_usar: false
        }
        ListElement {
            nombre: "Tacuarí"
            preferir_no_usar: true
        }
    }

    delegate: ColumnLayout {
        id: editorDeEdificio
        spacing: 5

        required property var model
        required property var index

        property alias edificio : editorDeEdificio.model

        /*
        property var rolesDeHorarios: [
            "horario_lunes",
            "horario_martes",
            "horario_miércoles",
            "horario_jueves",
            "horario_viernes",
            "horario_sábado",
            "horario_domingo"
        ]
        */

        RowLayout {
            Layout.topMargin: 20 // Cumple la función de topPadding

            TextField {
                text: edificio.nombre
                onEditingFinished: {
                    edificio.nombre = text
                }
            }

            // TODO: Agregar horarios

            CheckDelegate {
                LayoutMirroring.enabled: true

                text: "Preferir no usar"
                highlighted: hovered

                checked: edificio.preferir_no_usar
                onToggled: {
                    edificio.preferir_no_usar = checked
                }
            }
        }
        Aulas {
            edificio: parent.edificio
        }
    }

    footer: RowLayout {
        Button {
            Layout.topMargin: 20

            text: "add"
            highlighted: hovered

            onClicked: {
                edificios.insertRow(edificios.rowCount())
            }
        }
    }

    ScrollBar.vertical: ScrollBar { }
    // TODO: esto no funciona todavía: ScrollBar.horizontal: ScrollBar { }
}
