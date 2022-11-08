
# Iteration 2

Responsibilities (Original)
----------------------
The Original Plan for this iteration was as follows.

Grace was supposed to work on adding an edit button on the app's display for all
characters, as well as adding functionality for each edit button.

Azeem was supposed to work on adding a delete button on the app's display for all
characters, as well as adding functionality for each delete button.

Jeff was supposed to work on implementing basic CSS and styling into our Character Tree Page.

Zach was supposed to work on implementing a function to allow for relationships to be 
inputed by the user for multiple characters. It would do this by both adding relationships into the
database with a relationship table and showing the given relationships on the site's display. 

Josh was supposed to work on creating an extra attribute for relationship descriptions, as well as add a user feature
that allows them to input their relationship descriptions into their own relationships. 

Due to various circumstances (a group member dropping, confusion with assignments (one of the issues made on Github wasn't clear that the delete 
and edit functions were meant to be two separate responsibilities, and there was some miscommunication as well), and just general reassignment)
Our plan's responsibilities had to change. 

New Responsibilities
---------------------------

Grace worked on creating unit tests for the edit and delete character functions, changed the character table in the 
database so that character ids were no longer needed, and helped Jeff fix his delete and edit functions again so
they'd work properly without the character id attribute.

Jeff worked on adding a delete and edit button on the app's display for all
characters, as well as adding functionality for each button. 

Zach worked on adding in a function to: put relationships into the database/relationship table and update the
display to show these relationships.

Josh worked on creating extra attributes in the relationship table for relationship descriptions and types, 
as well as adding a user features that allowed them to input their relationship descriptions/types
into their own relationships. He also worked with Bootstrap to keep all of the edit and delete buttons
attached to each character. 

What We Completed
-------------------
Grace completed creating the various unit tests for the edit and delete character functions and changing the character
table to be used without character ids. She also added in a file for the adapted Flaskr Code's License and put a mention
of authorship in the app.py header. 

Jeff completed adding the delete and edit buttons on the app's display for all
characters, as well as adding functionality for each button. He also used Bootstrap to center the text 
on the tree pages. He and Grace also fixed the delete and edit functions later so they'd be usable without the 
character id attribute. 

Zach completed adding in a function to put relationships into the database/relationship table.

Josh completed the implementation of the relationship attributes types and descriptons, as well as made user features on the GUI
to let users add in these relationship types and descriptions on their own trees. 
He finished putting all of the edit and delete buttons in their proper places with Bootstrap. 
He also started on the Home page, this is still a work in progress.


What We Planned But Didn't Finish
---------------------------------

We did not get around to doing a lot with styling our Character Tree Page using Bootstrap and basic CSS, 
and we also did not get around to actually showing the added relationships on the site's display. 



Difficulties
-------------------

Zach and Grace had some troubles figuring out how to use the Git Branch Methods. Josh had to rework his Unit Test
for his add_character function, as it wasn't working properly this during this iteration. 
There was some general miscommunication about who was assigned to what task, as both Grace and Jeff believed they were
responsible for implementing the editing button (and adding in functionality for it). Which lead to both of them working
on separate versions of the edit button on their own branches. 

Adjustments
-------------------------

We decided to get rid of the character id attribute in the character table, in order to 
store less objects in our character table and to simplify it. We also decided to make implicit 
relationships add themselves automatically. For instance, if someone made a Parent/Child relationship
with character A and B and then made another Parent/Child relationship between B and C then the app
would automatically mark A and C as having a Grandparent/Grandchild relationship. This way the user
has to worry less about having to add in every possible familial relationship themselves. 


One Process We Found Helpful
----------------------------

During this week we realized having the extra in-person meeting with each other really helped us to get back on track 
after the initial miscommunications we were having during the week. Without them we would have not been able to get
back on the same page as easily, which might have caused us even more problems. 

Important Thing We Learned
-------------------------

One important thing from this iteration was that Git is a very useful tool once we figured out how to actually 
get better at it. Being able to use Git's branches especially helped us to be able to work on things concurrently, 
and figuring out how to use Github's pull requests also helped us to make our merges easier as well. 

Next Iteration
------------------------

 - Grace will finish creating the home page/do additional styling of the Individual Tree Pages 
 - Jeff will figure out how to Create Multiple Trees
 - Josh will work on implementing Implicit Relationship Types into the Tree Pages 
 - Zach will work on implementing features to delete relationships

Future Iterations
------------------------------
Iteration Week 4 User Stories
- Tree Display: Characters
- Tree Display: Relationships

Iteration Week 5 User Stories
- Tree Display: Relationship Types
- Tree Display: Relationship Legend
