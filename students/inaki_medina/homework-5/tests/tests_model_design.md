Task Model tests

Task Creation
Unit test: Create task with valid data
Unit test: Reject title with fewer than 3 characters
Unit test: Reject title exceeding 100 characters

Status Transitions
Unit test: Valid transition from TODO to IN_PROGRESS
Unit test: Invalid backward transition

Overdue Detection
Unit test: Detect an overdue unfinished task
Unit test: Completed and archived tasks are not overdue

Priority Comparison
Unit test: Compare higher, lower, and equal priorities

Due Date Validation
Unit test: Accept a future dueDate
Unit test: Reject a past dueDate
