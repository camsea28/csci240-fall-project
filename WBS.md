## Work Breakdown Structure
#### Media Gear Tracker for Events

### Tasks

### 1. CRUD functionality for one table
   - No dependencies, can be started right away.
   - Effort: Medium (2–3 days)
   - Subtasks:
     - Create logic for Create, Read, Update, Delete operations
     - Test each operation using sample data
  > Partially complete!
  > Still to complete - Update/Delete operations, added in read and create functionality

### 2. CRUD functionality for many-to-many relationship
   - Depends on: 1
   - Effort: Large (1 week)
   - Subtasks:
     - Add join logic to allow for many-to-many relationship
     - Test operations

### 3. Database considerations
   - Depends on: 1 and 2
   - Effort: Medium (2–3 days)
   - Subtasks:
     - Sanitize user input and validate form data
     - Create a user for database operations from the application
       - should have minimum required permissions

### 4. Prepare final presentation/demo
   - Depends on: 3
   - Effort: Medium (2–3 days)
   - Subtasks:
     - Write outline and talking points for presentation
     - Prepare demonstration

### 5. Post-class presentation and cleanup
   - Depends on: 3 and 4
   - Effort: Large (1 week)
   - Subtasks:
     - Clean up code and documentation
     - Add visuals and deploy the project demo