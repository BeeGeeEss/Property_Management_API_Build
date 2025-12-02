# PLANNING DOCUMENTATION

---

The purpose of this document is to present and review the *Entity Relationship Diagram (ERD)*, and analyse the decision to work with the chosen *database system*.

---

## ERD Review

### Peer Feedback

#### *Reviewer:* Amelia

#### *Date:* 2025-12-01

#### *Scope (document checked)*

- `ERD.png`

![Original ERD](/Images/ERD.png)

---

## Log of feedback

| Document checked | When checked | Who checked | Feedback provided | Actions to do based on feedback |
|---|---:|---|---|---|
| `ERD.png` | 2025-12-01 | Amelia Gravette | I like the idea and direction you've chosen for this project! I think it's cool that you're doing something for community housing (instead of something like standard property management) as the addition of the support workers makes this more interesting and dynamic. I can see this being very helpful in a real-world situation. I like how colourful you've made the ERD (it's nice to look at haha), I like the inclusion of the relationship explanations underneath, and I like how well you explained the many-to-many relationship between Support_Workers and Tenants. My feedback for you is: **1. The Relationships table:** What is the "Type" row for? It seems out of place and unnecessary to me, and could probably be removed. **2. Tenancies ➔ Inspections:** The description for this relationship includes "One inspection can only be conducted per property". Should there be another relationship join between the Inspections and Properties tables? If not, this should probably be removed. **3. Tenants < Tenancies > Properties:** This is another many-to-many relationship that needs to be documented (currently it's just 2 separate one-to-many relationships listed). **4. The entities:** Inspections table has Follow_Up_Notes as a FK, but this attribute isn't listed in any of the other tables. | **1.** Remove the 'type row' - included in error in the original ERD. **2.** Option to join inpections & Properties or remove Inspection. **3.** Determine if Tenants < Tenancies > Properties needs a junction table to be normalised to 3NF. **4.** Remove 'Fk' included in error in the original ERD. |

---

### Overall Asessment

The documentation is accurate, functional, and sufficient for both non‑technical users and developers. Improvements have already been made to documentation - additional changes may just add an extra level of guidance for users.

---

### Priority Action List

1. **Make suggested Code Comment changes** in `app.py` and `test_app.py` and document rationale.
2. **Add troubleshooting guide** in `example_usage.md` so users can easily troubleshoot common, or easy to make, mistakes.

---

### Verification / Next Steps

- Group check of suggested changes - once all changes have been made - before project is provided to external teams for feedback.

---

## Database System

### Chosen Database

#### PostgreSQL

### Reasoning - Alternative Choices

#### MongoDB