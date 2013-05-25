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
    watch: {
      dev: {
        files: [
          'comics/static/stylesheets/**/*'
        ],
        tasks: [
          'less:dev'
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
        }],
      }
    }
  });

  grunt.registerTask("dev", ["less:dev", "watch"]);
  grunt.registerTask("build", ["uglify", "less:dist"]);
};
