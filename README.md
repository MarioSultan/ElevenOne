# **ElevenOne**: *your perfect lab assistant*

![ElevenOne Logo](https://raw.githubusercontent.com/MarioSultan/ElevenOne/main/banner.png)

ElevenOne is a Python library for seamless scientific unit management, rigorous laboratory data processing, and automated publication-ready plotting.

Some of the things ElevenOne can do include:
* Handling of physical units

---

## Handling of physical units

ElevenOne features a complete internal system for handling physical units. Among the things it can do are the use and management of physical units, operations with them, and conversion between them.

```python
from elevenone import *

speed = 90 * km/h
print(speed.convert_to(m/s))
```
```python
>>> 25 m/s
```

ElevenOne has more than 60 different units to use in your project!
