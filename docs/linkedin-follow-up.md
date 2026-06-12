# LinkedIn Follow-Up Draft

Earlier this week I mentioned a small risk engineering project around OSCAL findings and risk scenario mapping.

I built a first version of it here:

https://github.com/envokeME/oscal-risk-bridge

```text
OSCAL assessment-results JSON
  -> failed control finding extraction
  -> control-to-risk-scenario mapping
  -> aggregated risk register output
```

The idea is not to replace OSCAL or compliance reporting. It is to explore the layer above control status:

- A failed `AC-2` or `IA-2` control is not just a compliance issue.
- Together, those findings may describe an unauthorized access scenario.
- A failed `SC-7` finding plus `CM-6` drift may point to external attack surface exposure.

The project runs locally with sample OSCAL-formatted assessment results and produces CSV, JSON, and Markdown risk register outputs. I also included an optional AWS pattern using S3 and Lambda, but the core workflow does not require cloud infrastructure.

What I like about this approach is that the mapping logic is explicit. The subjective part of risk translation lives in versioned mapping data, where it can be reviewed and improved, instead of being hidden in a scoring spreadsheet or a black-box automation tool.

This is still early, but it helped me think through a practical bridge:

```text
control findings -> risk scenarios -> risk register
```

The part I want to keep exploring is where the mapping logic should live. My bias is that the subjective risk translation layer should be explicit, reviewable, and version-controlled rather than buried in a spreadsheet or hidden behind a black-box score.
