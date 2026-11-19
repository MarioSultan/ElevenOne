# Plot Styles & Customization (`set_style`)

**ElevenOne** features a built-in style catalog containing **52 curated visual presets** ranging from clean academic themes and basic colors to dark modes and vibrant neon palettes.

You can instantly switch global styles using `Data.set_style()`, register your own custom styles, or override specific color attributes on the fly.

---

## 1. Setting a Preset Style (`Data.set_style`)

To apply a predefined style across all plots, pass its name to `Data.set_style()`:

```python
from elevenone import Data

# Apply a preset theme
Data.set_style("dark_mode")

# List all available styles
print(Data.list_styles())
```

> 💡 **Backward Compatibility:** `Data.set_theme()` remains available as an alias for `set_style()`.

---

## 2. Available Presets Catalog

Below is the complete list of all 52 built-in styles organized by category, along with their hex color codes and visual swatches:

### Brand & Basic Colors
Clean, bright backgrounds paired with standard or signature brand primary colors.

| Style Name | Primary | Secondary | Background (`facecolor`) | Canvas (`figure_facecolor`) | Text Color |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`elevenone`** *(Default)* | <code style="background:#00ccff;color:#000000;padding:2px 6px;border-radius:3px;">#00ccff</code> | <code style="background:#ff2ad4;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff2ad4</code> | <code style="background:#fcfcfc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fcfcfc</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#1a1a1a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a1a1a</code> |
| **`enonevele`** | <code style="background:#ff2ad4;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff2ad4</code> | <code style="background:#00ccff;color:#000000;padding:2px 6px;border-radius:3px;">#00ccff</code> | <code style="background:#fcfcfc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fcfcfc</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#1a1a1a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a1a1a</code> |
| **`red`** | <code style="background:#ee0000;color:#ffffff;padding:2px 6px;border-radius:3px;">#ee0000</code> | <code style="background:#000000;color:#ffffff;padding:2px 6px;border-radius:3px;">#000000</code> | <code style="background:#fcfcfc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fcfcfc</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#1a1a1a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a1a1a</code> |
| **`yellow`** | <code style="background:#ffbb00;color:#000000;padding:2px 6px;border-radius:3px;">#ffbb00</code> | <code style="background:#000000;color:#ffffff;padding:2px 6px;border-radius:3px;">#000000</code> | <code style="background:#fcfcfc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fcfcfc</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#1a1a1a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a1a1a</code> |
| **`green`** | <code style="background:#00aa00;color:#ffffff;padding:2px 6px;border-radius:3px;">#00aa00</code> | <code style="background:#000000;color:#ffffff;padding:2px 6px;border-radius:3px;">#000000</code> | <code style="background:#fcfcfc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fcfcfc</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#1a1a1a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a1a1a</code> |
| **`blue`** | <code style="background:#0088ff;color:#ffffff;padding:2px 6px;border-radius:3px;">#0088ff</code> | <code style="background:#000000;color:#ffffff;padding:2px 6px;border-radius:3px;">#000000</code> | <code style="background:#fcfcfc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fcfcfc</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#1a1a1a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a1a1a</code> |
| **`purple`** | <code style="background:#8822ff;color:#ffffff;padding:2px 6px;border-radius:3px;">#8822ff</code> | <code style="background:#000000;color:#ffffff;padding:2px 6px;border-radius:3px;">#000000</code> | <code style="background:#fcfcfc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fcfcfc</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#1a1a1a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a1a1a</code> |

---

### Formal, Academic & Minimalist
High-contrast, low-glare themes ideal for papers, reports, and publications.

