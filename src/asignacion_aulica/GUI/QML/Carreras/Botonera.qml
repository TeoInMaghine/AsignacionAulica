import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QML.ComponentesUI
import ModelosAsignaciónÁulica

/** Los botones de arriba de la pestaña de materias. */
RowLayout {

    required property int indexCarrera
    property list<string> tiposDeCuatrimestre: ["Primero", "Segundo"]
    signal importaciónHecha

    spacing: 15

    BotónRedondeadoConTextoColorUNRN {
        text: "Asignar Aulas"
        onClicked: {
            popupAsignación.open()
            ProxyGestorDeDatos.asignarAulas()
        }
    }
    
    // Popups mostrados al clickear "asignar aulas"
    PopupDuranteAsignación {
        id: popupAsignación
    }
    PopupConTexto {
        id: popupPostAsignación
        property string mensajeError: ""

        texto: mensajeError.length > 0 ? mensajeError : "Se asignaron aulas a todas las clases."
        textoBotón: "Cerrar"
    }

    Connections {
        target: ProxyGestorDeDatos
        function onFinAsignarAulas(result) {
            popupAsignación.close()
            popupPostAsignación.mensajeError = result
            popupPostAsignación.open()
        }
    }
    
    BotónRedondeadoConTextoColorUNRN {
        text: "Importar Excel"
        onClicked: popupPreImportar.open()
    }
    BotónRedondeadoConTextoColorUNRN {
        text: "Exportar Excel"
        onClicked: popupPreExportar.open()
    }
    BotónRedondeadoConTextoColorUNRN {
        text: "Generar Plantilla Excel"
        onClicked: selectorGenerarPlantilla.open()
    }


    Popup {
        id: popupPreImportar

        modal: true

        topPadding: 20
        bottomPadding: 20
        leftPadding: 60
        rightPadding: 60
        margins: 1

        anchors.centerIn: Overlay.overlay

        ColumnLayout {
            spacing: 20

            Label {
                text: "Importar un Excel puede sobreescribir datos en las carreras existentes."
                font.pointSize: FontSize.medium
                font.bold: true
            }

            RowLayout {
                BotónRedondeadoConTexto{
                    text: "Continuar de todos modos"
                    onClicked: selectorImportarArchivo.open()
                }
                BotónRedondeadoConTexto{
                    text: "Cancelar"
                    onClicked: {
                        popupPreImportar.close()
                    }
                }
            }
        }
    }
    FileDialog {
        id: selectorImportarArchivo

        nameFilters: ["Excel files (*.xlsx)"]

        onAccepted: {
            var result = ProxyGestorDeDatos.importarClasesDeExcel(selectedFile)
            if (result === "") importaciónHecha()

            popupPreImportar.close()
            popupPostImportar.mensajeError = result
            popupPostImportar.open()
        }
    }
    PopupConTexto {
        id: popupPostImportar
        property string mensajeError: ""

        texto: mensajeError.length > 0 ? mensajeError : "Se importaron las clases del excel."
        textoBotón: "Cerrar"
    }

    Popup {
        id: popupPreExportar

        modal: true

        topPadding: 20
        bottomPadding: 20
        leftPadding: 60
        rightPadding: 60
        margins: 1

        anchors.centerIn: Overlay.overlay

        ColumnLayout {
            spacing: 20

            Label {
                text: "Opciones para exportar a Excel"
                font.pointSize: FontSize.medium
                font.bold: true
            }

            RowLayout {
                Layout.alignment: Qt.AlignCenter
                Label {
                    text: "Año:"
                }
                TextFieldConEnter {
                    Layout.preferredWidth: 60

                    text: selectorExportarArchivo.año
                    validator: RegularExpressionValidator {
                        // Permitir números positivos o string vacío
                        regularExpression: /^[0-9]*$/
                    }
                    onEditingFinished: {
                        // Interpretar string vacío como 0
                        selectorExportarArchivo.año = parseInt(text) || 0
                    }
                }

                Item { width: 30 } // Espacio vacío

                Label {
                    text: "Cuatrimestre:"
                }
                ComboBox {
                    model: tiposDeCuatrimestre
                    currentIndex: selectorExportarArchivo.cuatrimestre
                    onActivated: (index) => {
                        selectorExportarArchivo.cuatrimestre = index
                    }
                }
            }

            RowLayout {
                BotónRedondeadoConTexto{
                    text: "Exportar todas las carreras"
                    onClicked: {
                        selectorExportarArchivo.todasLasCarreras = true
                        selectorExportarArchivo.open()
                    }
                }
                BotónRedondeadoConTexto{
                    text: "Exportar la carrera actual"
                    onClicked: {
                        selectorExportarArchivo.todasLasCarreras = false
                        selectorExportarArchivo.open()
                    }
                }
                BotónRedondeadoConTexto{
                    text: "Cancelar"
                    onClicked: {
                        popupPreExportar.close()
                    }
                }
            }
        }
    }

    FileDialog {
        id: selectorExportarArchivo

        fileMode: FileDialog.SaveFile
        nameFilters: ["Excel files (*.xlsx)"]

        // Argumentos para la exportación
        property int año: 2000
        property int cuatrimestre: 0
        property bool todasLasCarreras: false
        
        onAccepted: {
            var result = ProxyGestorDeDatos.exportarClasesAExcel(
                selectedFile,
                indexCarrera,
                año,
                tiposDeCuatrimestre[cuatrimestre],
                todasLasCarreras
            )

            popupPreExportar.close()
            popupPostExportar.mensajeError = result
            popupPostExportar.open()
        }
    }
    PopupConTexto {
        id: popupPostExportar
        property string mensajeError: ""

        texto: mensajeError.length > 0 ? mensajeError : "Se exportaron las clases al excel."
        textoBotón: "Cerrar"
    }

    FileDialog {
        id: selectorGenerarPlantilla

        fileMode: FileDialog.SaveFile
        nameFilters: ["Excel files (*.xlsx)"]
        
        onAccepted: {
            var result = ProxyGestorDeDatos.generarPlantillaExcel(selectedFile)

            popupPostGenerarPlantilla.mensajeError = result
            popupPostGenerarPlantilla.open()
        }
    }
    PopupConTexto {
        id: popupPostGenerarPlantilla
        property string mensajeError: ""

        texto: mensajeError.length > 0 ? mensajeError : "Se generó la plantilla excel."
        textoBotón: "Cerrar"
    }
}
