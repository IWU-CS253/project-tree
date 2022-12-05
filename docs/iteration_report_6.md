# Iteration 6

Original Plan
-------------------
Iteration Week 6 User Stories
- Adding Account Creation and Validation - Zach 
- Associate Individual Trees with Separate Accounts and Personalize Homepage so it is different for each user - Jeff
- Implement Local Tree Support, for guest users - Grace 
- Bug Fixes and Handling Invalid User Data and More compressive Unit Tests - Josh


Completed Work
---------------------
- Account Creation and Validation added (Create Account, Login, and Logout buttons)
- Reformatted Homepage
- Added Delete Tree Button
- Added Guest user system so that users can create trees while logged out without seeing every other tree any other guest has created
- Added automatic generation creation
- Used automatic generation creation to fully implement hierarchical trees
- Many bugfixes, including:
  - Made tree name and character names required
  - Fixed duplicate lines in tree diagram
  - Stopped allowing users to create self relationships or self ancestor relationships causing recursion errors
  - Made home page button work outside of local server


Planned and Unfinished 
----------------------
- More comprehensive unit tests still needed, particularly for create implicits

Difficulties
---------------------
- Getting bootstraps spacing systems, particularly its padding and centering features to work properly in nested divs took experimentation; still not 100% sure why some of it does or does not work
- Understanding and implementing the Flask session system was a bit unintuitive in regards to when it resets and when it remains; caused further issues with unit tests
- Some communication difficulties regarding division of tasks 
- Avoiding recursion errors due to edge cases and testing all of such edge cases proved difficult and continues to be a task
- There appears to be a bug in our hierarchy system where Vis occasionally makes connections that we did not provide between characters on the same level. We intend to look into this further and see if there is a more consistent way to implement the hierarchy.

Adjustments and Changes
---------------------
- Decided to "store" local trees by attaching a random string to them as their "user id" rather than literally storing the on guest users' devics in any way
- Made display hierarchy work by automatically creating generations for characters when the tree is loaded
- Originally planned on having a separate table for the relationship between trees and users, but decided instead to attach users to trees. As a corollary, we no longer intend to allow tree sharing.

Important Take-away
----------------------
- We learned that we need to keep _all possible user behaviors_ in mind, not just user behaviors that match our intentions. 
  - For example, we had not planned for how our site would behave if users attempted to enter nonsensical data, including nameless characters, self relationships, cyclical parent-child relationships etc.
  - We need to be prepared for as many potential user behaviors as possible and make sure that the site continues to work in spite of users doing weird things, and ideally stop them from doing things that would cause issues
  - Most of the time, this can be done by making sure that we check if inputs are valid and avoid letting them get all the way to the database if they aren't by giving the user an error message (not a crash page). Notably, this should be done on the back-end.

Next Two Weeks
---------------------
- Custom colors for types (including custom types) (Jeff)
  - Allow users to select what color will represent what relationship type, including for custom relationship types
  - Show these new types in the legend 
  - Move / redesign the legend to show custom type colors without burying the character list
- Add option to show specific implicit relationships in diagram (Grace)
  - Create a checkmark or other input for each implicit relationship that, when selected, adds that relationship to the graph (WITHOUT adding it to the database)
- Add option to show all of a particular implicit relationship type (e.g. cousins, etc) in diagram (Josh)
  - Create a dropdown list or other menu that lists all implicit relationship types
  - When a type is selected in this list, all implicit relationships of that type should be shown in the graph
- Improve error handling across the board; Fix hierarchical bugs  (Zach)
  - Give an error message (instead of crashing) when the user:
    - Attempts to add a duplicate relationship (same characters _and_ type)
    - Attempts to login with incorrect account information (username or password)
    - Attempts to register with a duplicate username 
  - Fix hierarchy from occasionally switching characters in relationships on the same level 


