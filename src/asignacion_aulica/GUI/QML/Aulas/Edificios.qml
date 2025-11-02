import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
// import ModelosAsignaciónÁulica
import QML.ComponentesUI

// TODO: reemplazar números mágicos de padding y spacing por propiedades que se
// definan en un solo lugar (igual que hice antes en Aulas básicamente)
ListView {
    id: view

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

        width: parent.width
        spacing: 5

        required property var model
        required property var index

        property alias edificio : editorDeEdificio.model

        RowLayout {
            Layout.topMargin: 10 // Cumple la función de topPadding

            TextField {
                text: edificio.nombre
                onEditingFinished: {
                    edificio.nombre = text
                }
            }

            EditorHorariosSemanales { }

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
        Item {
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
            Layout.preferredHeight: editorDeAula.height
            Layout.preferredWidth: editorDeAula.width
            Layout.leftMargin: 10

            Rectangle {
                id: background
                anchors.fill: parent

                color: "#F0F0F0"
                border.width: 1
                border.color: "lightgray"
            }
            Aulas {
                id: editorDeAula
                edificio: editorDeEdificio.edificio
            }
        }
    }

    footer: RowLayout {
        Button {
            Layout.topMargin: 10
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