| Style Name | Primary | Secondary | Background (`facecolor`) | Canvas (`figure_facecolor`) | Text Color |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`classic_paper`** | <code style="background:#1f77b4;color:#ffffff;padding:2px 6px;border-radius:3px;">#1f77b4</code> | <code style="background:#d62728;color:#ffffff;padding:2px 6px;border-radius:3px;">#d62728</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#000000;color:#ffffff;padding:2px 6px;border-radius:3px;">#000000</code> |
| **`monochrome`** | <code style="background:#333333;color:#ffffff;padding:2px 6px;border-radius:3px;">#333333</code> | <code style="background:#777777;color:#ffffff;padding:2px 6px;border-radius:3px;">#777777</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#f5f5f5;color:#000000;padding:2px 6px;border-radius:3px;">#f5f5f5</code> | <code style="background:#111111;color:#ffffff;padding:2px 6px;border-radius:3px;">#111111</code> |
| **`emerald`** | <code style="background:#10b981;color:#ffffff;padding:2px 6px;border-radius:3px;">#10b981</code> | <code style="background:#f59e0b;color:#000000;padding:2px 6px;border-radius:3px;">#f59e0b</code> | <code style="background:#f8fafc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#f8fafc</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#0f172a;color:#ffffff;padding:2px 6px;border-radius:3px;">#0f172a</code> |
| **`nordic`** | <code style="background:#88c0d0;color:#000000;padding:2px 6px;border-radius:3px;">#88c0d0</code> | <code style="background:#81a1c1;color:#ffffff;padding:2px 6px;border-radius:3px;">#81a1c1</code> | <code style="background:#eceff4;color:#000000;padding:2px 6px;border-radius:3px;">#eceff4</code> | <code style="background:#e5e9f0;color:#000000;padding:2px 6px;border-radius:3px;">#e5e9f0</code> | <code style="background:#2e3440;color:#ffffff;padding:2px 6px;border-radius:3px;">#2e3440</code> |
| **`arctic_frost`** | <code style="background:#00b4d8;color:#ffffff;padding:2px 6px;border-radius:3px;">#00b4d8</code> | <code style="background:#90e0ef;color:#000000;padding:2px 6px;border-radius:3px;">#90e0ef</code> | <code style="background:#f0f8ff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#f0f8ff</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#03045e;color:#ffffff;padding:2px 6px;border-radius:3px;">#03045e</code> |
| **`glacier_blue`** | <code style="background:#489fb5;color:#ffffff;padding:2px 6px;border-radius:3px;">#489fb5</code> | <code style="background:#8adaec;color:#000000;padding:2px 6px;border-radius:3px;">#8adaec</code> | <code style="background:#f0f7f9;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#f0f7f9</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#1b4965;color:#ffffff;padding:2px 6px;border-radius:3px;">#1b4965</code> |
| **`solarized_light`** | <code style="background:#2aa198;color:#ffffff;padding:2px 6px;border-radius:3px;">#2aa198</code> | <code style="background:#dc322f;color:#ffffff;padding:2px 6px;border-radius:3px;">#dc322f</code> | <code style="background:#fdf6e3;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fdf6e3</code> | <code style="background:#eee8d5;color:#000000;padding:2px 6px;border-radius:3px;">#eee8d5</code> | <code style="background:#657b83;color:#ffffff;padding:2px 6px;border-radius:3px;">#657b83</code> |
| **`holographic`** | <code style="background:#00f5d4;color:#000000;padding:2px 6px;border-radius:3px;">#00f5d4</code> | <code style="background:#7b2cbf;color:#ffffff;padding:2px 6px;border-radius:3px;">#7b2cbf</code> | <code style="background:#f8f9fa;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#f8f9fa</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#212529;color:#ffffff;padding:2px 6px;border-radius:3px;">#212529</code> |

---

### Warm, Pastel & Vintage Light
Soft, organic, and expressive palettes on light or cream backgrounds.

