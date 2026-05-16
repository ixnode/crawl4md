# Combined remove_images Cases

This fixture combines all known `remove_images` transformations in one file.

## 1. Plain image without alt or title

Image syntax is removed completely when no alt or title exists.

![](image.jpg)

## 2. Plain image with alt text

Alt text is kept.

![Boeing 707 Cockpit](cockpit.jpg)

## 3. Plain image with title but empty alt

If alt text is empty, title text is used.

![](image.jpg "Cockpit einer Boeing 707")

## 4. Plain image with alt and title

Alt text wins over title text.

![Alt text](image.jpg "Title text")

## 5. Linked image without alt or title

Image syntax is removed, but the outer link remains.

[![](image.jpg)](file.jpg)

## 6. Linked image with alt text

Image syntax is removed, alt text is preserved as link text, and the outer link target remains.

[![Eine Boeing 707 der Air India](https://upload.wikimedia.org/image.jpg)](https://de.wikipedia.org/wiki/Datei:image.jpg "Eine Boeing 707 der Air India")

## 7. Regular link plus plain image in one line

Regular links are unchanged. Plain image syntax is removed.

Text [keep](file.jpg) ![](image.jpg) after

## 8. Link containing image and text

Image syntax is removed; remaining text stays inside the outer link.

Text [![icon](icon.jpg) keep](file.jpg)

## 9. Linked wrapper with multiple images

All image syntaxes are removed; collected image text remains as link text.

[![](one.jpg) ![Two](two.jpg)](file.jpg)
