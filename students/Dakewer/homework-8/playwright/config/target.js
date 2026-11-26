// Application under test. Override with the TODO_URL environment variable.
const BASE_URL = process.env.TODO_URL || "https://todomvc.com/examples/react/dist/";
const IS_LOCAL_BUILD = ['localhost', '127.0.0.1'].includes(new URL(BASE_URL).hostname);

module.exports = { BASE_URL, IS_LOCAL_BUILD };
