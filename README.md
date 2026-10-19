# Stratifier

Assesses each entry rule in a countersigned tier ladder, then selects the highest matching tier. No matching rule produces below-ladder.

Published and verified on October 19, 2026.
[Deployed Studio contract](https://explorer-studio.genlayer.com/address/0x1cD21cF74F0A429ca8889538aa75efDCeA5a9566).
[Submission text and links](SUBMISSION.md).

## Material nondeterminism

The contract runs its own `gl.nondet.exec_prompt` judgment inside
`gl.eq_principle.prompt_comparative`. Validators independently repeat that
judgment; the wrapper compares the decision vector and input commitments.
The accepted vector determines the stored outcome. The comparator is LLM-based;
the contract revalidates integer bits, shape and hashes after it returns.
See [GenLayer equivalence documentation](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle).

## Agreed terms and immutable inputs

A submitter fixes tier names, rules and ordering. A distinct reviewer address must countersign the ladder hash before either party can submit the subject once. This enforces on-chain ordering; it cannot prove that either party had never seen the subject off-chain.

Stored input commitments are recomputed before model calls. Model decisions must
be integer 0/1 values with the exact vector length; booleans and floats are rejected.
Every stored settlement, including UNDETERMINED, is terminal. The result hash
binds input commitments, roles, outcome, decision fields and reason.
Pending, undetermined and below-ladder expose assigned_tier=null; get_tier distinguishes below-ladder.

## API

- `open_case(id, reviewer, tier_names, tier_rules)` -> ladder hash; highest tier first
- `countersign(id, ladder_hash)` -> designated reviewer only
- `submit_subject(id, subject)` -> either party, once, after countersigning
- `assign(id)` -> permissionless evaluation
- `get_ladder(id)` -> JSON names, rules, hash, roles and countersign status
- `get_result(id)` -> JSON commitments, gate mask, tier index, reason and result hash
- `get_tier(id)` -> tier name, below-ladder, or empty while unassigned
- `get_outcome(id)` -> 0 pending, 1 ASSIGNED, 2 UNDETERMINED

The constructor takes no arguments. Views return ordinary values or JSON strings.
Storage containers are declared by annotation and never manually constructed.
The runtime dependency is pinned. See [schema.json](schema.json) for the ABI.

## Executed verification

- SDK semantic validation, lint and ABI extraction passed with genvm-linter 0.11.0.
- 10 local regression groups passed, including all eight 3-bit decision vectors,
  countersign permissions, malformed results, commitments and terminal execution.
- Three live Studio cases matched expected results. Deployment, countersigns and
  evaluations finalized with SUCCESS and MAJORITY_AGREE, leader_only=false.
- Creator and counterparty used distinct addresses under the same test operator.

[evidence.json](evidence.json) records exact inputs, source commit/SHA-256,
transactions and stored outputs; [smoke.json](smoke.json) contains the cases.
Run local checks with `python3 sim/check.py`. Local SDK/model behavior is mocked,
including a SHA3-256 hash stub. Live execution uses the actual SDK Keccak256.
ABI validation checks storage and method types; it does not execute GenVM.

## Limits

This is assessment of supplied text. External facts, signatures, authorship and
source authenticity are not verified. Models can agree incorrectly. JSON framing
does not guarantee prompt-injection resistance. A network consensus failure may
leave a transaction unaccepted rather than store UNDETERMINED. There is no
external security audit or guaranteed portal acceptance. Studio is a test
environment; no mainnet deployment or portal submission is claimed.

## Publication correction

A preliminary deployment exposed an unsupported Address.ZERO constant. The
published revision constructs the zero address explicitly. All passing live
cases above use the corrected deployment. Evidence records the superseded address.
