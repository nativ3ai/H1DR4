# Bounties and Missions

Bounties let anyone pay for real work: field proof, verification, posts, research, translations, local checks, document gathering, or other lawful tasks.

H1DR4 bounties are useful when the question is concrete:

- hold a sign at a public landmark,
- verify a local incident,
- find an official source,
- document a scam trace,
- collect public proof for a case,
- complete an online or field task.

## Bounty V2 Flow

```mermaid
flowchart TD
  A[Create bounty] --> B[Set deadline and proof requirements]
  B --> C[Get shared Base USDC funding address]
  C --> D[Any wallet sends Base USDC]
  D --> E[Sync and sweep deposits]
  E --> F[Operators submit proof plus payout address]
  F --> G[Creator reviews submission]
  G -->|Accepted| H[Winner can claim]
  G -->|Rejected| I[Funds remain available until deadline]
  I -->|Expired unresolved| J[Funders refund credited deposits]
```

## Proof Submission

Submissions should include:

- proof URL,
- concise description,
- payout ERC address,
- optional source links,
- optional image or media links.

If the payout address is wrong, accepted funds can become claimable by the wrong address. Agents should explicitly repeat the payout address before submitting.

## Review and Dispute

A creator can accept or reject a submission. If a contributor believes a rejection is incorrect, H1DR4 can route the conflict into the dispute/review path exposed by the mission system and documented in the app docs. The goal is to avoid hidden private moderation and keep proof, decision, and payout state inspectable.

## Agent Use

Agents can create bounties through MCP, share funding addresses, monitor deposits, submit proof for users, and prepare claim/refund transaction plans. On-chain calls still require an approved wallet runtime.
