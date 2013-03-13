TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced", 
    'content_css': '/static/css/wheel_content.css',
    'style_formats': [
        { 'title': 'Images'},
        { 'title': 'Original Size Image', 'selector': 'img', 'attributes': {'class': 'img_content_original' }},
        { 'title': 'Thumbnail Image', 'selector': 'img', 'attributes': {'class': 'img_content_thumb' }},
        { 'title': 'Small Image', 'selector': 'img', 'attributes': {'class': 'img_content_small' }},
        { 'title': 'Medium Image', 'selector': 'img', 'attributes': {'class': 'img_content_medium'} },
        { 'title': 'Large Image', 'selector': 'img', 'attributes': {'class': 'img_content_large' }},
        #{ 'title': 'Test'},
        #{ 'title': "Boohoold", 'inline': 'b' },
        ],

    'relative_urls': False, 
    'theme_advanced_toolbar_location':'top', 
    'theme_advanced_resizing':True, 
    'plugins':'table, paste, wheel_browser',
    'table_styles' : "Header 1=header1;Header 2=header2;Header 3=header3",
    'table_cell_styles' : "Header 1=header1;Header 2=header2;Header 3=header3;Table Cell=tableCel1",
    'table_row_styles' : "Header 1=header1;Header 2=header2;Header 3=header3;Table Row=tableRow1",
    'table_cell_limit' : 100,
    'table_row_limit' : 5,
    'table_col_limit' : 5,
    'width':800,
    'height':600,
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect",
    'theme_advanced_buttons2' : "bullist,numlist,|,outdent,indent,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,hr,removeformat,visualaid,|,sub,sup,|,charmap",
    'theme_advanced_buttons3': "tablecontrols,|,pastetext,pasteword,selectall",
    'paste_auto_cleanup_on_paste' : True

}
