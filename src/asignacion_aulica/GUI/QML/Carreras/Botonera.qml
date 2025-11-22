/** Los botones de arriba de la pestaña de materias. */

import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

RowLayout {
    spacing: 10

    // Por ahora no hacen nada
    BotónRedondeadoConTextoColorUNRN {text: "Asignar Aulas"}
    BotónRedondeadoConTextoColorUNRN {text: "Exportar Excel"}
    BotónRedondeadoConTextoColorUNRN {text: "Importar Excel"}
}
