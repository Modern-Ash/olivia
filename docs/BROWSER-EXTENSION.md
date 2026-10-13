# Extensión de navegador (Chrome + Edge) y Copilot

Estado: propuesta para la iteración 2. La extensión es la **capa de aprobación y de contexto**; el core y los guardrails siguen en Python.

## Arquitectura

```mermaid
flowchart LR
    A["Agente<br/>(M365 Copilot / GitHub Copilot / Claude)"] -- MCP --> S["Servidor MCP OLIVIA<br/>core + guardrails"]
    S <-- "localhost / native messaging" --> E["Extensión MV3<br/>side panel"]
    E -- "captura manual de contexto" --> P["Página abierta por el usuario"]
    S --> R[("Registro<br/>Sheets / Excel / Airtable / Notion / CSV")]
    S --> M["Mail<br/>Gmail / Graph / SMTP"]
    E -- "Aprobar / Rechazar" --> S
```

## Flujo de aprobación

```mermaid
sequenceDiagram
    actor U as Persona
    participant A as Agente
    participant S as Servidor MCP
    participant G as Guardrails
    participant E as Extensión (side panel)
    A->>S: propose_draft(lead)
    S->>G: validar evidencia, trato, identidad
    alt bloqueado
        G-->>S: motivo
        S-->>A: rechazado + motivo
    else aprobado por reglas
        G-->>S: ok
        S->>E: borrador + evidencia
        E->>U: muestra para revisión
        U->>E: Aprobar o Rechazar
        E->>S: decisión
        S-->>A: resultado (envío solo si hubo aprobación)
    end
```

## Chrome y Edge

Edge es Chromium: una sola base de código MV3 sirve para los dos. Cambia solo la publicación.

```mermaid
flowchart TD
    C["Código MV3 único"] --> CH["Chrome Web Store"]
    C --> ED["Edge Add-ons"]
```

## Referencias

Los enlaces no se verificaron desde este entorno; confirmar antes de citarlos en un entregable.

**Extensiones**
- [Chrome: migrar a Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate)
- [Chrome: API Side Panel](https://developer.chrome.com/docs/extensions/reference/api/sidePanel)
- [Chrome: Native messaging](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging)
- [Chrome Web Store: publicar](https://developer.chrome.com/docs/webstore/publish)
- [Edge: extensiones basadas en Chromium](https://learn.microsoft.com/microsoft-edge/extensions-chromium/)
- [Edge Add-ons: publicar](https://learn.microsoft.com/microsoft-edge/extensions/publish/publish-extension)

**Copilot y MCP**
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Copilot Studio: agregar servidores MCP](https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-mcp)
- [VS Code: servidores MCP con Copilot](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [Microsoft Graph](https://learn.microsoft.com/graph/overview)

## Restricciones

- No hay evidencia de que Copilot dentro de Edge acepte extensiones de terceros como agente. La integración con Copilot va por MCP.
- La extensión solo captura contexto por acción manual del usuario en la página. No se automatiza la navegación ni la lectura masiva de LinkedIn. Ver `docs/COMPLIANCE.md`.
- El envío requiere siempre una aprobación humana explícita.
