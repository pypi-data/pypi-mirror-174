# DataWriter 
This python package allows for added ease when saving data to a .csv for post processing later.  

Refer to example.py for a more thorough walkthrough
'''python
# Initialize instrument and datawriter
writer_example = datawriter(filename="example", output_direct="deleteme", replace_file=True)

# identify the indexes of your columns of data that you want to collect
writer_example.write_header("col1", "col2", "col3")

# for in in data collected, write to .csv or .txt. Note that the file will not be corrupted 
# even if your script errors out midway.
for i in range(5):
    writer_example.write_row(i*.001, str(i), ["Hello World!"])
'''