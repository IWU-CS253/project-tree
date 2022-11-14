# Iteration 3

Original Plan
---------------------
- Grace was assigned to finish the homepage that Josh started working on, as well as doing additional user interface
work on the show_tree page.
- Jeff was assigned implementing the ability for a user to create and access multiple separate trees from the homepage,
which would be stored in the database as a tree table with relevant information, and with tree_id columns in all other
tables.
- Josh was assigned to work on creating a system to generate relationships that are derived from existing relationships
a tree
- Zach was assigned to implement relationship deletion

Completed Work
---------------------
- Homepage completed with full functionality
- Updated and improved styling and layout for show_tree page and edit_character page 
- The multiple tree functionality
  - Create and name trees from the homepage, and access and edit any tree in the database at present.
- A homepage button on the show_tree page
- Relationship deletion and unit tests completed
- Shift back to id-based DB model instead of natural key based model

Planned and Unfinished
---------------------
- Completed creation of graph for implicit creation, and added implicit siblings and parents—however, did not fully 
finish relationship implicits generation, as it does not yet interact with relationships as they exist in the DB.

Difficulties
---------------------
- Creation of multiple trees involved reworking database and site navigation model, and by extension every single 
function, which proved challenging.
- Creating algorithms is hard.
- Need to be more careful with git merge conflict resolution and with keeping unit tests up-to-date

Adjustments and Changes
---------------------
- Discussed techniques for tree_display; plan to use javascript library Vis
- Returned to an id-based database model
- Considering using implicit relationships graph tools to help with display 

Important Take-aways
---------------------
- Different methods (GET and POST) handle arguments differently (e.g. request.form vs. request.args)
- Manual CSS styling and Bootstrap will conflict if you're not careful

Next Iteration Plan
---------------------
Iteration Week 4 User Stories:

- Finish implicit relationships - Josh
- Tree Display: Characters & Relationships
  - Create functions to pass data from the tree to Vis: Zach 
  - Integrate the Vis into the show_tree page: Grace
  - Use Vis to show characters as nodes and relationships as edges: Grace 
  - Style / edit display to show relevant information about characters (eg. names): Jeff

Our assignments are a bit nebulous at the moment, as we are still not certain what the steps will be for creating and
integrating a Vis display. These will become more concrete when we figure out the exact steps at our meeting on Tuesday.


Future Iteration Plans
---------------------

Iteration Week 5 User Stories
- Tree Display: Relationship Types
- Tree Display: Relationship Legend

Iteration Week 6 User Stories:
- Account Creation
- Account Security and Recovery
- Relationship Type Filtering