import matplotlib.font_manager as fm

# List all available fonts
available_fonts = fm.findSystemFonts(fontpaths=None, fontext="ttf")

# Print the full paths of the fonts
for font in available_fonts:
    print(font)

# Alternatively, to just print the font names
font_names = [fm.FontProperties(fname=font).get_name() for font in available_fonts]
unique_font_names = sorted(set(font_names))  # Remove duplicates and sort alphabetically

print("\nAvailable Font Names:")
for font_name in unique_font_names:
    print(font_name)

# BIZ UDGothic
# BIZ UDMincho
# MS Gothic
# MS Mincho
# Meiryo
# Malgun Gothic (Korean-focused but often supports Japanese)
# Noto Sans JP
# Yu Gothic
# Yu Mincho
