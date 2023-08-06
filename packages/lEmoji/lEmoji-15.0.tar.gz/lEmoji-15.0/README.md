<p align="center">
    <br>
    lEmoji
    <br>
<p>

<h3 align="center">
	<p>Longstanding Emoji With Historical Version and Generator</p>
</h3>

LEmoji provides latest and any other historical version's emoji array.

```python
from lEmoji import EMOJI_LIST
from lEmoji import EMOJI_LIST_11_0  # version 11.0
```


LEmoji provides emoji generator to update new versions of emoji without upgrade this library.

```python
from lEmoji.generator import Generator
Generator().generate()

>>> Retrieving https://www.unicode.org/Public/emoji/ ...
>>> Retrieving https://www.unicode.org/Public/emoji/1.0/ ...
>>> Retrieving https://www.unicode.org/Public/emoji/2.0/ ...
...
>>> Retrieving https://www.unicode.org/Public/emoji/13.0/ ...
>>> Retrieving https://www.unicode.org/Public/emoji/13.1/ ...
>>> Retrieving https://www.unicode.org/Public/emoji/1.0/emoji-data.txt ...
>>> Retrieving https://www.unicode.org/Public/emoji/2.0/emoji-data.txt ...
>>> Retrieving https://www.unicode.org/Public/emoji/2.0/emoji-sequences.txt ...
...
>>> Retrieving https://www.unicode.org/Public/emoji/13.1/emoji-zwj-sequences.txt ...
```

### Join Us

If you have any interest to contribute this project, [contact me](mailto:i@6-79.cn) without hesitation!

### Release History

#### 0.2.1.beta, Released on Dec 25, 2020

- Fix the bug of failed installing

#### 0.2.beta, Released on Oct 31, 2020

- As unicode.org modified the html code, we fix the bug that generator is failed to grab emoji data.
- We create this description file.

#### 0.1.beta, Released on Feb 22, 2020

- LEmoji is born.
- We grab emoji data from version 1.0 to version 13.0.
- We provide generator for off-pip updating.
