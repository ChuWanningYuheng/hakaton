from file_viewer import view_file
import pandas as pd 
file_content = view_file()
file_content_df = pd.DataFrame(file_content.split())
print((file_content_df))
