module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation
        'style',    // Formatting, no code change
        'refactor', // Code change that neither fixes a bug nor adds a feature
        'perf',     // Performance improvement
        'test',     // Adding tests
        'chore',    // Maintenance
        'ci',       // CI/CD changes
        'build',    // Build system changes
        'revert',   // Revert a commit
      ],
    ],
    'scope-enum': [
      2,
      'always',
      [
        'falcon-js',
        'falcon-python',
        'falcon-react',
        'falcon-nextjs',
        'pigeon-js',
        'pigeon-python',
        'sage-js',
        'sage-python',
        'deps',
        'release',
      ],
    ],
    'scope-empty': [1, 'never'], // Warn if no scope
  },
};
