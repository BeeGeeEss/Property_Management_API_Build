# PLANNING DOCUMENTATION

---

The purpose of this document is to present and review the *Entity Relationship Diagram (ERD)*; and to analyse the decision to work with the chosen *database system*.

---

## ERD Review

### Feedback One

#### *Reviewer:* Amelia Gravette

#### *Date:* 2025-12-01

#### *Scope (document checked)*

- `ERD.png`

![Original ERD](/Images/ERD.png)

---

## Log of feedback

| Document checked | When checked | Who checked | Feedback provided | Actions to do based on feedback |
|---|---:|---|---|---|
| `ERD.png` | 2025-12-01 | Amelia Gravette | I like the idea and direction you've chosen for this project! I think it's cool that you're doing something for community housing (instead of something like standard property management) as the addition of the support workers makes this more interesting and dynamic. I can see this being very helpful in a real-world situation. I like how colourful you've made the ERD (it's nice to look at haha), I like the inclusion of the relationship explanations underneath, and I like how well you explained the many-to-many relationship between Support_Workers and Tenants. My feedback for you is: **1. The Relationships table:** What is the "Type" row for? It seems out of place and unnecessary to me, and could probably be removed. **2. `Tenancies` ➔ `Inspections`:** The description for this relationship includes "One inspection can only be conducted per property". Should there be another relationship join between the `Inspections` and `Properties` tables? If not, this should probably be removed. **3. `Tenants` < `Tenancies` > `Properties`:** This is another many-to-many relationship that needs to be documented (currently it's just 2 separate one-to-many relationships listed). **4. The entities:** `Inspections` table has Follow_Up_Notes as a FK, but this attribute isn't listed in any of the other tables. | **1.** Remove the 'type row' - included in error in the original ERD. **2.** Option to join `Inpections` & `Properties` or remove `Inspections`. **3.** Determine if `Tenants` < `Tenancies` > `Properties` needs a junction table to be normalised to 3NF. **4.** Remove 'Fk' included in error in the original ERD. |

---

### Overall Asessment

The chosen topic is applicable to real world settings, and can provide a solid model for community housing organisations. The aesthetic of the ERD is pleasing. And the inclusion of the relationship summary is helpful.

---

### Priority Action List

1. **Remove values included in error** - remove the type row in the relationship table. Remove 'FK' from follow up notes row.
2. **Decide on how to handle Inspections** - create a second draft linking `Inspections` to `Properties` and assess the workload.
3. **Document Many-To-Many Relationships** - Assess if `Tenant/Tenancies/Properties` need to be normalised further.

---

### Verification / Next Steps

- Make changes to ERD and provide updated version to Amelia for further feedback.

---

### Feedback Two

#### *Reviewer:* Sujan Aryal

#### *Date:* 2025-12-03

#### *Scope (document checked)*

- `ERD.png`

![Original ERD](/Images/ERD.png)

---

## Log of feedback

| Document checked | When checked | Who checked | Feedback provided | Actions to do based on feedback |
|---|---:|---|---|---|
| `ERD.png` | 2025-12-03 | Sujan Aryal | Look for attribute names like relationships, add more precise and suitable name like (role instead of relationship). Another thing to consider: ✔️ Right now Organisation is just a attribute in `Support_Workers`. If support workers might work for different organisations or you want to manage organisations properly, create a separate Organisations table (Organisation_ID, Name, Phone, etc.).Then add Organisation_ID as a foreign key in Support_Workers. | 1. Look at attributes and find suitable names. 2. If Organisation is going to be it's own attribute, create an organisation table to link to Support Workers via a foreign key. |

---

### Overall Asessment

Attributes need to be reassed to be more precise and accurate. Organisation may need to be seperated in order for this ERD to be normalised to 3NF.

---

### Priority Action List

1. **Assess Attributes** - go through ERD and make changes where required.
2. **Make a decision about the Organisation Attribute** - Decide if stand alone attributes are necessary - if so, they need to moved to their own table.

---

### Verification / Next Steps

- Make final changes to ERD before submission.

---

### Feedback Three - Second Draft of ERD

#### *Reviewer:* Amelia Gravette

#### *Date:* 2025-12-02

#### *Scope (document checked)*

- `ERD_Second_Draft.png`

![Second Draft of ERD](/Images/ERD_Second_Draft.png)

---

## Log of feedback

