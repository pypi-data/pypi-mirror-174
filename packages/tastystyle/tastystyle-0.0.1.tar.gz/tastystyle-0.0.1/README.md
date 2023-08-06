# tastystyle
a small python package for styling the terminal. how original, i know.

tastystyle supports colours, bold text, dim text, italics, underlined, background and foreground reversal and strikethrough text.

please note not all styles work on windows

## colours
text is coloured with the `bg()` and `fg()` commands. it support keywords, rgb colours, and hex colours.

example:
```python
from tastystyle import colors as c

# keyword
print(f'{c.FG("GREEN")}Green!{c.RESET()}')
# rgb
print(f'{c.FG(65, 214, 62)}Green!{c.RESET()}')
# hex
print(f'{c.FG("#41d63e")}Green!{c.RESET()}')
```
<details>
<summary>all keywords</summary>	
<table>
<thead>
<tr>
<th>name</th>
<th>rgb</th>
<th>hex</th>
</tr>
</thead>
<tbody>
<tr>
<td>RED</td>
<td>214, 62, 62</td>
<td>#d63e3e</td>
</tr>
<tr>
<td>ORANGE</td>
<td>214, 143, 62</td>
<td>#d68f3e</td>
</tr>
<tr>
<td>YELLOW</td>
<td>211, 214, 62</td>
<td>#d3d63e</td>
</tr>
<tr>
<td>L_GREEN</td>
<td>98, 214, 96</td>
<td>#62d660</td>
</tr>
<tr>
<td>GREEN</td>
<td>65, 214, 62</td>
<td>#41d63e</td>
</tr>
<tr>
<td>CYAN</td>
<td>62, 214, 199</td>
<td>#3ed6c7</td>
</tr>
<tr>
<td>L_BLUE</td>
<td>62, 161, 214</td>
<td>#3ea1d6</td>
</tr>
<tr>
<td>BLUE</td>
<td>62, 65, 214</td>
<td>#3e41d6</td>
</tr>
<tr>
<td>PURPLE</td>
<td>181, 62, 214</td>
<td>#b53ed6</td>
</tr>
<tr>
<td>VIOLEET</td>
<td>214, 62, 209</td>
<td>#d63ed1</td>
</tr>
</tbody>
</table>

</details>

## other
text can be styled in other ways with the following:
```python
from tastystyle import styles as s

# bold
print(f'{s.BOLD()}bold text{s.RESET()}')
# italic
print(f'{s.ITALIC()}italic text{s.RESET()}')
# underline
print(f'{s.UNDER()}underlined text{s.RESET()}')
# strikethrough
print(f'{s.STRIKE()}strikethrough text{s.RESET()}')
# dim
print(f'{s.DIM()}dim text{s.RESET()}')
# reversed
print(f'{s.REVERSE()}reversed text{s.RESET()}')
```

created with ❤ by tastyl