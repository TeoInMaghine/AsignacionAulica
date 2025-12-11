import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

/** Los botones de arriba de la pestaña de materias. */
RowLayout {
    spacing: 15

    BotónRedondeadoConTextoColorUNRN {
        text: "Asignar Aulas"
        onClicked: {
            popupAsignación.open()
            ProxyGestorDeDatos.asignarAulas()
        }
    }
    
    // Por ahora no hacen nada
    BotónRedondeadoConTextoColorUNRN {text: "Exportar Excel"}
    BotónRedondeadoConTextoColorUNRN {text: "Importar Excel"}

    // Popups mostrados al clickear "asignar aulas"
    PopupDuranteAsignación {
        id: popupAsignación
    }
    PopupPostAsignación {
        id: popupPostAsignación
        díasSinAsignar: ""
    }

    Connections {
        target: ProxyGestorDeDatos
        function onFinAsignarAulas(result) {
            popupAsignación.close()
            popupPostAsignación.díasSinAsignar = result
            popupPostAsignación.open()
        }
    }
    
}
