# Tree User Stories

### Priority System

Factoring dependency into priorities, this uses a 1-5 priority system
- 1: Necessary, first priority
- 2: Necessary
- 3: Not strictly necessary, but nice
- 4: Stretch goal

### Estimate System

Number where 1 =  Estimated time to create character adding system (probably fastest & easiest)


Account Creation
-----------------------
As a user I want to create an account as creator or as a viewer, so I can save my work / save trees I like.

 - Priority: 1
 - Estimate: 3
 - Confirmation:

   1. Create an account with a username and password
   2. Log in with the created account
   3. See previous work (if any)
   4. Create new work bound to this account

Tree Creation
-----------------------
As a creator, I want to create a tree to hold characters and relationships

 - Priority: 1
 - Estimate: 1
 - Confirmation:

   1. Create a tree
   2. Save a tree

Character/Person Addition
-----------------------
As a creator, I want to add characters with names and descriptions, so I can keep track of them.

 - Priority: 1
 - Estimate: 1
 - Confirmation:
   
   1. Add a character (with a name)
   2. Add a description
   3. Check to see that character is present in the tree with the description

Relationship Addition
-----------------------
As a creator, I want to add relationships between my characters  of different types (custom or provided).

 - Priority: 1
 - Estimate: 1
 - Confirmation:

   1. Add a relationship with a predefined type between characters
   2. Check to see the type is as specified
   3. Add a relationship with a custom type between characters
   4. Check to see the type is as specified

Tree Display: Characters
-----------------------
As a user, I want a page to show my characters with their names and pictures on a page 

 - Priority: 1
 - Estimate: 2
 - Confirmation:

   1. Add a character (name, description, picture)
   2. Check if the character appears on the page with their picture
 
Tree Display: Relationships
-----------------------
As a user, I want a page to show the connections between my characters and be able to click on them to see relationship details and attributes

 - Priority: 1
 - Estimate: 4
 - Confirmation:

   1. Add relationships between characters
   2. Check that relationships between characters on the display page

Tree Display: Relationship Types
-----------------------
As a creator, I want the different relationship types to be colored or otherwise indicated by the lines drawn, and I want to pick the color if it is a custom type.

 - Priority: 1
 - Estimate: 2
 - Confirmation:

   1. Add relationships between characters (including types)
   2. Check to see that predefined types show the correct color / line type
   3. Check to see that custom types show the correct color / line type
   4. Check to see that custom type edits show the edited color / line type

Relationship Descriptions
-----------------------
As a creator, I want to add descriptions to my relationships that summarize the nature of the relationships.

 - Priority: 2
 - Estimate: 1
 - Confirmation: 

   1. Create a relationship
   2. Add a description
   3. Check to see that description persists in all display areas


Tree Display: Relationship Legend
-----------------------
As a user, I want to have a legend to show what the different colors and types of lines mean for relationships

 - Priority: 2
 - Estimate: 1
 - Confirmation:

   1. Create relationships
   2. Check to see legend is present and accurate

Tree Display: Responsiveness
-----------------------
As a user, I want the tree display to be responsive to different screen sizes and easy to navigate in those sizes

 - Priority: 2
 - Estimate: 3
 - Confirmation:

   1. Add a simple tree
   2. Check to see display is readable on multiple display sizes via inspect window 

Editing and Deletion
-----------------------
As a creator, I want to be able to edit and delete characters, relationships, and attributes.

 - Priority: 2
 - Estimate: 2
 - Confirmation:

   1. Create characters and relationships
   2. Delete a character
   3. Edit a character's name and description
   4. Delete a relationship
   5. Change a relationship type
   6. Edit a relationship attribute
   7. Check to see if changes persist properly

Account Security & Recovery
-----------------------
As a user, I want to have account security and recovery options.

 - Priority: 3
 - Estimate: 4
 - Confirmation:

   1. Check for data sanitization and make sure SQL injection isn't possible
   2. Reset my password 
   3. Reset my username
 
Character Image Adding
-----------------------
As a creator, I want to be able to upload images to characters

 - Priority: 3
 - Estimate: 4
 - Confirmation: 

   1. Create a character (name and description)
   2. Upload an image to that character
   3. See that the image persists

Relationship Type Filtering
-----------------------
As a user, I want to be able to filter a tree by relationship types to see specific groupings.

 - Priority: 3
 - Estimate: 2
 - Confirmation: 

   1. Add a simple tree
   2. Pick a filter by a certain predefined type
   3. Check that filter is applied to display
   4. Pick a filter by a certain custom type
   5. Check that filter is applied to display

Branch Hiding
-----------------------
As a user, I want to be able to show or hide particular branches or narrow down to relationships with specific people.

 - Priority: 3
 - Estimate: 5
 - Confirmation:

   1. Create a simple tree
   2. Click the button to hide a certain branch
   3. Click it to show it again
   4. Check to ensure that no data has changed

Tree Display: Manipulate Branches
-----------------------
As a user, I want to be able to move tree connections or branches around to format the tree to my liking

 - Priority: 4
 - Estimate: 7
 - Confirmation:

   1. Add a simple tree
   2. Move a branch to a different location to reorient the tree
   3. Change tree orientation 


Tree Display: Image Exporting
-----------------------
As a creator, I want to be able to export my tree display as an image or other filetype 

 - Priority: 4
 - Estimate: 5
 - Confirmation:

   1. Add a simple tree
   2. Export the display type as image

Character Bios
-----------------------
As a creator, I want to add full character bios that can be access from the main tree.

 - Priority: 4
 - Estimate: 2
 - Confirmation:

   1. Create a character 
   2. Create a bio page
   3. Click on character in the tree to ensure the bio page renders properly
 



