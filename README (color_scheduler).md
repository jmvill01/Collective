COLOR SCHEDULER
Requested by: Nathan Garcia & Hope Griffin
Developed by: Joel Villamor
V: 1.1.0 (Latest)


V: 1.1.0 Update:
Added functionality for reading the quantity column of the truck closing file. This should
provide accurate sums for all entries and display the corresponding sum in the GUI.


Abstract:
The color scheduler was meant to tackle the irritably tedious process of counting,  
reordering, and verifying order color plans. As a manual process, this task usually 
cost its producers anywhere from 45 mins to 2+ hrs a week to create. The result of this 
software is producing the same color plans at a fraction of the time spent as the 
production of these lists are usually instantaneous. 


Inputs/Outputs:
The color scheduler, takes truck closing data (csv) and a corresponding color sequence.
The color sequence is a csv document formatted within the first column. The original 
Brentwood color sequence will provide the order in which the colors are handled. 

1. color sequence
    - Note: The finalized color sequence format/cleaned up color options is located within
    the color_sequence folder within the given zip file. Use this file for the import of
    the color sequence selection. It should provide the highest accuracy as of 06/29/23.

    Formatting color sequence files:
    The color sequence files are formatted with all color options in the first column.
    This file should provide both the order by which the colors will be ran through the 
    plant, as well as the color descriptors. Ensure that there are no duplicates, misspellings
    or blank lines in the data to provide the most accurate result.

By taking this data and formatting it within one column (one color per row), the software
takes it and creates an inner dictionary (the order being preserved). The dictionary 
entries are incremented per color as the truck closing file is being evaluated. This
creates the corresponding quantities seen in the table after clicking "Visualize".

2. truck closing file

After clicking "Save", the color scheduler will prompt the user with a file saving
prompt. This software produces a csv formatted file and it is preferable that the user
place the '.csv' extension at the end of the desired filename, though it is not necessary to see the data.

Note: The table presented is read-only. Any changes made to the table after visualizing the sort
may not be reflected when saving the file.

Output: <filename>.csv

<Note:>
The output of the software will first be the colors that followed the algorithm and are sorted correctly. 
The additional field, preficed with "Unmatched Colors:" are colors and their corresponding quantities that 
did not match any of the given color sequence descriptors.

These colors will have to be manually sorted within the correctly sorted entries above. These unmatched 
colors likely signify that the inputted "color sequence" file is outdated and in need of updating.  


Installation:
1. Copy the zip folder from the I-drive onto your pc (your location of choice).
2. Extract the folder in the location of choice  
3. Navigate through the extracted folder contents as shown below:
    - dist (folder)
    - color_scheduler (folder)
4. Find and move the file "color_scheduler.exe" to a convenient location for ease of use (optional)
    - you may also use the "send to" -> "Desktop" options on the right click of the mouse
5. Double click the executable (.exe) and the program will start.

Bug Report/Feedback form:
https://forms.office.com/Pages/DesignPageV2.aspx?origin=NeoPortalPage&subpage=design&id=b6WNC91KR0a8VR2kwHD_ASsGFTGswvFOin0cLP8glVhUM1lWTFBEMENETktVRUE3VU8yNTlWNUU4RC4u&topview=Preview
