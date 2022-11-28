# Iteration 4

Original Plan
---------------------
- Finish implicit relationships - Josh
- Tree Display: Characters & Relationships
  - Create functions to pass data from the tree to Vis: Zach 
  - Integrate the Vis into the show_tree page: Grace
  - Use Vis to show characters as nodes and relationships as edges: Grace 
  - Style / edit display to show relevant information about characters (eg. names): Jeff

Completed Work
---------------------
- Modified show_tree and homepage to have a layout.html and every function/button to have its own separate html page (Jeff)
- Removed some useless code from app.py (Jeff)
- Implicit relationships created for parents / children, siblings, niblings / piblings, cousins, and grandparents (Josh) (we still need to add unit tests for this)
- Fixed all of unit tests (made them work with the new add tree) (Zach)
- Display for characters and relationships functional now (Grace)

Difficulties
---------------------
- Combining Javascript and Jinja for Vis to display the graph was difficult
- Jinja variable system was difficult to use

Adjustments and Changes
---------------------
- homepage and show_tree htmls now extend from layout.html
- every button now has its own html page which is included in the homepage and show_tree
- Grace ended up doing all of the Tree Display because it was difficult to split the work so Zach instead fixed our unit tests and Jeff cleaned up some code in app.py and the htmls

Important Take-aways
---------------------
- Go to Mark if we need help
- Vis is much easier to use than anticipated

Next Iteration Plan
---------------------
Iteration Week 5 User Stories
- Tree Display: Relationship Types: Grace
- Tree Display: Relationship Legend: Jeff
- Fix tree display to only show primary relationships (parents, children, siblings) and avoid sibling loops: Josh
- Make tree display hierarchical: Zach

Future Iteration Plans
---------------------
Iteration Week 6 User Stories:
- Account Creation
- Account Security and Recovery
- Relationship Type Filtering
- Unit Tests for implicit relationships

Iteration Week 7 User Stories:
- Tree Display: Responsiveness
- Branch Hiding
- Tree Display: Manipulate Branches