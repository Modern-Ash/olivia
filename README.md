# OLIVIA

**O**pportunity · **L**eads · **I**ntelligence · **V**erification · **I**nsight · **A**pproach

OLIVIA es un agente para encontrar y contactar oportunidades de cualquier tipo: clientes, socios, empleo, inversores, licitaciones. Funciona con distintos agentes (Claude, Cursor, Copilot, OpenAI Agents) y con distintas suites de oficina (Google Workspace, Microsoft 365, Airtable, Notion o un CSV).

Nació de una campaña real de ModernAsh en octubre de 2026. En esa campaña se contactaron 23 prospectos: 13 por mail y 10 por mensaje de LinkedIn. Las reglas de este repo vienen de los errores que se encontraron en esa corrida.

## Cómo funciona

```
Perfil de oportunidad (YAML)
        │
        ▼
 1. Discover ──► 2. Qualify ──► 3. Verify ──► 4. Personalize ──► 5. Approve ──► 6. Send ──► 7. Log ──► 8. Follow-up
   (skills)       (skills)      (guardrails)    (render + guardrails)  (humano)      (adapters)  (registry)  (scheduler)
```

| Capa | Qué es | Dónde está |
|---|---|---|
| Skills | Instrucciones por etapa, en formato Agent Skills (`SKILL.md`) | `skills/` |
| Core | Modelo de datos, perfiles, renderizado y guardrails, en Python sin dependencias pesadas | `olivia/` |
| Esquemas | Contratos JSON Schema del perfil y del lead | `schemas/` |
| Perfiles | Un YAML por tipo de búsqueda | `profiles/` |
| Adaptadores | Registro (Sheets, Excel, Airtable, Notion) y mail (Gmail, Graph, SMTP) | *iteración 2* |
| Servidor MCP | Expone el core como herramientas para cualquier agente | *iteración 2* |

## Estado: iteración 1

- [x] Perfil de oportunidad y su esquema
- [x] Modelo de lead (refleja la planilla de outreach)
- [x] Skills: discover, qualify (con verificación de identidad) y personalize
- [x] Guardrails: evidencia obligatoria, trato tú o voseo según el país, destinatario distinto del remitente, identidad verificada, casillas genéricas
- [x] CLI: `validate` y `render`, que generan borradores en `outbox/`
- [ ] Adaptadores de registro y de mail
- [ ] Servidor MCP
- [ ] Seguimiento programado

## Uso rápido

```bash
pip install -e .
olivia validate examples/leads.example.csv --profile profiles/modernash-partners.yaml
olivia render   examples/leads.example.csv --profile profiles/modernash-partners.yaml --out outbox/
```

`render` escribe un borrador `.md` por lead aprobado y un `report.csv` con los leads bloqueados y el motivo. **No envía nada**: el envío siempre pasa por una aprobación humana.

## Principios

1. **Siempre hay una persona en el medio.** OLIVIA propone y la persona aprueba. Nunca se automatiza el envío masivo.
2. **Nada inventado.** Cada apertura cita algo verificable (un post, un artículo, un dato público). Frases como "Sigo de cerca tu trabajo" están bloqueadas si no hay evidencia.
3. **Solo datos públicos y profesionales**, con su fuente registrada y opción de baja. Ver `docs/COMPLIANCE.md`.
4. **Configurable sin tocar código**: un perfil nuevo es un YAML nuevo.

## Licencia

Por definir.
