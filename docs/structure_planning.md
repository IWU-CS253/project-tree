Structure Planning
------------------

### Views & Interaction 

#### Home Page
- If logged out:
  - Includes login / create account forms
  - Shows recent public tree links?
- If logged in:
  - Shows sidebar with existing trees
  - Shows Create Tree option

#### Tree Page

- Tree Title
- Pre-Display Formatting:
  - Characters listed as bullet points that can be expanded to show a list of all relationships, categorized by type
  - Relationships can be clicked to view more detail (description; other characters that share the relationship, e.g. other siblings)
  - Putting effort into this design can be useful; can be kept as a separate panel that can be opened / closed in the final product as well; filtering could apply to this as well
- Post-Display Formatting:
  - Display as defined by user-stories; potentially keeping above as a panel.

Basic Database Schema
------------------
***Domains***
- IDs = Autoincrementing INT
- Names = STRING
- Picture = VARBINARY [Or possibly a link elsewhere for larger pictures?]
- Text = STRING

**Table *Character***
- Id: ID
- Name: Name
- Image: Picture
- Description: Text
- **Primary Key** Id

**Table *Relationships***
- Character1 = ID [Not autoincrementing here; references Character]
- Character2 = ID [Not autoincrementing here; references Character]
- Type = Text
- **Primary key** (Character1, Character2) [Enforces uniqueness on relationships to avoid duplicates]
- **Foreign Key** Character1 **references** Character
- **Foreign Key** Character2 **references** Character

### Design Questions

- There are some questions we have to answer on how we want this app to work before we can implement a more complex schema
  - Want kind of data validation limitations do we _want_? In particular, the question of parents comes in. This model allows an infinite number of characters to share the same relationship with infinitely more characters, e.g. Character X having 37 parents. Do we want that?
  - We'll have to make compromises on data validation vs. flexibility here. Flexibility is easier to implement on the database end, but we should also probably consider what display implementation will look like with no restrictions by relationship type.
  - If we do max flexibility like this, perhaps using a "Generation" attribute could help us build the tree when parenthood as a strictly defined relationship type can't be relied on to build a stack?
