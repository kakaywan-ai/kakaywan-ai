# API Contract

Status: implemented by the local Python standard-library HTTP server.

## Endpoint

`POST /api/chat`

Request:

```json
{
  "message": "What are the city's watershed protection guidelines?"
}
```

Successful grounded response:

```json
{
  "answer": "Answer based on retrieved approved document passages.",
  "sources": [
    {
      "document": "processed"
    }
  ],
  "grounded": true
}
```

Insufficient evidence response:

```json
{
  "answer": "I couldn't find supporting information for that in the sources currently available. Try rephrasing it or asking about a topic covered by the sources.",
  "sources": [],
  "grounded": false
}
```

## Contract rules

- `message` is required and must not be empty.
- `sources` must refer to actual retrieved passages.
- Return only the source document recorded in the index.
- `grounded` is assigned by backend validation, not copied from model-generated text.
- If the system cannot establish sufficient evidence, return the fallback.
- `mode` is optional and must be a string.
- Invalid JSON returns 400; invalid messages return 422; oversized request bodies return 413; unavailable Ollama or invalid safety-classifier output returns 503.
- Messages are limited by `MAX_MESSAGE_CHARS` (500 by default).
