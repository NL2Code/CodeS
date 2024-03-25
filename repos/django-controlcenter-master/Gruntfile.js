'use strict';

module.exports = function(grunt) {
    var css_path = 'controlcenter/static/controlcenter/css/',
        styl_path = 'controlcenter/stylus/',
        file_names = ['all', 'chartist-default-colors', 'chartist-material-colors'],
        files = {};

    for (var i = 0; i < file_names.length; i++){
        files[css_path + file_names[i] + '.css'] = styl_path + file_names[i] + '.styl';
    }

    grunt.initConfig({
        stylus: {
            build: {
                options: {
                    compress: false,
                    urlfunc: 'embedurl',
                    use: [
                        function(){
                            return require('autoprefixer-stylus')('last 2 versions');
                        }
                    ]
                },
                files: files
            }
        },

        combine_mq: {
            build: {
                src: css_path + 'all.css',
                dest: css_path + 'all.css'
            }
        },

        watch: {
            css: {
                files: styl_path + '*.styl',
                tasks: ['stylus:build', 'combine_mq:build']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-stylus');
    grunt.loadNpmTasks('grunt-combine-mq');
    grunt.registerTask('default', ['stylus', 'combine_mq']);
};