| Document checked | When checked | Who checked | Feedback provided | Actions to do based on feedback |
|---|---:|---|---|---|
| `ERD_Second_Draft.png` | 2025-12-02 | Amelia Gravette | I can understand the thought behind splitting `Contacts` out into a separate table. I would personally advise against this because. You've created an ultra-complexity with a triple join here (as in, it's a junction for `Tenants`, `Support_Workers` and `Property_Managers`). While these entities share attributes like Name, Phone, Email, and Role, those attributes belong to distinct individuals. Even though the fields look duplicated, the data isn’t, i.e. a Tenant’s name is not the same as a Support_Worker's name, etc. So it’s appropriate for each table to keep its own contact fields. I like how you've added the `Inspections` table, because that makes sense to include and makes it very real-world. However, if you're pressed for time and not aiming for the HD, you could cut this table out all together because it's an additional join table (trust me, they are a total nightmare to code; at least they were for me haha, and I only did 1), and you've got 3 join tables in this ERD - `Tenant_Support_Workers`, `Tenant_Tenancies` and `Inspections`. So: Keep it in if you want extra marks and want to make this as realistic as possible OR, Remove it if you want to make this less complex; it's really up to you how you'd like to do it. Also with your connectors, you've got the many-to-many's the wrong way for `Tenant_Tenancies`. The "many" side should be on this table so it reads as "one Tenant can have many Tenancies + one Tenancy can have many Tenants". You've honestly done such a good job with this, I can definitely see the ideas you're trying to convey! I just recommend making some tweaks to simplify it | **1.** Make a decision to keep or cut `Inspections`. **2.** Change the relationship direction for `Tenant` and `Tenancies` when connecting to `Tenant_Tenancies`. **3.** Remove `Contacts` table and go back to listing contact details in `Tenants`, `Support_Workers` and `Property_Managers` for ease of coding. |

---

### Overall Asessment

The ERD can be simplified in order to satisfy the assignment criteria - and allow for the database to be coded well.

---

### Priority Action List

1. **Cut Tables** - Cut `Inspections` and `Contacts`.
2. **Simplify Attributes** - Ensure that only necessary attributes remain.
3. **Make Cosmetic Changes** - Ensure relationships are correct, and relationship table correctly documents this.

---

### Verification / Next Steps

- Create third and final draft of ERD incorporating all feedback provided. Keep ERD to 5-7 tables with only one junction table if possible.

---

## Final ERD

---

![ERD Final Draft](/Images/ERD_Final.png)

![Relationship Table Final Draft](/Images/Relationship_Table_Final.png)

## Database System

### PostgreSQL vs. MongoDB

The scope of this assignment determined that we needed to chose between PostgreSQl or MondoDB for the development of a database.

PostgreSQl is an SQL-based object-relational database which organises data into tables (consisting of rows and columns). Tables are linked by the use of keys, which allows complex relationships to be created and updated. Postgres ensures a high level of data integrity and complex querying. Postgres is best used for structured data (Luna, 2025).  

MongoDB is a non-relational document database which stores unstructured data in key-value pairs within JSON documents. MongoDB does not rely on predefined relationships between data groups, instead using a flexible data model. MongoDB is high-performing and great for social media content (AWS, n.d).

### Reason for Final Choice

For this project, given that the data is structured and relies heavily on relationships, I chose to use PostgreSQL.

Some of the reasons for my choice were: 1. The scalability of relational databases - given that this database is likely to expand and continue to evolve. 2. Wanting to have strong data integrity. 3. Wanting to be able to create complex queries. 4. Postgres works well for Customer Relationship Management Systems (CRMs) and that's essentially what this system is (AlgoDaily; Geeks for Geeks, 2025).

#### References

AlgoDaily. (n.d). *PostgreSQL for CRM databases.* <https://algodaily.com/lessons/postgresql-architecture>

AWS. (n.d). *What’s the difference between MongoDB and PostgreSQL?* <http://apastyle.apa.org/style-grammar-guidelines/references/examples/webpage-website-references>

Geeks for Geeks. (2025). *Difference between PostgreSQL and MongoDB.* <https://www.geeksforgeeks.org/postgresql/difference-between-postgresql-and-mongodb/>

Luna, J. C. (2025). *PostgreSQL vs MongoDB: choosing the right database for your data projects.* <https://www.datacamp.com/blog/postgresql-vs-mongodb>
