# Roadmap

## Iteración 1 (este commit)

Perfil de oportunidad, modelo de lead, skills de discover, qualify y personalize, guardrails, y una CLI de `validate`/`render` con salida a CSV y borradores.

## Iteración 2: conectar

- **Adaptadores de registro**, todos con la misma interfaz (`read_leads`, `upsert_lead`, `log_touch`): Google Sheets, Excel/Microsoft 365, Airtable, Notion y CSV.
- **Adaptadores de mail**: Gmail, Microsoft Graph y SMTP. Por defecto crean borradores; el envío requiere aprobación explícita.
- **Servidor MCP**: expone `profile_load`, `leads_query`, `leads_upsert`, `draft_render`, `draft_approve` y `touch_log` para cualquier agente compatible con MCP.

## Iteración 3: operar

- Skill `olivia-send`: envía solo lo aprobado, respeta los límites diarios y de mensajes pagos y registra cada envío.
- Skill `olivia-follow-up`: a los `follow_up_after_days` días revisa las respuestas y propone el seguimiento.
- Plugin para Claude Code y Cowork, y una configuración de ejemplo para Paperclip con agentes Scout, Qualifier, Writer y Sender.

## Iteración 4: medir

Tasa de respuesta por segmento, canal, tipo de apertura y registro (tú o voseo), con un panel de resultados.