| Style Name | Primary | Secondary | Background (`facecolor`) | Canvas (`figure_facecolor`) | Text Color |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`sunset`** | <code style="background:#ff5e62;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff5e62</code> | <code style="background:#ff9966;color:#000000;padding:2px 6px;border-radius:3px;">#ff9966</code> | <code style="background:#fffaf0;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fffaf0</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#2c3e50;color:#ffffff;padding:2px 6px;border-radius:3px;">#2c3e50</code> |
| **`autumn`** | <code style="background:#d35400;color:#ffffff;padding:2px 6px;border-radius:3px;">#d35400</code> | <code style="background:#c0392b;color:#ffffff;padding:2px 6px;border-radius:3px;">#c0392b</code> | <code style="background:#fdfefe;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fdfefe</code> | <code style="background:#f9ebea;color:#000000;padding:2px 6px;border-radius:3px;">#f9ebea</code> | <code style="background:#512e5f;color:#ffffff;padding:2px 6px;border-radius:3px;">#512e5f</code> |
| **`royal_purple`** | <code style="background:#8e44ad;color:#ffffff;padding:2px 6px;border-radius:3px;">#8e44ad</code> | <code style="background:#f1c40f;color:#000000;padding:2px 6px;border-radius:3px;">#f1c40f</code> | <code style="background:#f4ecf7;color:#000000;padding:2px 6px;border-radius:3px;">#f4ecf7</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#4a235a;color:#ffffff;padding:2px 6px;border-radius:3px;">#4a235a</code> |
| **`cherry_blossom`** | <code style="background:#ff758c;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff758c</code> | <code style="background:#ff7eb3;color:#000000;padding:2px 6px;border-radius:3px;">#ff7eb3</code> | <code style="background:#fff0f5;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fff0f5</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#ffffff</code> | <code style="background:#4a3b4c;color:#ffffff;padding:2px 6px;border-radius:3px;">#4a3b4c</code> |
| **`coffee`** | <code style="background:#a0522d;color:#ffffff;padding:2px 6px;border-radius:3px;">#a0522d</code> | <code style="background:#deb887;color:#000000;padding:2px 6px;border-radius:3px;">#deb887</code> | <code style="background:#fdf5e6;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fdf5e6</code> | <code style="background:#fff8dc;color:#000000;padding:2px 6px;border-radius:3px;">#fff8dc</code> | <code style="background:#3e2723;color:#ffffff;padding:2px 6px;border-radius:3px;">#3e2723</code> |
| **`lavender`** | <code style="background:#9b59b6;color:#ffffff;padding:2px 6px;border-radius:3px;">#9b59b6</code> | <code style="background:#3498db;color:#ffffff;padding:2px 6px;border-radius:3px;">#3498db</code> | <code style="background:#fbfcfc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fbfcfc</code> | <code style="background:#f4f6f7;color:#000000;padding:2px 6px;border-radius:3px;">#f4f6f7</code> | <code style="background:#2c3e50;color:#ffffff;padding:2px 6px;border-radius:3px;">#2c3e50</code> |
| **`steampunk`** | <code style="background:#b8860b;color:#ffffff;padding:2px 6px;border-radius:3px;">#b8860b</code> | <code style="background:#cd853f;color:#000000;padding:2px 6px;border-radius:3px;">#cd853f</code> | <code style="background:#f4e8d1;color:#000000;padding:2px 6px;border-radius:3px;">#f4e8d1</code> | <code style="background:#e6d5b8;color:#000000;padding:2px 6px;border-radius:3px;">#e6d5b8</code> | <code style="background:#4a3525;color:#ffffff;padding:2px 6px;border-radius:3px;">#4a3525</code> |
| **`pastel_dream`** | <code style="background:#ffb703;color:#000000;padding:2px 6px;border-radius:3px;">#ffb703</code> | <code style="background:#fb8500;color:#000000;padding:2px 6px;border-radius:3px;">#fb8500</code> | <code style="background:#fdfcdc;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fdfcdc</code> | <code style="background:#fef9ef;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fef9ef</code> | <code style="background:#386641;color:#ffffff;padding:2px 6px;border-radius:3px;">#386641</code> |
| **`matcha_latte`** | <code style="background:#52796f;color:#ffffff;padding:2px 6px;border-radius:3px;">#52796f</code> | <code style="background:#84a98c;color:#000000;padding:2px 6px;border-radius:3px;">#84a98c</code> | <code style="background:#f4f7f4;color:#000000;padding:2px 6px;border-radius:3px;">#f4f7f4</code> | <code style="background:#eaf2ec;color:#000000;padding:2px 6px;border-radius:3px;">#eaf2ec</code> | <code style="background:#2f3e46;color:#ffffff;padding:2px 6px;border-radius:3px;">#2f3e46</code> |
| **`vintage_sepia`** | <code style="background:#8c6239;color:#ffffff;padding:2px 6px;border-radius:3px;">#8c6239</code> | <code style="background:#a97d5d;color:#ffffff;padding:2px 6px;border-radius:3px;">#a97d5d</code> | <code style="background:#fbf8f2;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fbf8f2</code> | <code style="background:#f3eee3;color:#000000;padding:2px 6px;border-radius:3px;">#f3eee3</code> | <code style="background:#3b2f2f;color:#ffffff;padding:2px 6px;border-radius:3px;">#3b2f2f</code> |
| **`terracotta_warmth`** | <code style="background:#e07a5f;color:#ffffff;padding:2px 6px;border-radius:3px;">#e07a5f</code> | <code style="background:#f4a261;color:#000000;padding:2px 6px;border-radius:3px;">#f4a261</code> | <code style="background:#fefee3;color:#000000;padding:2px 6px;border-radius:3px;border:1px solid #ccc;">#fefee3</code> | <code style="background:#f4f1de;color:#000000;padding:2px 6px;border-radius:3px;">#f4f1de</code> | <code style="background:#264653;color:#ffffff;padding:2px 6px;border-radius:3px;">#264653</code> |

