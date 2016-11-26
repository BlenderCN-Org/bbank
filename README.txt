#golly gee willikers i can't beleive this old thing still functions


##### old txt from way way back:

    Library » Path » Blend » (Category ») Asset

        • Library – A User Selected Path.

            A library represents a folder in the filesystem
            where blend files are kept.

            Following the entry of the library into the database, paths are added.

            ° If recurse is checked, paths will be entered for every folder of the library which contains blend files.
            
            ° If recurse is not checked, only the path of the library will be added to the database.

            Assets are not scanned for during this step.
            
            Libraries, Paths, Blends, and Assets, have a state of exclusion or inclusion. Default is to include.

            The user may toggle a library on or off.  This affects the exclusion of paths within the library, which in
            turn affects the exclusion of blends within the paths and for each blend's assets as well.


    ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————


        • Path – Paths Contain Blends.

            Following the entry of the path into the database, blends are added.


    ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————


        • Blend – Blend Files contain Assets. 

            Blend files are scanned for asset content, either one by one or all included.
            

    ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————


        • Asset – Assets belong to one of twenty-seven categories.
            
            Assets have post-load actions which allow to:

            Load an object at cursor location.

            Load an image in image editor.

            Load a text in text editor.

            Apply a loaded material to selected objects.


    ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————


        • Category –

            Types of datablock that are saved with a blend file.

    ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————


        ° Note –

            Notes may be kept on assets.

    ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————


        ° Bank - 0 1 2 3 4 5 6 7 8 9 

            A bank is selected by pressing the asterix on the number-pad twice, followed by one of
            the number pad digits 0 through 9.  Each bank has ten slots.

            Escape cancels.
    ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————


        • Slot - 0 1 2 3 4 5 6 7 8 9
            
            An asset is loaded from the active bank by pressing the asterix the number pad once, followed by on of the
            number pad digits 0 through 9

            Escape cancels.
