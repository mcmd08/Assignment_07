#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# Maria Dacutanan, 2020-Aug-25, Updated read_file function to to unpickle my 2D list
# Maria Dacutanan, 2020-Aug-25, Updated read_file function to include error handling for file not existing
# Maria Dacutanan, 2020-Aug-25, Updated write_file function to pickle my 2D list
# Maria Dacutanan, 2020-Aug-25, Updated write_file function to include error handling for permission or disk space issues
# Maria Dacutanan, 2020-Aug-25, Updated get_newInventory function to force user to enter a numeric ID
# Maria Dacutanan, 2020-Aug-26, Updated read_file function to include exception handling for unpickling errors
# Maria Dacutanan, 2020-Aug-26, Updated read_file function to include exception handling for unpickling empty file
# Maria Dacutanan, 2020-Aug-26, Updated write_file function to include exception handling for pickling errors
#------------------------------------------#

import pickle


# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
loadErr=False

# -- PROCESSING --  #
class DataProcessor:

    """Add or Delete Data from Inventory"""
    
    @staticmethod
    def add_newInventory(id, title, artist, table):
        """Function to add new data into CDInventory
        
        Args:
            id(string): id of new entry
            title(string): CD title of new entry
            artist(string): arist's name of new entry
        
        Returns:
            None
        """
        dicRow = {'ID': id, 'Title': title, 'Artist': artist}
        table.append(dicRow)
    
    @staticmethod
    def del_inventory(id, table):
        """Function to Delete from CDInventory
        
        Args:
            id(string)=id of entry in CDInventory that is to be deleted
        
        Returns:
            None
        """
        
        blnCDRemoved = False
        lstID=[]
        delctr=0
        for cd in table:                   
            for row in cd['ID']:
                lstID.append(row) #Store all IDs from lstTbl into lstID table
        if lstID.count(id) > 0: #Check if user input exists in lstID
            intRowNr = 0            
            #This while block will loop thru lstTbl to delete ALL instances of ID in case of duplicates
            while intRowNr < len(lstTbl):
                if (table[intRowNr]['ID']) == id:
                    # del lstTbl[intRowNr]
                    del table[intRowNr]
                    delctr+=1 #Count number of deletions
                    intRowNr=0 #if ID was deleted, restart intRowNr as lstTbl has shifted
                else:
                    intRowNr += 1#increase intRowNr to move on to next index of lstTbl                         
            blnCDRemoved = True

        if blnCDRemoved:
            print('{} CD(s) removed.\n'.format(delctr))
        else:
            print('Could not find this CD!\n')
        # return None


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        loadctr=0
        try:
            with open(file_name, 'rb') as objFile:
                data=pickle.load(objFile) #dump my 2D list into data
            while loadctr <  len(data):
                    table.append(data[loadctr]) #append my list element (which is a dictionary) into table
                    loadctr+=1 #count number of rows loaded into memory
            print ('{} CD(s) loaded into inventory.\n'.format(loadctr))
        except FileNotFoundError as e:
            print('Unable to load inventory from ' + file_name + '.') #exception handling for file not existing
            print ()
            print (e, e.__doc__, sep='\n')
            print()
        except EOFError as e:
            print(file_name + ' is empty.') #exception handling for empty file
            print ()
            print (e, e.__doc__, sep='\n')
            print()
        except pickle.UnpicklingError as e:
            print(file_name + ' is corrupted.') #exception handling for unpickling error
            print ()
            print (e, e.__doc__, sep='\n')
            print()

            
    @staticmethod
    def write_file(file_name, table):
        """Function to Save CDInventory into File
        
        Args:
            file_name(file object)=filename of CDInventory file
            table(list)= list of CDInventory dictionaries
        
        Return:
            None
        """
        
        savectr=len(table)
        try:
            with open (file_name, 'wb') as objFile:
                pickle.dump(table,objFile) #pickle my 2D list
            print ('{} CD(s) saved into {}.\n'.format(savectr,file_name))
        except PermissionError as e:
            print('Not enough rights to create/modify ' + file_name + '.') #if unable pickle data due to permission issues
            print ()
            print (e, e.__doc__, sep='\n')
            print ()
        except IOError as e:
            print ('I/O error({0}): {1}'.format(e.errno,e.strerror))#if unable to pickle data due to IO errors such as disk space issues
            print ()
            print (e, e.__doc__, sep='\n')
            print ()
        except pickle.PickleError as e:
            print ('Unable to write data into ' + file_name + '.') #if unable to pickle 2D list, exception handling for pickling errors
            print ()
            print (e, e.__doc__, sep='\n')
            print ()



# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation wouild you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        if (table):
            print('======= The Current Inventory: =======')
            print('ID\tCD Title (by: Artist)\n')
            for row in table:
                print('{}\t{} (by:{})'.format(*row.values()))
            print('======================================')
        else:
            print ('Inventory is empty.\n')
        # return None

    @staticmethod
    def get_newInventory():
        """Prompts User to provide ID, Title and Arist Name 


        Args:
            None

        Returns:
            strID (string) - ID
            strTitle (string) - Title
            strArtist (string) - Artist

        """
        
        while True: #user is re-prompted for null ID
            strID = str(input('Enter an ID: ').strip())
            if (strID):
                if not (strID.isdigit()): #user is re-prompted for ID if a non-digit ID was entered
                    print('Please use a numeric ID.')
                else:
                    break
        while True: #user is re-prompted for null CD Title
            strTitle = input('Enter the CD\'s Title: ').strip()
            if (strTitle):
                break
        while True: #user is re-prompted for null Artist's Name
            strArtist = input('Enter the Artist\'s Name: ').strip()
            if (strArtist):
                break
        return (strID, strTitle, strArtist)

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 procless load inventory
    if strChoice == 'l':
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
            strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
            if strYesNo.lower() == 'yes':
                print('reloading...')
                FileProcessor.read_file(strFileName, lstTbl) # function call to read CDInventory.txt
                IO.show_inventory(lstTbl)
            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(lstTbl)
            continue  # start loop back at top.

    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        intID,strTitle,strArtist=IO.get_newInventory() #function call to prompt user for ID, CD Title and Artist and unpack return values
        DataProcessor.add_newInventory(intID, strTitle, strArtist, lstTbl) #function call to add data into inventory
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get user input for which CD to delete
        # 3.5.1.1 display Inventory to user        
        if (lstTbl): #check if lstTbl is not empty
        # 3.5.1.2 ask user which ID to remove
            while True:
                intIDDel = input('Which ID would you like to delete? ').strip()
                if (intIDDel): #user is re-prompted for empty ID
                    DataProcessor.del_inventory(intIDDel, lstTbl) #function call to delete user provided ID
                    break
            IO.show_inventory(lstTbl)
        else:
            print('Nothing to delete. Inventory is empty.\n')
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        if (lstTbl):
            IO.show_inventory(lstTbl)
            strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
            # 3.6.2 Process choice
            if strYesNo == 'y':
                # 3.6.2.1 save data
                FileProcessor.write_file(strFileName, lstTbl) #function call to write inventory into file
            else:
                input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        else:
            print('Nothing to save. Inventory is empty.\n')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




