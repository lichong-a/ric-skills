# Design Comparison Contract

## Required Inputs

- Approved visual target and its version.
- Rendered implementation revision.
- Matching viewport dimensions, state, theme, locale, and data.
- Side-by-side image and focused crops for meaningful differences.

## Drift Classes

- `S0`: unusable, unsafe, or fundamentally different result.
- `S1`: missing structure, state, key asset, hierarchy, or responsive behavior.
- `S2`: visible fidelity issue affecting product quality or intent.
- `S3`: minor craft difference without meaningful impact.

## Report

For each difference, identify source location, rendered location, class, evidence, intended behavior, and required remediation. Distinguish intentional approved adaptation from unapproved drift.
