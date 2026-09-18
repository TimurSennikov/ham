# HAM

Half-Life Addon Manager (HAM) can be used to easily install Half-Life addons.

![License](https://img.shields.io/badge/license-GPL-3-0.svg) ![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

- Easy Half-Life addon managing.

### Tech Stack

- **Python**

## Installation

```bash
git clone https://github.com/TimurSennikov/ham.git
cd ham
echo "alias ham='python3 $(pwd)/main.py'" >> ~/.bashrc
```

## Usage

### Get help
```bash
ham --help
```

### Initialize HAM pack in current directory
```bash
ham init <name>
```

### Change HAM pack bg
```bash
ham bg <path_to_bg_image>
```

### Change HAM pack skybox
```bash
ham skybox <path_to_skybox_image> <skybox_name>
```
#### Leave <skybox_name> empty to replace all of the available skyboxes.

### Build HAM pack (convert to ZIP)
```bash
ham build
```

### Install HAM pack
```bash
ham install
```

### Install HAM pack from ZIP
```bash
ham install --hamfile pack.ham
```

### Uninstall installed HAM pack
```bash
ham uninstall
```

### Show HAM packs history
```bash
ham history
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

Made with ❤ by [TimurSennikov](https://github.com/TimurSennikov)
