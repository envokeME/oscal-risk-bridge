# OSCAL Format Notes

The demo input uses the OSCAL `assessment-results` model and is authored against OSCAL version `1.1.2`.

## Validation Checks

The CLI can run a lightweight structural validation pass before generating outputs:

```powershell
oscal-risk-bridge `
  --validate-oscal `
  --findings examples/oscal-assessment-results.json `
  --mapping mappings/risk-scenarios.json `
  --out demo-output/risk-register.csv
```

The validator checks the parts of OSCAL that matter for this prototype:

- `assessment-results` root object exists.
- Required metadata fields exist: `title`, `last-modified`, `version`, and `oscal-version`.
- Required `import-ap.href` exists.
- Root, result, and finding UUIDs are valid UUIDs.
- Each result includes `title`, `description`, `start`, and `reviewed-controls`.
- Findings include `title`, `description`, `target.type`, `target.target-id`, and `status.state`.
- Finding objective status uses OSCAL states: `satisfied` or `not-satisfied`.
- Implementation status uses OSCAL-defined states such as `implemented`, `partial`, or `planned`.
- Custom GRC properties such as `severity` use a custom namespace.

## Important Modeling Choice

The sample stores finding severity as a custom OSCAL property:

```json
{
  "name": "severity",
  "ns": "https://battlerisk.example/ns/oscal-risk-bridge",
  "value": "high"
}
```

That namespace matters. When an OSCAL property omits `ns`, OSCAL treats it as part of the OSCAL namespace, where custom names such as `severity` may not be valid for the containing object.

## Scope

This validator is a project-level guardrail, not a full OSCAL metaschema validator. For production use, the next step would be validating against the official OSCAL JSON schema or metaschema for the declared `oscal-version`.
