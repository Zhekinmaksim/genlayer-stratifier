# Stratifier verification

Executed on October 19, 2026. Exact inputs and transactions are in evidence.json.

## Local checks

10 groups passed: all eight 3-bit outcomes, countersign authorization and wrong
hashes, countersign prerequisite, terminal settlement, strict vectors, malformed
consensus payloads, independent mock judgments and disagreement, input integrity
before model calls, immutable inputs and result commitment coverage. Hash stubs
use SHA3-256; live execution uses SDK Keccak256. Tests reject Address.ZERO usage.

## Executed live cases

- stratifier-middle-001: expected {"outcome":1,"assigned_tier":1,"gate_mask":6,"below_all":false}; observed match; FINALIZED/SUCCESS/MAJORITY_AGREE.
- stratifier-top-001: expected {"outcome":1,"assigned_tier":0,"gate_mask":7,"below_all":false}; observed match; FINALIZED/SUCCESS/MAJORITY_AGREE.
- stratifier-below-001: expected {"outcome":1,"assigned_tier":null,"gate_mask":0,"below_all":true}; observed match; FINALIZED/SUCCESS/MAJORITY_AGREE.

Each case was created by the creator account and countersigned by a distinct
counterparty before evaluation. Both accounts share one test operator.

## Additional test ideas

Prompt-injection variants and malicious counterparty behavior require broader
adversarial evaluation. No live injection-resistance proof is claimed.
