---
paths:
  - "src/billing/**"
  - "src/__tests__/billing/**"
---

# Billing module rules

Money is stored in cents as integers. Never floats. If you're tempted to divide by 100 for display, use the `formatMoney(cents, currency)` helper in `billing/money.ts`.

Currency codes are ISO 4217 uppercase (`USD`, `INR`, `JPY`). No lowercase, no synonyms.

All mutations go through `billing/api.ts`. Never write to billing tables directly, even in migrations — write a service method and call it.

Prorations are calendar-day based, not second-based. If a customer upgrades at 11:59 PM, they get one day of the new plan, not one minute. Don't change this without a product decision.
