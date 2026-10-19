# Stratifier portal submission

## Category

Builder > Intelligent Contracts

## Title

Stratifier

## Contribution date

October 19, 2026 (publication and live verification).

## Description and notes

```text
Stratifier is a GenLayer contract for assigning a subject to a fixed, ordered tier ladder. A distinct reviewer countersigns the names and entry rules before a subject can be submitted. gl.nondet.exec_prompt runs inside gl.eq_principle.prompt_comparative: validators independently assess each rule and compare every gate bit plus subject and ladder hashes. The validated non-deterministic vector determines the highest matching tier, or below-ladder when none match. Inputs are one-time, commitments are rechecked, bit types are strict and settlement is terminal. The result hash binds commitments and all decision fields. Three live Studio cases finalized with SUCCESS and MAJORITY_AGREE: middle tier, top tier and below-ladder; all used two distinct signing accounts. Ten local regression groups and SDK validation pass. This is assessment of supplied text against agreed criteria, without external authentication; model consensus does not guarantee factual correctness.
```

971 characters.

## Primary evidence links

- Source repository: https://github.com/Zhekinmaksim/genlayer-stratifier
- Studio contract: https://explorer-studio.genlayer.com/address/0x1cD21cF74F0A429ca8889538aa75efDCeA5a9566

## Additional evidence

- Exact deployed source: https://github.com/Zhekinmaksim/genlayer-stratifier/blob/55c28ffe7abe9535685b25f9d3ab3a6bf63e4a0c/contract.py
- Deployment: https://explorer-studio.genlayer.com/tx/0xe94709128724af404539023a4930e1d7833aaa17ec17c073ed9a9423b65530f9
- stratifier-middle-001: https://explorer-studio.genlayer.com/tx/0xf1f3c1c3cfe2c44113e9135d7c72af2db2868f3d46f2c7c347ecb621c1b21729
- stratifier-top-001: https://explorer-studio.genlayer.com/tx/0x19e8dd431cf058e18af6a2bd7b996e27686d11ae5c1902799c8ed919904c2a3a
- stratifier-below-001: https://explorer-studio.genlayer.com/tx/0xc29922cc5e42baf34399efe7d0b158ec2fe2c7b6e3063d64e57db878799d0bae
- Inputs, outputs and countersign transactions: https://github.com/Zhekinmaksim/genlayer-stratifier/blob/main/evidence.json

## Verification

10/10 local regression groups and SDK semantic validation passed. Each of the
three live cases matched the expected stored result. Deployment, countersigns
and evaluations are FINALIZED, execution SUCCESS, consensus MAJORITY_AGREE.
Normal consensus was used (leader_only=false).

Two distinct existing accounts were used for creator and counterparty; both are
controlled by the same tester. This verifies role separation. Local tests mock
SDK/model behavior and use SHA3-256 as a hash stub; live execution uses the actual
SDK Keccak256.

## Submission status

Ready for manual form entry. No portal form was created or sent.
Studio is a test environment. Portal acceptance is not guaranteed.
