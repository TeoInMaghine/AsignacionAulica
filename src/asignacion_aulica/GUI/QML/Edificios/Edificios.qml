import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica
import QML.ComponentesUI

ListView {
    id: view

    anchors.fill: parent
    anchors.margins: 15
    spacing: 10
    clip: true
    
    contentWidth: contentItem.childrenRect.width + 2 * anchors.margins

    model: ListEdificios { id: edificios }

    delegate: ColumnLayout {
        id: editorDeEdificio

        readonly property alias indentaciónDeAnidado: colapsador.width

        required property var model
        required property var index

        property alias edificio : editorDeEdificio.model

        RowLayout {
            id: editorSiempreVisibleDeEdificio
            spacing: 0

            Colapsador {
                id: colapsador
                Component.onCompleted: {
                    editorDetallesDeEdificio.visible = checked
                }
                onClicked: {
                    editorDetallesDeEdificio.visible = checked
                }
            }
            TextField {
                text: edificio.nombre
                onEditingFinished: {
                    edificio.nombre = text
                }
            }
            BotónBorrar {
                Layout.leftMargin: 10
                onClicked: {
                    edificios.removeRow(index)
                }
            }
        }

        ColumnLayout {
            id: editorDetallesDeEdificio
            Layout.leftMargin: indentaciónDeAnidado

            spacing: 10

            CheckDelegate {
                id: checkboxPreferirNoUsar
                text: "Preferir no usar"

                highlighted: hovered

                checked: edificio.preferir_no_usar
                onToggled: {
                    edificio.preferir_no_usar = checked
                }
            }

            Label {
                // Alinear con el checkbox de preferir no usar
                leftPadding: checkboxPreferirNoUsar.leftPadding
                text: "Horarios del edificio:"
            }
            RowLayout { HeaderHorariosSemanales { } }
            RowLayout { EditorHorariosSemanales { } }

            Item {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
                Layout.preferredHeight: editorDeAulas.height
                Layout.preferredWidth: editorDeAulas.width

                Rectangle {
                    id: fondo
                    anchors.fill: parent

                    color: "#F0F0F0"
                    border.width: 1
                    border.color: "lightgray"
                }
                Aulas {
                    id: editorDeAulas
                    edificio: editorDeEdificio.edificio
                }
            }

            // Espacio separador (sólo cuando los edificios están expandidos)
            Item { height: 10 }
        }

    }

    footer: Item {
        height: footerEdificios.height + view.spacing
        width: footerEdificios.width

        BotónAñadir {
            id: footerEdificios
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.topMargin: view.spacing
            anchors.leftMargin: 10
            width: 200

            onClicked: {
                edificios.insertRow(edificios.rowCount())
            }
        }
    }
}
