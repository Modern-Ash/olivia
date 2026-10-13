# Cumplimiento y uso responsable

OLIVIA trabaja con datos de personas. Estas reglas no se pueden desactivar desde un perfil.

## Plataformas

- **LinkedIn prohíbe en sus condiciones el scraping y la automatización de mensajes.** OLIVIA solo hace búsquedas de lectura dentro de la sesión del propio usuario, y cada mensaje lo aprueba una persona. No hay envío masivo ni rotación de cuentas.
- Se respetan límites diarios (`channels.max_messages_per_day`) y un tope de mensajes pagos, como los InMail (`channels.max_paid_messages_per_run`).

## Datos personales

- **Solo datos profesionales y públicos**: nombre, cargo, organización, país, publicaciones públicas y direcciones de contacto publicadas por la persona o su organización.
- **Siempre con fuente**: cada lead registra de dónde salió su evidencia (`evidence_url`) y su mail (`email_source_url`). No se adivinan direcciones ni se usan servicios que las buscan.
- **Baja**: cualquier pedido de no recibir más mensajes pasa el lead a `status: opted_out` y nunca se lo vuelve a contactar.
- **Borrado**: ante un pedido de supresión, se elimina el registro del lead.
- Marco de referencia: RGPD (UE/España) y Ley 25.326 de Protección de Datos Personales (Argentina). Cada usuario de OLIVIA es responsable de su base legal para el tratamiento (por ejemplo, interés legítimo en contacto B2B) y de revisarla con su asesor legal.

## Contenido

- Nada inventado: las aperturas citan algo verificable, y el código bloquea las afirmaciones de relación que no se pueden probar.
- No se imita a otras personas ni organizaciones.
