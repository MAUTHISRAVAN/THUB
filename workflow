{
  "nodes": [
    {
      "parameters": {
        "path": "/faq-query",
        "method": "POST",
        "responseMode": "lastNode",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [200, 300]
    },
    {
      "parameters": {
        "functionCode": "const query = $json[\"query\"] || '';\nreturn [{ json: { query: query.trim() } }];"
      },
      "name": "Clean Query",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [400, 300]
    },
    {
      "parameters": {
        "functionCode": "const { generate_rag_response } = require('/scripts/utils');\nconst response = generate_rag_response($json.query);\nreturn [{ json: response }];"
      },
      "name": "Generate Response",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [600, 300]
    },
    {
      "parameters": {
        "functionCode": "return [{\n  json: {\n    status: 'success',\n    query: $json.query,\n    answer: $json.answer,\n    sources: $json.sources,\n    similarity_scores: $json.similarity_scores\n  }\n}];"
      },
      "name": "Format Response",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [800, 300]
    },
    {
      "parameters": {
        "functionCode": "console.error('Error occurred:', $json);\nreturn [{ json: { error: 'Internal server error' } }];"
      },
      "name": "Error Handler",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [600, 500]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [ [ { "node": "Clean Query", "type": "main", "index": 0 } ] ]
    },
    "Clean Query": {
      "main": [ [ { "node": "Generate Response", "type": "main", "index": 0 } ] ]
    },
    "Generate Response": {
      "main": [ [ { "node": "Format Response", "type": "main", "index": 0 } ], [ { "node": "Error Handler", "type": "main", "index": 0 } ] ]
    }
  }
}
