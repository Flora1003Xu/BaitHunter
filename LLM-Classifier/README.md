# LLM Classifier

This project analyzes dark mode interfaces across transitions using OCR, CV, and LLM technologies. Based on screenshot data before and after interface transitions, it determines whether the transition is misleading.

---

### Features

Provides pairs of screenshot data before and after interface transitions, outputting the level of consistency between the interfaces.

- Supports batch analysis
- Supports analysis of individual instances

---

### Quick Start

**1. Environment Setup:** Refer to `requirements.txt`

**2. Data Preparation:**

- For batch analysis: Populate the data folder with data, placing each screenshot pair in a separate subfolder.

```
data/
├── case1 to be tested/
│   ├── before_file.jpg(png)
│   └── after_file.jpg(png)
├── case2 to be tested/
│   └── before_file.jpg(png)
│   └── after_file.jpg(png)
├── ....../
```

- For single instance analysis: Place the pair of before and after screenshots in the data folder.

```
data/
├── before_file.jpg(png)
├── after_file.jpg(png)
```

**3. Execution:**

```js
python main.py
```

---

### Execution Results

Each case generates a result.json file, stored in the folder at the same level as the corresponding screenshot pair.
