# Iteration 5

Original Plan
-------------------
Iteration Week 5 User Stories
- Tree Display: Relationship Types: Grace
- Tree Display: Relationship Legend: Jeff
- Fix sibling tree display/other configurations (maybe zooming): Josh
- Make tree display hierarchical: Zach

Completed Work
---------------------
- Every Relationship Type is now a different colored line on the display (Grace).
- The Relationship Legend has been added (Jeff). 
- Implicit and Defined Relationships are now separate, implicits are shown in the relationship list but not in the display
which fixes the sibling loop and other related problems (Josh). 
- The tree display is now hierarchical (Zach). 

Planned and Unfinished 
----------------------
Other tree configuration issues, like zooming have not been dealt with yet. 

Difficulties
---------------------
- Trouble knowing when to use Jinja code vs Javascript code within the html files, i.e. show_tree, specifically for hard coding in the relationship types.
- Figuring out how to put colors in with Bootstrap. 

Adjustments and Changes
---------------------
- Made a new table in the schema called colors, to keep track of relationship types and colors. 
- Changed model for handling implicit relationships and the display. Implicits are now listed separately from defined relationships, and are not in the display by default. 
We intend to add the ability for a user to show a given implicit relationship, but by default they will not be displayed to keep the graph cleaner.

Important Take-aways
----------------------
- We learned that some code from Vis is a lot harder to implement than we may think at some time. 
- We learned to pay close attention to what language we might need to use at what times, when multiple languages are being used at the same time. 
- We learned that keeping the big picture with intended user experience in mind is important in informing how we build everything else. 

Next Iteration Plan
---------------------
- Adding Account Creation and Validation - Zach 
- Associate Individual Trees with Separate Accounts and Personalize Homepage so it is different for each user - Jeff
- Implement Local Tree Support, for guest users - Grace 
- Bug Fixes and Handling Invalid User Data and More compressive Unit Tests - Josh