---

### Dark Mode & Elegant Night
Deep, dark backgrounds designed for comfortable screen viewing, presentations, and dashboards.

| Style Name | Primary | Secondary | Background (`facecolor`) | Canvas (`figure_facecolor`) | Text Color |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`dark_mode`** | <code style="background:#00e5ff;color:#000000;padding:2px 6px;border-radius:3px;">#00e5ff</code> | <code style="background:#ff007f;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff007f</code> | <code style="background:#121212;color:#ffffff;padding:2px 6px;border-radius:3px;">#121212</code> | <code style="background:#1e1e1e;color:#ffffff;padding:2px 6px;border-radius:3px;">#1e1e1e</code> | <code style="background:#e0e0e0;color:#000000;padding:2px 6px;border-radius:3px;">#e0e0e0</code> |
| **`solarized_dark`** | <code style="background:#268bd2;color:#ffffff;padding:2px 6px;border-radius:3px;">#268bd2</code> | <code style="background:#cb4b16;color:#ffffff;padding:2px 6px;border-radius:3px;">#cb4b16</code> | <code style="background:#002b36;color:#ffffff;padding:2px 6px;border-radius:3px;">#002b36</code> | <code style="background:#073642;color:#ffffff;padding:2px 6px;border-radius:3px;">#073642</code> | <code style="background:#839496;color:#000000;padding:2px 6px;border-radius:3px;">#839496</code> |
| **`obsidian_gold`** | <code style="background:#d4af37;color:#000000;padding:2px 6px;border-radius:3px;">#d4af37</code> | <code style="background:#ffdf00;color:#000000;padding:2px 6px;border-radius:3px;">#ffdf00</code> | <code style="background:#111111;color:#ffffff;padding:2px 6px;border-radius:3px;">#111111</code> | <code style="background:#1b1b1b;color:#ffffff;padding:2px 6px;border-radius:3px;">#1b1b1b</code> | <code style="background:#e6e6e6;color:#000000;padding:2px 6px;border-radius:3px;">#e6e6e6</code> |
| **`deep_ocean`** | <code style="background:#0077b6;color:#ffffff;padding:2px 6px;border-radius:3px;">#0077b6</code> | <code style="background:#00b4d8;color:#000000;padding:2px 6px;border-radius:3px;">#00b4d8</code> | <code style="background:#03045e;color:#ffffff;padding:2px 6px;border-radius:3px;">#03045e</code> | <code style="background:#023e8a;color:#ffffff;padding:2px 6px;border-radius:3px;">#023e8a</code> | <code style="background:#caf0f8;color:#000000;padding:2px 6px;border-radius:3px;">#caf0f8</code> |
| **`midnight_blueprint`** | <code style="background:#48cae4;color:#000000;padding:2px 6px;border-radius:3px;">#48cae4</code> | <code style="background:#90e0ef;color:#000000;padding:2px 6px;border-radius:3px;">#90e0ef</code> | <code style="background:#03045e;color:#ffffff;padding:2px 6px;border-radius:3px;">#03045e</code> | <code style="background:#023e8a;color:#ffffff;padding:2px 6px;border-radius:3px;">#023e8a</code> | <code style="background:#ade8f4;color:#000000;padding:2px 6px;border-radius:3px;">#ade8f4</code> |
| **`nordic_aurora`** | <code style="background:#a3be8c;color:#000000;padding:2px 6px;border-radius:3px;">#a3be8c</code> | <code style="background:#b48ead;color:#000000;padding:2px 6px;border-radius:3px;">#b48ead</code> | <code style="background:#2e3440;color:#ffffff;padding:2px 6px;border-radius:3px;">#2e3440</code> | <code style="background:#3b4252;color:#ffffff;padding:2px 6px;border-radius:3px;">#3b4252</code> | <code style="background:#eceff4;color:#000000;padding:2px 6px;border-radius:3px;">#eceff4</code> |
| **`gothic_rose`** | <code style="background:#d90429;color:#ffffff;padding:2px 6px;border-radius:3px;">#d90429</code> | <code style="background:#ef233c;color:#ffffff;padding:2px 6px;border-radius:3px;">#ef233c</code> | <code style="background:#1b1a1a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1b1a1a</code> | <code style="background:#2b2a2a;color:#ffffff;padding:2px 6px;border-radius:3px;">#2b2a2a</code> | <code style="background:#edf2f4;color:#000000;padding:2px 6px;border-radius:3px;">#edf2f4</code> |
| **`solar_flare`** | <code style="background:#ff9f1c;color:#000000;padding:2px 6px;border-radius:3px;">#ff9f1c</code> | <code style="background:#ffbf69;color:#000000;padding:2px 6px;border-radius:3px;">#ffbf69</code> | <code style="background:#2b2d42;color:#ffffff;padding:2px 6px;border-radius:3px;">#2b2d42</code> | <code style="background:#3a3d59;color:#ffffff;padding:2px 6px;border-radius:3px;">#3a3d59</code> | <code style="background:#ffffff;color:#000000;padding:2px 6px;border-radius:3px;">#ffffff</code> |
| **`boreal_forest`** | <code style="background:#2d6a4f;color:#ffffff;padding:2px 6px;border-radius:3px;">#2d6a4f</code> | <code style="background:#52b788;color:#000000;padding:2px 6px;border-radius:3px;">#52b788</code> | <code style="background:#081c15;color:#ffffff;padding:2px 6px;border-radius:3px;">#081c15</code> | <code style="background:#1b4332;color:#ffffff;padding:2px 6px;border-radius:3px;">#1b4332</code> | <code style="background:#d8f3dc;color:#000000;padding:2px 6px;border-radius:3px;">#d8f3dc</code> |
| **`cherry_dark`** | <code style="background:#ff4d6d;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff4d6d</code> | <code style="background:#c9184a;color:#ffffff;padding:2px 6px;border-radius:3px;">#c9184a</code> | <code style="background:#14080d;color:#ffffff;padding:2px 6px;border-radius:3px;">#14080d</code> | <code style="background:#240d16;color:#ffffff;padding:2px 6px;border-radius:3px;">#240d16</code> | <code style="background:#ffccd5;color:#000000;padding:2px 6px;border-radius:3px;">#ffccd5</code> |
| **`electric_cobalt`** | <code style="background:#3a86ff;color:#ffffff;padding:2px 6px;border-radius:3px;">#3a86ff</code> | <code style="background:#8338ec;color:#ffffff;padding:2px 6px;border-radius:3px;">#8338ec</code> | <code style="background:#0a0f1d;color:#ffffff;padding:2px 6px;border-radius:3px;">#0a0f1d</code> | <code style="background:#131b33;color:#ffffff;padding:2px 6px;border-radius:3px;">#131b33</code> | <code style="background:#e0e7ff;color:#000000;padding:2px 6px;border-radius:3px;">#e0e7ff</code> |
| **`volcano`** | <code style="background:#ff4500;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff4500</code> | <code style="background:#ff8c00;color:#000000;padding:2px 6px;border-radius:3px;">#ff8c00</code> | <code style="background:#1a0f0a;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a0f0a</code> | <code style="background:#2c1810;color:#ffffff;padding:2px 6px;border-radius:3px;">#2c1810</code> | <code style="background:#ffdab9;color:#000000;padding:2px 6px;border-radius:3px;">#ffdab9</code> |
| **`velvet_midnight`** | <code style="background:#7b2cbf;color:#ffffff;padding:2px 6px;border-radius:3px;">#7b2cbf</code> | <code style="background:#9d4edd;color:#ffffff;padding:2px 6px;border-radius:3px;">#9d4edd</code> | <code style="background:#0d0614;color:#ffffff;padding:2px 6px;border-radius:3px;">#0d0614</code> | <code style="background:#1a0d2b;color:#ffffff;padding:2px 6px;border-radius:3px;">#1a0d2b</code> | <code style="background:#e0aaff;color:#000000;padding:2px 6px;border-radius:3px;">#e0aaff</code> |

