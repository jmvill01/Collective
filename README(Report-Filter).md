# Report Filter
REPORT FILTER
Requested by: Fernando Mendoza
Developed by: Joel Villamor
V: 1.2.0 (Latest)


V: 1.2.0 Update:
New Functionality:
    - Macros
    - Mods
    - Auto-save Feature (for macros)
This update is substantial in features and changes. The most basic, but necessary change was to implement the mod filtering capabilities. This will enable the user to filter out the mods that they don't want to see. The macro functionality allows the user to create shortcuts that enable them to view a preset list of modifications  that they want to see.

In order to fail proof the system, an auto-save feature was incorporated that will save all newly created macros and mods to the "macro_mods.csv" file located in the _res folder of the zip file. This should ensure the safety of all the user's macros regardless of program crashes, system failures, and whatever else may cause unwanted data loss. (Auto-Save occurs every 15s and on program exit)

Abstract:
This project was meant to handle the auto filtration of certain data points regarding the usual trkclcsv.csv file.
With this software, it will allow the user to filter through data entries that correspond with the given 'Attribute'
and 'Sched Date'.

'Sched Date' and 'Attribute' correspond with the columns: 0 and 1 within trkclcsv. 

After specifying the given parameters, the software will provide all entries that correspond with those points
and provide the following columns/properties:

    - Truck
    - Order
    - Line
    - Item
    - MODS (The items associated modifications)

All data points that are provided to the right of the Mods column are considered the associated modifications
that correspond with the entry/row.

Future Improvements:
    - Improve the UI (Shrink/Expand capabilities)
    - Improve Table Interactibility
    - Allow for a range of dates to be seen/filtered
    - Add Bug reporting form to software (temporarily provided below)
    - Add in Headers to the table
