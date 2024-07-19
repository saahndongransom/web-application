CKEDITOR.config.contentsCss = ['/static/css/bootstrap.min.css'];
CKEDITOR.config.templates_files = ['/static/js/ckeditor_templates.js'];
CKEDITOR.config.extraPlugins = 'widget,dialog,dialogui,lineutils,clipboard,notification,stylesheetparser,videoembed';
CKEDITOR.config.toolbar = [['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'], ['Undo', 'Redo'], ['Link', 'Unlink'], ['Table', 'HorizontalRule', 'SpecialChar'], ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'], ['Image', 'Video', 'Embed'], ['Format', 'Font', 'FontSize', 'TextColor', 'BGColor'], ['Maximize', 'Source']];

CKEDITOR.stylesSet.add('bootstrap', [    {name: 'Image responsive', element: 'img', attributes: {'class': 'img-fluid'}}]);

CKEDITOR.editorConfig = function (config) {
    config.stylesSet = 'bootstrap';
};