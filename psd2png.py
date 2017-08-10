from psd_tools import PSDImage
import os

for fname in os.listdir('./psd'):
    fn, ext = fname.split('.')
    if ext == 'png':
        print(fname)
        # print('%s %s %s' % (fname, fn, ext))
    # psd = PSDImage.load('./psd/%s'% fname)
    # img = psd.as_PIL()
    # img.save('./psd/%s.png' % fn)
# for folderName, subFolders, filenames in os.walk('./psd'):
#     for filename in filenames:
#         print(filename)
