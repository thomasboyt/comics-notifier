module.exports = function(grunt) {
  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);
  grunt.initConfig({
    uglify: {
      dist: {
        files: {
          'dist/scripts.js': [
            'comics/static/components/jquery/jquery.min.js',
            'comics/static/components/bootstrap/js/bootstrap-typeahead.js',
            'comics/static/components/bootstrap/js/bootstrap-alert.js',
            'comics/static/js/main.js'
          ]
        }
      }
    },
    cssmin: {
      dist: {
        files: {
          'dist/styles.css': [
            'comics/static/components/bootstrap/docs/assets/css/bootstrap.css',
            'comics/static/stylesheets/main.css'
          ]
        }
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
          dest: "dist/"
        }]
      }
    }
  });

  grunt.registerTask("default", ["uglify", "cssmin"]);
};
