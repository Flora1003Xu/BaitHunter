# LLM分类器

本项目通过OCR、CV、LLM等技术分析跨界面的暗模式界面，基于界面跳转前后的截图数据，判断跳转是否具有误导性。

---

### 功能特点

提供界面跳转前后的截图数据对，输出跳转前后界面一致性的等级。

- 支持批量分析
- 支持单例子分析

---


### 快速开始

**1. 环境准备：** 参考`requirements.txt`

**2. 数据准备：**

- 批量分析：在data文件夹下填充数据，每个截图对放在单独的一个子文件夹中。

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

- 单例子分析：将跳转前后截图对放在data文件夹下。

```
data/
├── before_file.jpg(png)
├── after_file.jpg(png)
```

**3. 运行：**

```js
python main.py
```

---

### 运行效果

每个例子生成一个result.json文件，存放在和对应截图对同级的文件夹下。

