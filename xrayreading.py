# xrayreading.py

import re
# Import BeautifulSoup for parsing HTML. Get via easy_install.
import beautifulsoup4

# Modify valid_tags and valid_attrs for HTML whitelisting. Code by @palewire.
def sanitize_html(value):
    valid_tags = 'p i b a'.split()
    valid_attrs = ''.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                     if attr in valid_attrs]
    return soup.renderContents().decode('utf8').replace('javascript:', '')

# Convert from b, i to span with title
def italic_to_title(value):
    soup = BeautifulSoup(value)
    xraycomments = []

# Ask the user for X-ray conversion
filetoxray = input('File to X-ray? ')

# Read the file as a string
contents = open(filetoxray, 'r').read()

# Whitelist tags and attributes
sanitized = sanitize_html(contents)

# Regex to remove empty paragraph tags
sanitized = re.sub('<p>\s*?&nbsp;\s*?</p>', '', sanitized)
done = re.sub('<b>', '<span class="xray">', sanitized)

italic_to_title(done)

# Write the converted file and give user confirmation
convertedfile = "xray-" + filetoxray
file = open(convertedfile, 'w')
file.write(done)
file.close()
print("Converted file saved as: %s" % convertedfile)
