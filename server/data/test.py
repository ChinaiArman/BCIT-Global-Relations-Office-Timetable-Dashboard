duplicate_rows_df = df[df.duplicated()]
print("number of duplicate rows in original: ", duplicate_rows_df.shape[0])

# // remove the * from Instructor column only
df['* Instructor'] = df['* Instructor'].str.replace('*', '')
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

print(df.head())
# // create new dataframe with only: Block, CRN, Course, Type, Day, Start Date, End Date

# create new dataframe dropping * Instructor
# new_df_no_instructor = df.drop(['* Instructor'], axis=1)

# //count the number of duplicate rows in the new dataframe
# duplicate_rows_df_no_instructor = new_df_no_instructor[new_df_no_instructor.duplicated()]
# print("number of duplicate rows INSTRUCTOR: ", duplicate_rows_df_no_instructor.shape[0])


new_df = df[['Block', 'CRN', 'Course', 'Type', 'Day', 'Begin Time', 'End Time', '* Instructor', '* Bldg/Room', 'Start Date', 'End Date']]

# print the frirst 50 rows of the new dataframe
print(new_df.head(50))

# where there is a duplicate in every column except instructor, add the instructor to the first row and delete the second row
new_df = new_df.drop_duplicates(subset=new_df.columns.difference(['* Instructor']), keep=False)


# // count number of duplicate rows in the new dataframe
duplicate_rows_df = new_df[new_df.duplicated()]
print("number of duplicate rows: ", duplicate_rows_df.shape[0])

# //print 100 of the duplicate_rows_df
print(duplicate_rows_df.head(100))