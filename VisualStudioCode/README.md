# ThoughtWorks Theme in Visual Studio Code

## Usage

- Open your `vscode`
- View extensions
- More Actions -> Install form VSIX...
- Select `thoughtworks-theme-*.*.*.vsix`
- Reload your `vscode` and can select the new theme

## Contribution

`light_all.json` is the original file of `vscode` which is the default light theme. Using the converting tool in the roor directory `convert.py` and the ThoughtWorks palette `ThoughtWorks.palette` to generate the theme file `thoughtworks.json`.

### Package

```npx vsce package```

### TODO

- dedupe the same keys in `tokenColors` in `light_all.json`