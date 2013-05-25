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
    cssmin: {
      dist: {
        files: {
          'dist/styles.css': [
            'comics/static/components/bootstrap/docs/assets/css/bootstrap.css',
            'comics/static/components/font-awesome/build/assets/font-awesome/css/font-awesome.min.css',
            'comics/static/stylesheets/typeahead.js-bootstrap.css',
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
          dest: "static/"
        },
        {
          src: "comics/static/js/*",
          dest: "static/js/"
        },
        {
          src: "comics/static/img/*",
          dest: "static/img/"
        }],
      }
    }
  });

  grunt.registerTask("build", ["uglify", "cssmin"]);
};