---

### Cyberpunk, Neon & Synthwave
Ultra-vibrant, high-energy luminous accents set against pitch-black or deep violet backdrops.

| Style Name | Primary | Secondary | Background (`facecolor`) | Canvas (`figure_facecolor`) | Text Color |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`cyberpunk`** | <code style="background:#fcee0a;color:#000000;padding:2px 6px;border-radius:3px;">#fcee0a</code> | <code style="background:#00ffcc;color:#000000;padding:2px 6px;border-radius:3px;">#00ffcc</code> | <code style="background:#050505;color:#ffffff;padding:2px 6px;border-radius:3px;">#050505</code> | <code style="background:#120458;color:#ffffff;padding:2px 6px;border-radius:3px;">#120458</code> | <code style="background:#00ffcc;color:#000000;padding:2px 6px;border-radius:3px;">#00ffcc</code> |
| **`cyberpunk_tokyo`** | <code style="background:#ff0055;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff0055</code> | <code style="background:#7928ca;color:#ffffff;padding:2px 6px;border-radius:3px;">#7928ca</code> | <code style="background:#0d0221;color:#ffffff;padding:2px 6px;border-radius:3px;">#0d0221</code> | <code style="background:#190538;color:#ffffff;padding:2px 6px;border-radius:3px;">#190538</code> | <code style="background:#00f0ff;color:#000000;padding:2px 6px;border-radius:3px;">#00f0ff</code> |
| **`cyber_punk_pink`** | <code style="background:#ff007f;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff007f</code> | <code style="background:#7928ca;color:#ffffff;padding:2px 6px;border-radius:3px;">#7928ca</code> | <code style="background:#05020a;color:#ffffff;padding:2px 6px;border-radius:3px;">#05020a</code> | <code style="background:#0f071f;color:#ffffff;padding:2px 6px;border-radius:3px;">#0f071f</code> | <code style="background:#ffb3d9;color:#000000;padding:2px 6px;border-radius:3px;">#ffb3d9</code> |
| **`cyber_ninja`** | <code style="background:#ff3366;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff3366</code> | <code style="background:#33ccff;color:#000000;padding:2px 6px;border-radius:3px;">#33ccff</code> | <code style="background:#08080c;color:#ffffff;padding:2px 6px;border-radius:3px;">#08080c</code> | <code style="background:#12121c;color:#ffffff;padding:2px 6px;border-radius:3px;">#12121c</code> | <code style="background:#f0f0f5;color:#000000;padding:2px 6px;border-radius:3px;">#f0f0f5</code> |
| **`cyber_amber`** | <code style="background:#ffb703;color:#000000;padding:2px 6px;border-radius:3px;">#ffb703</code> | <code style="background:#fb8500;color:#000000;padding:2px 6px;border-radius:3px;">#fb8500</code> | <code style="background:#0a0802;color:#ffffff;padding:2px 6px;border-radius:3px;">#0a0802</code> | <code style="background:#1c1404;color:#ffffff;padding:2px 6px;border-radius:3px;">#1c1404</code> | <code style="background:#ffecb6;color:#000000;padding:2px 6px;border-radius:3px;">#ffecb6</code> |
| **`neon_purple`** | <code style="background:#b537f2;color:#ffffff;padding:2px 6px;border-radius:3px;">#b537f2</code> | <code style="background:#00f0ff;color:#000000;padding:2px 6px;border-radius:3px;">#00f0ff</code> | <code style="background:#0c0714;color:#ffffff;padding:2px 6px;border-radius:3px;">#0c0714</code> | <code style="background:#181026;color:#ffffff;padding:2px 6px;border-radius:3px;">#181026</code> | <code style="background:#f3eff5;color:#000000;padding:2px 6px;border-radius:3px;">#f3eff5</code> |
| **`neon_lime`** | <code style="background:#39ff14;color:#000000;padding:2px 6px;border-radius:3px;">#39ff14</code> | <code style="background:#ff073a;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff073a</code> | <code style="background:#0a0a0a;color:#ffffff;padding:2px 6px;border-radius:3px;">#0a0a0a</code> | <code style="background:#141414;color:#ffffff;padding:2px 6px;border-radius:3px;">#141414</code> | <code style="background:#f1f1f1;color:#000000;padding:2px 6px;border-radius:3px;">#f1f1f1</code> |
| **`neon_toxic`** | <code style="background:#adff2f;color:#000000;padding:2px 6px;border-radius:3px;">#adff2f</code> | <code style="background:#00ff7f;color:#000000;padding:2px 6px;border-radius:3px;">#00ff7f</code> | <code style="background:#0a120a;color:#ffffff;padding:2px 6px;border-radius:3px;">#0a120a</code> | <code style="background:#101e10;color:#ffffff;padding:2px 6px;border-radius:3px;">#101e10</code> | <code style="background:#ccffcc;color:#000000;padding:2px 6px;border-radius:3px;">#ccffcc</code> |
| **`neon_amethyst`** | <code style="background:#9d4edd;color:#ffffff;padding:2px 6px;border-radius:3px;">#9d4edd</code> | <code style="background:#c77dff;color:#000000;padding:2px 6px;border-radius:3px;">#c77dff</code> | <code style="background:#10002b;color:#ffffff;padding:2px 6px;border-radius:3px;">#10002b</code> | <code style="background:#240046;color:#ffffff;padding:2px 6px;border-radius:3px;">#240046</code> | <code style="background:#e0aaff;color:#000000;padding:2px 6px;border-radius:3px;">#e0aaff</code> |
| **`retro_synth`** | <code style="background:#ff0055;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff0055</code> | <code style="background:#00ffff;color:#000000;padding:2px 6px;border-radius:3px;">#00ffff</code> | <code style="background:#110c1d;color:#ffffff;padding:2px 6px;border-radius:3px;">#110c1d</code> | <code style="background:#1f1738;color:#ffffff;padding:2px 6px;border-radius:3px;">#1f1738</code> | <code style="background:#ff00aa;color:#ffffff;padding:2px 6px;border-radius:3px;">#ff00aa</code> |
| **`synthwave_sunset`** | <code style="background:#ff70a6;color:#000000;padding:2px 6px;border-radius:3px;">#ff70a6</code> | <code style="background:#ff9770;color:#000000;padding:2px 6px;border-radius:3px;">#ff9770</code> | <code style="background:#2b1055;color:#ffffff;padding:2px 6px;border-radius:3px;">#2b1055</code> | <code style="background:#3c1361;color:#ffffff;padding:2px 6px;border-radius:3px;">#3c1361</code> | <code style="background:#ffd6ff;color:#000000;padding:2px 6px;border-radius:3px;">#ffd6ff</code> |
| **`matrix`** | <code style="background:#00ff00;color:#000000;padding:2px 6px;border-radius:3px;">#00ff00</code> | <code style="background:#008f11;color:#ffffff;padding:2px 6px;border-radius:3px;">#008f11</code> | <code style="background:#000000;color:#ffffff;padding:2px 6px;border-radius:3px;">#000000</code> | <code style="background:#0a0a0a;color:#ffffff;padding:2px 6px;border-radius:3px;">#0a0a0a</code> | <code style="background:#00ff66;color:#000000;padding:2px 6px;border-radius:3px;">#00ff66</code> |
| **`cyber_matrix_dark`** | <code style="background:#00ff66;color:#000000;padding:2px 6px;border-radius:3px;">#00ff66</code> | <code style="background:#00b347;color:#000000;padding:2px 6px;border-radius:3px;">#00b347</code> | <code style="background:#020802;color:#ffffff;padding:2px 6px;border-radius:3px;">#020802</code> | <code style="background:#051405;color:#ffffff;padding:2px 6px;border-radius:3px;">#051405</code> | <code style="background:#80ffaa;color:#000000;padding:2px 6px;border-radius:3px;">#80ffaa</code> |

