

COLOR_FONDO = "#E3F2FD"
COLOR_TITULO = "#1565C0"
COLOR_BOTON_PRIMARIO = "#1976D2"
COLOR_BOTON_PELIGRO = "#D32F2F"
COLOR_TEXTO_BOTON = "white"
COLOR_BOTON_SECUNDARIO = "#757575"

USUARIOS = {
    "admin": {"password": "admin123", "rol": "admin"},
    "doctor": {"password": "doc2024", "rol": "doctor"},
    "recepcion": {"password": "rec123", "rol": "recepcion"}
}

ROLES_MODULOS = {
    "admin": ["Pacientes", "Médicos", "Citas", "Historial Médico", "Recetas", "Facturación"],
    "doctor": ["Pacientes", "Médicos", "Citas", "Historial Médico", "Recetas"],
    "recepcion": ["Pacientes", "Médicos", "Citas", "Facturación"]
}

CAMPOS_MODULOS = {
    "Pacientes": ["ID Paciente", "Nombre", "Apellido", "Fecha Nac.", "Género", "Teléfono", "Dirección"],
    "Médicos": ["ID Médico", "Nombre", "Apellido", "Especialidad", "Teléfono"],
    "Citas": ["ID Cita", "ID Paciente", "ID Médico", "Fecha", "Hora", "Motivo", "Estado"],
    "Historial Médico": ["ID Historial", "ID Paciente", "ID Cita", "Diagnóstico", "Tratamiento", "Notas", "Fecha"],
    "Recetas": ["ID Receta", "ID Paciente", "ID Médico", "Medicamento", "Dosis", "Indicaciones", "Fecha Emisión"],
    "Facturación": ["ID Factura", "ID Paciente", "ID Cita", "Concepto", "Monto", "Fecha Emisión", "Estado Pago"]
}
