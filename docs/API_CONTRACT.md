# API Contract — Initial Proposal

Status: proposed. Team Leader, Karl, and Isaac must agree on the final schema before implementation.

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
      "document": "Document title",
      "page": 5,
      "section": "Section title"
    }
  ],
  "grounded": true
}
```

Insufficient evidence response:

```json
{
  "answer": "Information not available in the current approved records.",
  "sources": [],
  "grounded": false
}
```

## Contract rules

- `message` is required and must not be empty.
- `sources` must refer to actual retrieved passages.
- Do not invent page numbers, document titles, or URLs.
- `grounded` is assigned by backend validation, not copied from model-generated text.
- If the system cannot establish sufficient evidence, return the fallback.
- Agree on HTTP status codes, error schema, maximum message length, and optional language/mode fields before frontend integration.
