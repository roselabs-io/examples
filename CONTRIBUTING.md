# Contributing to Rose Labs Examples

Thank you for your interest in contributing!

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/). All commits must follow this format:

```
type(scope): description
```

### Types

- `feat` - New example or feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Formatting, no code change
- `refactor` - Code refactoring
- `chore` - Maintenance tasks

### Scopes

- `falcon-js`, `falcon-python`, `falcon-react`, `falcon-nextjs`
- `pigeon-js`, `pigeon-python`
- `sage-js`, `sage-python`
- `deps` - Dependency updates

### Examples

```bash
feat(falcon-js): add Next.js example
fix(pigeon-python): correct async handling
docs(sage-js): improve README
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-example`
3. Make your changes
4. Commit with conventional commit message
5. Push and create a PR against `main`

## Adding a New Example

1. Create a directory under the appropriate SDK folder:
   ```
   falcon-js/
   └── my-new-example/
       ├── README.md
       ├── package.json
       └── index.js
   ```

2. Include a README with:
   - What the example demonstrates
   - Setup instructions
   - How to run it

3. Keep examples minimal and focused

## Questions?

Open an issue or reach out at support@roselabs.io