---

## 3. Customizing & Overriding Style Colors

You can load a base style and selectively override individual color parameters using keyword arguments (`**kwargs`):

```python
# Load 'dark_mode' but use a custom yellow primary accent
Data.set_style("dark_mode", primary="#ffea00", secondary="#00ff66")
```

### Style Attributes Reference

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `primary` | Hex code (`str`) | Color for main data curves, scatter markers, bars, and box plot bodies. |
| `secondary` | Hex code (`str`) | Color for linear trendlines (`fit=True`), medians, and error caps. |
| `facecolor` | Hex code (`str`) | Background color inside axes plot area. |
| `figure_facecolor` | Hex code (`str`) | Canvas background color surrounding the main plot axes. |
| `grid_color` | Hex code (`str`) | Color for background dashed grid lines. |
| `text_color` | Hex code (`str`) | Color for titles, axis names, and tick labels. |
| `error_color` | Hex code (`str`) | Color for $1\sigma$ measurement error bars and caps. |

---

## 4. Registering Custom Styles (`register_style`)

To save a custom palette for reuse across your scripts or research group, register it into ElevenOne's global style dictionary:

```python
from elevenone import Data

# Register a custom brand theme
Data.register_style(
    name="my_lab_theme",
    primary="#0284c7",
    secondary="#e11d48",
    facecolor="#f8fafc",
    figure_facecolor="#ffffff",
    grid_color="#cbd5e1",
    text_color="#0f172a",
    error_color="#64748b"
)

# Apply your custom theme globally
Data.set_style("my_lab_theme")
```

---

## 5. Integrating with Matplotlib Subplots (`ax`)

Passing an existing Matplotlib `ax` object allows you to place ElevenOne visualizations directly inside complex grid layouts while retaining active styling parameters:

```python
import matplotlib.pyplot as plt
import elevenone as eo
from elevenone.basic_units import V, A, s

# Apply global theme
eo.Data.set_style("nordic")

dataset = eo.Data({
    "Time": [1, 2, 3, 4] * s,
    "Voltage": [1.0, 2.1, 3.2, 4.0] * V,
    "Current": [0.1, 0.2, 0.3, 0.4] * A
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

dataset.plot(x="Time", y="Voltage", ax=ax1, title="Voltage Response")
dataset.scatter(x="Current", y="Voltage", fit=True, ax=ax2, title="V-I Fitting")

plt.show()
```