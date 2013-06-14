module.exports = function(grunt) {
  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);
  grunt.initConfig({
    uglify: {
      dist: {
        files: {
          'dist/scripts.js': [
            'comics/static/components/jquery/jquery.min.js',
            'comics/static/components/bootstrap/js/bootstrap-alert.js',
            'comics/static/components/typeahead.js/dist/typeahead.js',
            'comics/static/components/angular/angular.min.js'
          ]
        }
      }
    },
    less: {
      dev: {
        files: {
          'comics/static/tmp/styles.css': 'comics/static/stylesheets/main.less'
        }
      },
      dist: {
        files: {
          'dist/styles.css': 'comics/static/stylesheets/main.less'
        },
        options: {
          'yuicompress': true
        }
      }
    },
    ngtemplates: {
      whampow: {
        options: {
          base: "comics/static/ng-templates/"
        },
        src: "comics/static/ng-templates/*.html",
        dest: "comics/static/tmp/templates.js"
      }
    },
    watch: {
      less: {
        files: [
          'comics/static/stylesheets/**/*'
        ],
        tasks: [
          'less:dev'
        ]
      },
      ngtemplates: {
        files: [
          'comics/static/ng-templates/**/*'
        ],
        tasks: [
          'ngtemplates'
        ]
      }
    },
    s3: {
      options: {
        bucket: 'comics-notifier',
        access: 'public-read-write'
      },
      dist: {
        upload: [{
          src: "dist/*",
          dest: "static/"
        }, {
          src: "comics/static/js/*",
          dest: "static/js/"
        }, {
          src: "comics/static/img/*",
          dest: "static/img/"
        }, {
          src: "comics/static/font/*",
          dest: "font/"
        }, {
          src: "comics/static/tmp/templates.js",
          dest: "static/tmp/templates.js"
        }],
      }
    }
  });

  grunt.registerTask("dev", ["less:dev", "ngtemplates", "watch"]);
  grunt.registerTask("build", ["ngtemplates", "uglify", "less:dist"]);
};
