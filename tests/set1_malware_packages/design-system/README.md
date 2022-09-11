#  Design System

## Usage
`design-system-v2` is under development. It will replace current `@axie/design-system` at some point in the future.

1. Add `"@sky-mavis/design-system": "1.0.0"` to your package.json.
2. Run `yarn`

## Development
`yarn dev` Watch changes in the package.

## Build
`yarn build` By default, `design-system-v2` will be compiled with `ES6` target.

`yarn build:esnext` Build with ESNext target which support [ES proposed features](https://github.com/tc39/proposals).

`yarn build:commonjs` build with CommonJS module resolver.

## Publish
Coming soon.

## Ronin DS dev 17/05/2021
Change `workspaces` property in `package.json` of `supreme` to `[packages/design-system-v2, packages/design-system-docs]`

Upgrade `nodejs` to latest stable version. Upgrade `node-gyp` to 8.0 version.

Remove `node-modules`, `yarn.lock`

Re-run `yarn`
