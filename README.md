# work_log
A terminal application for logging what work someone did on a certain day. The user can either add an entry or look up previous entries.
When you add an entry, the script asks for a task name, how much time was spent on the task, and any general notes about the task. 
Each entry is recorded into a row of a CSV file along with a date.

User can find all of the tasks that were done on a certain date (or a date range),
or that match a search string (either as a regular expression or a plain text search), or that required certain amount of time to fulfill. 
Search results are printed to the screen, including the date, title of task, time spent, and general notes.
