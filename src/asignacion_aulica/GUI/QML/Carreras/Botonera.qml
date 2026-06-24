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
        text: "Exportar Excel"
        onClicked: selectorExportarArchivo.open()
    }
    BotónRedondeadoConTextoColorUNRN {
        text: "Importar Excel"
        onClicked: selectorImportarArchivo.open()
    }

    FileDialog {
        id: selectorImportarArchivo
        onAccepted: {
            // FIXME: Falla importar un excel que se acaba de exportar porque no
            // acepta celdas de año o carrera vacíos. Preguntar en una ventana
            // de diálogo qué año y cuatrimestre poner, y también aceptar que
            // estén esas celdas vacías.
            var result = ProxyGestorDeDatos.importarClasesAExcel(selectedFile)
            popupPostImportar.mensajeError = result
            popupPostImportar.open()
            // FIXME: resetear indexCarrera o la lista de materias o el modelo
            // si no había carreras, sino se queda vacío.
        }
    }
    FileDialog {
        id: selectorExportarArchivo

        fileMode: FileDialog.SaveFile
        nameFilters: ["Excel files (*.xlsx)"]
        
        onAccepted: {
            var result = ProxyGestorDeDatos.exportarClasesAExcel(
                selectedFile,
                // TODO: Tener un diálogo donde te pregunta si solo
                // guardar la carrera actual o todas las carreras.
                indexCarrera
            )
            popupPostExportar.mensajeError = result
            popupPostExportar.open()
        }
    }

    // TODO: Tener mensajes de éxito con más información
    PopupConTexto {
        id: popupPostImportar
        property string mensajeError: ""

        texto: mensajeError.length > 0 ? mensajeError : "Se importaron las clases del excel."
        textoBotón: "Cerrar"
    }
    PopupConTexto {
        id: popupPostExportar
        property string mensajeError: ""

        texto: mensajeError.length > 0 ? mensajeError : "Se exportaron las clases al excel."
        textoBotón: "Cerrar"
    }
}
