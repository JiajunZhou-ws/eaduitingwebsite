import os
filepath = "C:\Users\zhout9\Desktop\website\static\Uploads"
for each in os.listdir(filepath):
    print each.decode('gbk').encode('utf-8')
