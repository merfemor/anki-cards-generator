export default [
    {
        files: ['src/app/static/**/*.js'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'module',
            globals: {
                Alpine: 'readonly',
                Blob: 'readonly',
                Response: 'readonly',
                alert: 'readonly',
                console: 'readonly',
                document: 'readonly',
                fetch: 'readonly',
                window: 'readonly',
            },
        },
        rules: {
            'no-undef': 'error',
            'no-unused-vars': ['error', { args: 'none' }],
        },
    },
];
