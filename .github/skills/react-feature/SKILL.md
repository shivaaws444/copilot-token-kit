---
name: react-feature
description: Build or change a React UI feature (component, page, form, hook, API wiring) following existing project patterns. Use for any frontend/UI/React/JSX/TSX request.
---
# React Feature
1. Find ONE similar component and copy its structure, styling, state and data-fetching approach.
2. Component < ~150 lines; extract hooks for logic. Props typed (TS or PropTypes, matching repo).
3. Forms: existing form lib + validation mirroring backend Bean Validation rules.
4. States: loading, error, empty, success. Accessible labels and keyboard support.
5. Test with React Testing Library: render, interact, assert visible output; mock the API layer.
Done when: `npm test -- <file>` and lint pass. Output changed hunks + 3-line summary.
