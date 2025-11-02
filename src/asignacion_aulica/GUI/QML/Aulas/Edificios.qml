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
    spacing: 10

    width: parent.width
    contentWidth: contentItem.childrenRect.width + 2 * anchors.margins
    // TODO: esto no funciona completamente al achicar la ventana
    ScrollBar.horizontal: ScrollBar { id: hbar; active: vbar.active }
    ScrollBar.vertical: ScrollBar { id: vbar; active: hbar.active }
    flickableDirection: Flickable.HorizontalAndVerticalFlick

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

        width: view.width

        required property var model
        required property var index

        property alias edificio : editorDeEdificio.model

        RowLayout {
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
            Layout.leftMargin: 20 // "Indentación de anidado"

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

    footer: Item {
        height: footerEdificios.height + view.spacing
        width: footerEdificios.width

        Button {
            id: footerEdificios
            anchors.bottom: parent.bottom
            width: 200

            text: "añadir"
            highlighted: hovered
            onClicked: {
                edificios.insertRow(edificios.rowCount())
            }
        }
    }
}
