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

    model: ListAulasDobles {
        id: aulasDobles
        indexEdificio: edificio.index
    }

    header: Item {
        property alias spacing: headerAulasDobles.spacing
        height: headerAulasDobles.height + view.spacing
        width: headerAulasDobles.width

        HeaderAulasDobles {
            id: headerAulasDobles
            visible: view.count != 0
        }
        Label {
            Layout.margins: 10
            text: "No hay aulas dobles registradas"
            visible: view.count === 0
            font.pointSize: FontSize.medium
        }
    }

    delegate: RowLayout {
        id: editorDeAulaDoble
        spacing: headerItem.spacing

        // Referencia: https://doc.qt.io/qt-6/qtquick-modelviewsdata-modelview.html#models

        required property var model
        required property var index

        property alias aulaDoble : editorDeAulaDoble.model

        SelectorDeAula {
            Layout.preferredWidth: Constantes.width_editor_aula
            indexEdificio: edificio.index
            textoCuandoNoSeleccionado: "Ninguna"

            currentIndex: aulaDoble.index_aula_grande
            onActivated: index => {
                aulaDoble.index_aula_grande = index
            }
        }

        Item { width: 10 } // Espacio vacío, separar aula grande de las chicas

        SelectorDeAula {
            Layout.preferredWidth: Constantes.width_editor_aula
            indexEdificio: edificio.index
            textoCuandoNoSeleccionado: "Ninguna"

            currentIndex: aulaDoble.index_aula_chica_1
            onActivated: index => {
                aulaDoble.index_aula_chica_1 = index
            }
        }
        SelectorDeAula {
            Layout.preferredWidth: Constantes.width_editor_aula
            indexEdificio: edificio.index
            textoCuandoNoSeleccionado: "Ninguna"

            currentIndex: aulaDoble.index_aula_chica_2
            onActivated: index => {
                aulaDoble.index_aula_chica_2 = index
            }
        }

        BotónBorrar {
            onClicked: {
                aulasDobles.removeRow(index)
            }
        }
    }

    footer: Item {
        height: footerAulasDobles.height + view.spacing
        width: footerAulasDobles.width

        BotónRedondeadoConTexto {
            id: footerAulasDobles
            text: "+ Aula Doble"
            anchors.bottom: parent.bottom

            onClicked: {
                aulasDobles.insertRow(aulasDobles.rowCount())
            }
        }
    }
}
