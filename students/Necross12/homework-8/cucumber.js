module.exports = {
  default: {
    require: ['features/support/**/*.js', 'features/step_definitions/**/*.js'],
    paths: ['features/**/*.feature'],
    format: ['progress-bar', 'html:reports/cucumber-report.html'],
  },
};
